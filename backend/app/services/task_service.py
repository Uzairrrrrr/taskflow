from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.task import Task
from app.models.user import User
from datetime import datetime

class TaskService:
    @staticmethod
    def get_tasks(
        db: Session, 
        user_id: int, 
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Task]:
        query = db.query(Task).filter(Task.owner_id == user_id)
        
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)
        if category:
            query = query.filter(Task.category == category)
            
        return query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_task(db: Session, task_id: int, user_id: int) -> Optional[Task]:
        return db.query(Task).filter(
            Task.id == task_id, 
            Task.owner_id == user_id
        ).first()
    
    @staticmethod
    def create_task(db: Session, task_data: dict, user_id: int) -> Task:
        db_task = Task(**task_data, owner_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def update_task(db: Session, task_id: int, user_id: int, task_data: dict) -> Optional[Task]:
        db_task = TaskService.get_task(db, task_id, user_id)
        if not db_task:
            return None
        
        for key, value in task_data.items():
            if value is not None:
                setattr(db_task, key, value)
        
        if task_data.get('status') == 'completed' and not db_task.completed_at:
            db_task.completed_at = datetime.utcnow()
        elif task_data.get('status') != 'completed':
            db_task.completed_at = None
            
        db_task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def delete_task(db: Session, task_id: int, user_id: int) -> bool:
        db_task = TaskService.get_task(db, task_id, user_id)
        if not db_task:
            return False
        
        db.delete(db_task)
        db.commit()
        return True