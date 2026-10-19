from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, field_validator

class TarefaModelo(BaseModel): 
    id: int
    title: str
    description: str
    priority: Literal["low", "medium", "high"]
    status: Literal["pending", "in_progress", "completed"]
    due_date: date

    @field_validator('title')
    @classmethod 
    def clean_code(cls, tit) -> str:
        return tit.title()

class TaskStatusUpdate(BaseModel):
    status: Literal["pending", "in_progress", "completed"]

class EmailPayload(BaseModel):
    email: str

class TaskUpdatePayload(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    status: Optional[Literal["pending", "in_progress", "completed"]] = None
    due_date: Optional[str] = None