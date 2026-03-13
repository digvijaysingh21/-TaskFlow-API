# from fastapi import APIRouter, HTTPException, Query, Path
# from typing import Optional


# router = APIRouter(
#     prefix="/tasks",
#     tags=["Tasks"],
# )

# # ── Fake in-memory DB (will be replaced with real DB in Session 6) ──
# fake_tasks_db = [
#     {"id": 1, "title": "Set up FastAPI project", "status": "done", "priority": "high", "project_id": 1},
#     {"id": 2, "title": "Design database schema", "status": "in_progress", "priority": "high", "project_id": 1},
#     {"id": 3, "title": "Write authentication logic", "status": "pending", "priority": "medium", "project_id": 1},
#     {"id": 4, "title": "Add Redis caching", "status": "pending", "priority": "low", "project_id": 2},
#     {"id": 5, "title": "Write tests", "status": "pending", "priority": "medium", "project_id": 2},
# ]

# # ── GET /tasks ──────────────────────────────────────────────────────
# @router.get("/", summary="Get all tasks")
# async def get_tasks(
#     skip: int = Query(default=0, ge=0, description="Number of records to skip"),
#     limit: int = Query(default=10, ge=1, le=100, description="Max records to return"),
#     status: Optional[str] = Query(default=None, description="Filter by status: pending, in_progress, done"),
#     priority: Optional[str] = Query(default=None, description="Filter by priority: low, medium, high"),
#     project_id: Optional[int] = Query(default=None, description="Filter by project ID"),
# ):
#     """
#     Retrieve all tasks with optional filters and pagination.
#     - **skip**: how many records to skip (for pagination)
#     - **limit**: max records to return
#     - **status**: filter by task status
#     - **priority**: filter by priority level
#     - **project_id**: filter tasks belonging to a project
#     """
#     results = fake_tasks_db

#     # Apply filters
#     if status:
#         results = [t for t in results if t["status"] == status]
#     if priority:
#         results = [t for t in results if t["priority"] == priority]
#     if project_id:
#         results = [t for t in results if t["project_id"] == project_id]

#     # Apply pagination
#     total = len(results)
#     results = results[skip : skip + limit]

#     return {
#         "total": total,
#         "skip": skip,
#         "limit": limit,
#         "data": results,
#     }


# # ── GET /tasks/stats ────────────────────────────────────────────────
# # IMPORTANT: this must come BEFORE /tasks/{task_id}
# @router.get("/stats", summary="Get task statistics")
# async def get_task_stats():
#     """
#     Returns a count breakdown of tasks by status and priority.
#     """
#     stats = {
#         "total": len(fake_tasks_db),
#         "by_status": {},
#         "by_priority": {},
#     }

#     for task in fake_tasks_db:
#         # Count by status
#         s = task["status"]
#         stats["by_status"][s] = stats["by_status"].get(s, 0) + 1

#         # Count by priority
#         p = task["priority"]
#         stats["by_priority"][p] = stats["by_priority"].get(p, 0) + 1

#     return stats


# # ── GET /tasks/{task_id} ────────────────────────────────────────────
# @router.get("/{task_id}", summary="Get a single task")
# async def get_task(
#     task_id: int = Path(..., ge=1, description="The ID of the task to retrieve"),
# ):
#     """
#     Retrieve a single task by its ID.
#     Raises 404 if not found.
#     """
#     task = next((t for t in fake_tasks_db if t["id"] == task_id), None)
#     if not task:
#         raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
#     return task


# # ── POST /tasks ─────────────────────────────────────────────────────
# @router.post("/", status_code=201, summary="Create a new task")
# async def create_task(task: dict):
#     """
#     Create a new task.
#     Requires: title, status, priority, project_id
#     (We will replace `dict` with a proper Pydantic schema in Session 3)
#     """
#     new_task = {
#         "id": len(fake_tasks_db) + 1,
#         "title": task.get("title", "Untitled"),
#         "status": task.get("status", "pending"),
#         "priority": task.get("priority", "medium"),
#         "project_id": task.get("project_id", 1),
#     }
#     fake_tasks_db.append(new_task)
#     return new_task


# # ── PUT /tasks/{task_id} ────────────────────────────────────────────
# @router.put("/{task_id}", summary="Fully update a task")
# async def update_task(
#     task_id: int = Path(..., ge=1),
#     task: dict = None,
# ):
#     """
#     Full update — replaces all fields of the task.
#     """
#     index = next((i for i, t in enumerate(fake_tasks_db) if t["id"] == task_id), None)
#     if index is None:
#         raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

#     updated = {
#         "id": task_id,
#         "title": task.get("title", "Untitled"),
#         "status": task.get("status", "pending"),
#         "priority": task.get("priority", "medium"),
#         "project_id": task.get("project_id", 1),
#     }
#     fake_tasks_db[index] = updated
#     return updated


# # ── PATCH /tasks/{task_id} ──────────────────────────────────────────
# @router.patch("/{task_id}", summary="Partially update a task")
# async def partial_update_task(
#     task_id: int = Path(..., ge=1),
#     task: dict = None,
# ):
#     """
#     Partial update — only updates the fields provided.
#     Fields not included in the body remain unchanged.
#     """
#     index = next((i for i, t in enumerate(fake_tasks_db) if t["id"] == task_id), None)
#     if index is None:
#         raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

#     existing = fake_tasks_db[index]
#     # Only update keys that were actually sent
#     for key, value in task.items():
#         if key != "id":  # never allow overwriting the ID
#             existing[key] = value

#     fake_tasks_db[index] = existing
#     return existing


# # ── DELETE /tasks/{task_id} ─────────────────────────────────────────
# @router.delete("/{task_id}", status_code=204, summary="Delete a task")
# async def delete_task(
#     task_id: int = Path(..., ge=1),
# ):
#     """
#     Delete a task by ID.
#     Returns 204 No Content on success.
#     """
#     index = next((i for i, t in enumerate(fake_tasks_db) if t["id"] == task_id), None)
#     if index is None:
#         raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

#     fake_tasks_db.pop(index)
#     return None  # 204 = no response body





































from fastapi import APIRouter, HTTPException, Query, Path, Body, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime
import asyncio

from app.schemas.task import TaskCreate, TaskUpdate, TaskOut, TaskListResponse
from app.schemas.enums import TaskStatus, TaskPriority

from app.schemas.common import SuccessResponse
from app.utils.errors import raise_not_found, raise_bad_request

from app.utils.background import log_task_created, log_task_deleted, log_task_updated, notify_assignee

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

# Fake DB — now using proper dicts that match TaskOut shape
fake_tasks_db = [
    {
        "id": 1, "title": "Set up FastAPI project", "description": "Initialize project structure",
        "status": "done", "priority": "high", "project_id": 1, "assigned_to": None,
        "due_date": None, "created_at": datetime.now(), "updated_at": datetime.now(),
    },
    {
        "id": 2, "title": "Design database schema", "description": "ERD and table design",
        "status": "in_progress", "priority": "high", "project_id": 1, "assigned_to": 1,
        "due_date": datetime(2026, 4, 1), "created_at": datetime.now(), "updated_at": datetime.now(),
    },
    {
        "id": 3, "title": "Write authentication logic", "description": None,
        "status": "pending", "priority": "medium", "project_id": 1, "assigned_to": None,
        "due_date": None, "created_at": datetime.now(), "updated_at": datetime.now(),
    },
]

# ── GET /tasks/ ──────────────────────────────────────────────────────
@router.get(
    "/",
    response_model=TaskListResponse,
    summary="Get all tasks",
    responses={400: {"description": "Invalid filter value"}},  # ← from old
)
async def get_tasks(
    skip: int = Query(default=0, ge=0, description="Records to skip"),                          # ← from old
    limit: int = Query(default=10, ge=1, le=100, description="Max records to return"),          # ← from old
    status: Optional[TaskStatus] = Query(default=None, description="Filter by status"),         # ← from old
    priority: Optional[TaskPriority] = Query(default=None, description="Filter by priority"),   # ← from old
    project_id: Optional[int] = Query(default=None, ge=1, description="Filter by project"),    # ← from old
):
    async def filter_by_status(tasks, s):
        await asyncio.sleep(0)
        return [t for t in tasks if t["status"] == s.value] if s else tasks

    async def filter_by_priority(tasks, p):
        await asyncio.sleep(0)
        return [t for t in tasks if t["priority"] == p.value] if p else tasks

    status_filtered, priority_filtered = await asyncio.gather(
        filter_by_status(fake_tasks_db, status),
        filter_by_priority(fake_tasks_db, priority),
    )

    priority_ids = {t["id"] for t in priority_filtered}
    results = [t for t in status_filtered if t["id"] in priority_ids]

    if project_id:
        results = [t for t in results if t["project_id"] == project_id]

    total = len(results)
    return TaskListResponse(total=total, skip=skip, limit=limit, data=results[skip: skip + limit])

# ── GET /tasks/stats ─────────────────────────────────────────────────
@router.get(
    "/stats",
    summary="Get task statistics",
    response_description="Breakdown of tasks by status and priority",
)
async def get_task_stats():
    # Simulate two concurrent DB aggregation queries
    async def count_by_status():
        await asyncio.sleep(0)
        counts = {}
        for task in fake_tasks_db:
            counts[task["status"]] = counts.get(task["status"], 0) + 1
        return counts

    async def count_by_priority():
        await asyncio.sleep(0)
        counts = {}
        for task in fake_tasks_db:
            counts[task["priority"]] = counts.get(task["priority"], 0) + 1
        return counts

    # Both run concurrently
    by_status, by_priority = await asyncio.gather(
        count_by_status(),
        count_by_priority(),
    )

    return {
        "total": len(fake_tasks_db),
        "by_status": by_status,
        "by_priority": by_priority,
    }


# ── GET /tasks/{task_id} ─────────────────────────────────────────────
@router.get(
    "/{task_id}",
    response_model=TaskOut,
    response_model_exclude_unset=True,
    summary="Get a single task",
    responses={
        404: {"description": "Task not found"},
    },
)
async def get_task(task_id: int = Path(..., ge=1, description="Task ID")):
    task = next((t for t in fake_tasks_db if t["id"] == task_id), None)
    if not task:
        raise_not_found("Task", task_id)
    return task


# ── POST /tasks/ ─────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=TaskOut,
    status_code=201,
    summary="Create a new task",
    responses={
        201: {"description": "Task created successfully"},
        409: {"description": "Duplicate task title in same project"},
    },
)
async def create_task(task: TaskCreate,  background_tasks: BackgroundTasks):
    # Business logic validation — check for duplicate title in same project
    duplicate = next(
        (t for t in fake_tasks_db
         if t["title"].lower() == task.title.lower()
         and t["project_id"] == task.project_id),
        None,
    )
    if duplicate:
        raise_bad_request(
            message=f"A task named '{task.title}' already exists in this project",
            field="title",
        )

    new_task = {
        "id": len(fake_tasks_db) + 1,
        **task.model_dump(),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    fake_tasks_db.append(new_task)

    # Fire and forget — these run AFTER response is sent
    background_tasks.add_task(log_task_created, new_task["id"], new_task["title"], user_id=1)
    if new_task.get("assigned_to"):
        background_tasks.add_task(
            notify_assignee,
            new_task["id"],
            new_task["assigned_to"],
            f"You have been assigned to task: {new_task['title']}",
        )

    return new_task


# ── PUT /tasks/{task_id} ─────────────────────────────────────────────
@router.put(
    "/{task_id}",
    response_model=TaskOut,
    summary="Fully update a task",
    responses={404: {"description": "Task not found"}},
)
async def update_task(
    task_id: int = Path(..., ge=1),
    task: TaskCreate = Body(...),
    background_tasks: BackgroundTasks = None,
):
    index = next((i for i, t in enumerate(fake_tasks_db) if t["id"] == task_id), None)
    if index is None:
        raise_not_found("Task", task_id)

    updated = {
        "id": task_id,
        **task.model_dump(),
        "created_at": fake_tasks_db[index]["created_at"],
        "updated_at": datetime.now(),
    }
    fake_tasks_db[index] = updated

    background_tasks.add_task(log_task_updated, task_id, task.model_dump(), user_id=1)

    return updated

# ── PATCH /tasks/{task_id} ───────────────────────────────────────────
@router.patch(
    "/{task_id}",
    response_model=TaskOut,
    response_model_exclude_unset=True,
    summary="Partially update a task",
    responses={404: {"description": "Task not found"}},
)
async def partial_update_task(
    task_id: int = Path(..., ge=1),
    task: TaskUpdate = Body(...),
    background_tasks: BackgroundTasks = None,
):
    index = next((i for i, t in enumerate(fake_tasks_db) if t["id"] == task_id), None)
    if index is None:
        raise_not_found("Task", task_id)

    updates = task.model_dump(exclude_unset=True)
    if not updates:
        raise_bad_request("No fields provided to update")

    fake_tasks_db[index].update(updates)
    fake_tasks_db[index]["updated_at"] = datetime.now()

    background_tasks.add_task(log_task_updated, task_id, updates, user_id=1)
    return fake_tasks_db[index]

# ── DELETE /tasks/{task_id} ──────────────────────────────────────────
@router.delete(
    "/{task_id}",
    status_code=204,
    summary="Delete a task",
    responses={
        204: {"description": "Task deleted successfully"},
        404: {"description": "Task not found"},
    },
)
async def delete_task(
    task_id: int = Path(..., ge=1),
    background_tasks: BackgroundTasks = None,
    ):
    index = next((i for i, t in enumerate(fake_tasks_db) if t["id"] == task_id), None)
    if index is None:
        raise_not_found("Task", task_id)

    fake_tasks_db.pop(index)
    background_tasks.add_task(log_task_deleted, task_id, user_id=1)
    return None
