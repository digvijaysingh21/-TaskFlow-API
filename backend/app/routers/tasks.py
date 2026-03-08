from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

# ── Fake in-memory DB (will be replaced with real DB in Session 6) ──
fake_tasks_db = [
    {"id": 1, "title": "Set up FastAPI project", "status": "done", "priority": "high", "project_id": 1},
    {"id": 2, "title": "Design database schema", "status": "in_progress", "priority": "high", "project_id": 1},
    {"id": 3, "title": "Write authentication logic", "status": "pending", "priority": "medium", "project_id": 1},
    {"id": 4, "title": "Add Redis caching", "status": "pending", "priority": "low", "project_id": 2},
    {"id": 5, "title": "Write tests", "status": "pending", "priority": "medium", "project_id": 2},
]

# ── GET /tasks ──────────────────────────────────────────────────────
@router.get("/", summary="Get all tasks")
async def get_tasks(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Max records to return"),
    status: Optional[str] = Query(default=None, description="Filter by status: pending, in_progress, done"),
    priority: Optional[str] = Query(default=None, description="Filter by priority: low, medium, high"),
    project_id: Optional[int] = Query(default=None, description="Filter by project ID"),
):
    """
    Retrieve all tasks with optional filters and pagination.
    - **skip**: how many records to skip (for pagination)
    - **limit**: max records to return
    - **status**: filter by task status
    - **priority**: filter by priority level
    - **project_id**: filter tasks belonging to a project
    """
    results = fake_tasks_db

    # Apply filters
    if status:
        results = [t for t in results if t["status"] == status]
    if priority:
        results = [t for t in results if t["priority"] == priority]
    if project_id:
        results = [t for t in results if t["project_id"] == project_id]

    # Apply pagination
    total = len(results)
    results = results[skip : skip + limit]

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": results,
    }


# ── GET /tasks/stats ────────────────────────────────────────────────
# IMPORTANT: this must come BEFORE /tasks/{task_id}
@router.get("/stats", summary="Get task statistics")
async def get_task_stats():
    """
    Returns a count breakdown of tasks by status and priority.
    """
    stats = {
        "total": len(fake_tasks_db),
        "by_status": {},
        "by_priority": {},
    }

    for task in fake_tasks_db:
        # Count by status
        s = task["status"]
        stats["by_status"][s] = stats["by_status"].get(s, 0) + 1

        # Count by priority
        p = task["priority"]
        stats["by_priority"][p] = stats["by_priority"].get(p, 0) + 1

    return stats


# ── GET /tasks/{task_id} ────────────────────────────────────────────
@router.get("/{task_id}", summary="Get a single task")
async def get_task(
    task_id: int = Path(..., ge=1, description="The ID of the task to retrieve"),
):
    """
    Retrieve a single task by its ID.
    Raises 404 if not found.
    """
    task = next((t for t in fake_tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


# ── POST /tasks ─────────────────────────────────────────────────────
@router.post("/", status_code=201, summary="Create a new task")
async def create_task(task: dict):
    """
    Create a new task.
    Requires: title, status, priority, project_id
    (We will replace `dict` with a proper Pydantic schema in Session 3)
    """
    new_task = {
        "id": len(fake_tasks_db) + 1,
        "title": task.get("title", "Untitled"),
        "status": task.get("status", "pending"),
        "priority": task.get("priority", "medium"),
        "project_id": task.get("project_id", 1),
    }
    fake_tasks_db.append(new_task)
    return new_task


# ── PUT /tasks/{task_id} ────────────────────────────────────────────
@router.put("/{task_id}", summary="Fully update a task")
async def update_task(
    task_id: int = Path(..., ge=1),
    task: dict = None,
):
    """
    Full update — replaces all fields of the task.
    """
    index = next((i for i, t in enumerate(fake_tasks_db) if t["id"] == task_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    updated = {
        "id": task_id,
        "title": task.get("title", "Untitled"),
        "status": task.get("status", "pending"),
        "priority": task.get("priority", "medium"),
        "project_id": task.get("project_id", 1),
    }
    fake_tasks_db[index] = updated
    return updated


# ── PATCH /tasks/{task_id} ──────────────────────────────────────────
@router.patch("/{task_id}", summary="Partially update a task")
async def partial_update_task(
    task_id: int = Path(..., ge=1),
    task: dict = None,
):
    """
    Partial update — only updates the fields provided.
    Fields not included in the body remain unchanged.
    """
    index = next((i for i, t in enumerate(fake_tasks_db) if t["id"] == task_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    existing = fake_tasks_db[index]
    # Only update keys that were actually sent
    for key, value in task.items():
        if key != "id":  # never allow overwriting the ID
            existing[key] = value

    fake_tasks_db[index] = existing
    return existing


# ── DELETE /tasks/{task_id} ─────────────────────────────────────────
@router.delete("/{task_id}", status_code=204, summary="Delete a task")
async def delete_task(
    task_id: int = Path(..., ge=1),
):
    """
    Delete a task by ID.
    Returns 204 No Content on success.
    """
    index = next((i for i, t in enumerate(fake_tasks_db) if t["id"] == task_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    fake_tasks_db.pop(index)
    return None  # 204 = no response body