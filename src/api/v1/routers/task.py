from typing import Any

from celery.result import AsyncResult
from fastapi import APIRouter

from src.task_queue.task import add

router = APIRouter()


@router.post("/add")
def add_task(x: int, y: int, delay: int = 0) -> Any:
    task = add.delay(delay, x, y)
    return {"task_id": task.id}


@router.get("/task/{task_id}")
def get_task_result(task_id: str) -> Any:
    task: AsyncResult = add.AsyncResult(task_id)
    return {"task_id": task.id, "task_status": task.status, "task_result": task.result}
