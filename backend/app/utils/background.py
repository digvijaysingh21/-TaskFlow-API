import asyncio
from datetime import datetime


# Note: background task functions can be sync OR async
# FastAPI handles both correctly

def log_task_created(task_id: int, title: str, user_id: int):
    """
    Log when a task is created.
    In production: write to a logging service or DB audit table.
    """
    print(f"[{datetime.now()}] TASK_CREATED | id={task_id} | title={title!r} | by user={user_id}")


def log_task_updated(task_id: int, changes: dict, user_id: int):
    """
    Log what fields changed on a task update.
    """
    print(f"[{datetime.now()}] TASK_UPDATED | id={task_id} | changes={changes} | by user={user_id}")


def log_task_deleted(task_id: int, user_id: int):
    """
    Log when a task is deleted.
    """
    print(f"[{datetime.now()}] TASK_DELETED | id={task_id} | by user={user_id}")


async def notify_assignee(task_id: int, assignee_id: int, message: str):
    """
    Async background task — notify the user assigned to a task.
    In production: send a push notification, email, or Slack message.
    Simulated with asyncio.sleep to mimic a real async notification call.
    """
    await asyncio.sleep(0.5)  # simulate async notification call
    print(f"[{datetime.now()}] NOTIFY | user={assignee_id} | task={task_id} | msg={message!r}")