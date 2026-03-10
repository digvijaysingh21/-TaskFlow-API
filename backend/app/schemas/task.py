from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime
from app.schemas.enums import TaskStatus, TaskPriority


# ── CREATE ───────────────────────────────────────────────────────────
class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Title of the task",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Detailed description of the task",
    )
    status: TaskStatus = Field(
        default=TaskStatus.pending,
        description="Current status of the task",
    )
    priority: TaskPriority = Field(
        default=TaskPriority.medium,
        description="Priority level",
    )
    project_id: int = Field(
        ...,
        ge=1,
        description="ID of the project this task belongs to",
    )
    assigned_to: Optional[int] = Field(
        default=None,
        ge=1,
        description="User ID of the assignee",
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="Due date in ISO 8601 format",
    )

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("Title cannot be blank or whitespace only")
        return v.strip()

    @model_validator(mode="after")
    def due_date_required_if_in_progress(self):
        if self.status == TaskStatus.in_progress and self.due_date is None:
            raise ValueError("Tasks marked as in_progress must have a due_date")
        return self


# ── UPDATE (all fields optional for PATCH) ───────────────────────────
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assigned_to: Optional[int] = Field(default=None, ge=1)
    due_date: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v.strip() == "":
            raise ValueError("Title cannot be blank")
        return v.strip() if v else v


# ── OUT (what we return to the client) ───────────────────────────────
class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    project_id: int
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
    # from_attributes=True lets Pydantic read from SQLAlchemy
    # model objects (not just dicts) — needed in Session 6


# ── LIST RESPONSE (wrapper for paginated list) ────────────────────────
class TaskListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[TaskOut]