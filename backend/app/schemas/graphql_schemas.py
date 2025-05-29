import strawberry
from typing import List, Optional
from datetime import datetime
from enum import Enum

@strawberry.enum
class TaskStatusGQL(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

@strawberry.enum
class TaskPriorityGQL(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@strawberry.type
class TaskGQL:
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    category: str
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    owner_id: int

@strawberry.input
class TaskFilterGQL:
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None

@strawberry.input
class TaskInputGQL:
    title: str
    description: Optional[str] = None
    status: str = "todo"
    priority: str = "medium"
    category: str = "General"
    due_date: Optional[datetime] = None

@strawberry.input
class TaskUpdateInputGQL:
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None