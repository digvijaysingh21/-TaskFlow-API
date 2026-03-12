from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.schemas.user import UserPublic
from app.schemas.task import TaskOut

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(default=None. max_length=1000)

    @field_validator("name")
    @classmethod
    def name_strip(cls, v:str) -> str:
        return v.strip()
    
class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)


class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int 
    created_at: datetime 
    updated_at: datetime 

    model_config = {"from_attributes": True}


# Detailed project - includes members and tasks (nested models)

class ProjectDetail(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner: UserPublic
    members: list[UserPublic] = []
    tasks: list[TaskOut] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
