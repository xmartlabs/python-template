from typing import Any

from celery.result import AsyncResult
from fastapi import APIRouter, Body, Path

from src.api.v1.schemas.task import Task, TaskCreate, TaskResult
from src.task_queue.task import add

router = APIRouter()


@router.post("/add", response_model=Task)
def add_task(payload: TaskCreate = Body(...)) -> Any:
    task = add.delay(payload.delay, payload.x, payload.y)
    return {"task_id": task.id}


@router.get("/task/{task_id}", response_model=TaskResult)
def get_task_result(task_id: str = Path(...)) -> Any:
    task: AsyncResult = add.AsyncResult(task_id)
    return {"task_id": task.id, "task_status": task.status, "task_result": task.result}
