from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import strawberry
from app.schemas.graphql_schemas import (
    TaskGQL, TaskFilterGQL, TaskInputGQL, TaskUpdateInputGQL
)
from app.services.task_service import TaskService
from app.database import get_db
from typing import Optional

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            message_str = json.dumps(message)
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(message_str)
                except Exception as e:
                    print(e)
                    pass

    async def broadcast_task_update(self, task_data: dict, user_id: int):
        message = {
            "type": "task_update",
            "data": task_data
        }
        await self.send_personal_message(message, user_id)

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

@strawberry.type
class Query:
    @strawberry.field
    def tasks(
        self, 
        filters: Optional[TaskFilterGQL] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[TaskGQL]:
        db = next(get_db())
        user_id = 1  # Simplified for demo - in real app, get from auth context
        
        filter_dict = {}
        if filters:
            if filters.status:
                filter_dict['status'] = filters.status
            if filters.priority:
                filter_dict['priority'] = filters.priority
            if filters.category:
                filter_dict['category'] = filters.category
        
        tasks = TaskService.get_tasks(
            db=db, 
            user_id=user_id, 
            skip=skip, 
            limit=limit,
            **filter_dict
        )
        
        return [TaskGQL(**task.__dict__) for task in tasks]
    
    @strawberry.field
    def task(self, id: int) -> Optional[TaskGQL]:
        db = next(get_db())
        user_id = 1  # Simplified
        
        task = TaskService.get_task(db=db, task_id=id, user_id=user_id)
        if not task:
            return None
            
        return TaskGQL(**task.__dict__)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_task(self, task_input: TaskInputGQL) -> TaskGQL:
        db = next(get_db())
        user_id = 1  # Simplified
        
        task_data = {
            "title": task_input.title,
            "description": task_input.description,
            "status": task_input.status,
            "priority": task_input.priority,
            "category": task_input.category,
            "due_date": task_input.due_date
        }
        
        task = TaskService.create_task(db=db, task_data=task_data, user_id=user_id)
        return TaskGQL(**task.__dict__)
    
    @strawberry.mutation
    def update_task(self, id: int, task_input: TaskUpdateInputGQL) -> Optional[TaskGQL]:
        db = next(get_db())
        user_id = 1  # Simplified
        
        task_data = {}
        if task_input.title is not None:
            task_data["title"] = task_input.title
        if task_input.description is not None:
            task_data["description"] = task_input.description
        if task_input.status is not None:
            task_data["status"] = task_input.status
        if task_input.priority is not None:
            task_data["priority"] = task_input.priority
        if task_input.category is not None:
            task_data["category"] = task_input.category
        if task_input.due_date is not None:
            task_data["due_date"] = task_input.due_date
        
        task = TaskService.update_task(db=db, task_id=id, user_id=user_id, task_data=task_data)
        if not task:
            return None
            
        return TaskGQL(**task.__dict__)
    
    @strawberry.mutation
    def delete_task(self, id: int) -> bool:
        db = next(get_db())
        user_id = 1  # Simplified
        
        return TaskService.delete_task(db=db, task_id=id, user_id=user_id)

# Create GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)