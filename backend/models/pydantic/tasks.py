from config import TaskPriority
from datetime import datetime
from pydantic import BaseModel
from typing import Literal

class SchemaTask(BaseModel): 
    title: str 
    description: str | None = None
    priority:Literal[
        TaskPriority.low,
        TaskPriority.medium,
        TaskPriority.high
    ] = TaskPriority.medium
    due_date: datetime | None = None
    assignee_id: int | None = None

class ResponseTask(BaseModel): 
    id: int
    title: str
    description: str | None = None
    assignee_id: int | None = None
    column_id: int 
    project_id: int

class CreateTask(SchemaTask): pass

class UpdateTask(SchemaTask): pass