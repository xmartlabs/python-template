from uuid import UUID

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    x: int = Field(..., description="First number", examples=[4, 2])
    y: int = Field(..., description="Second number", examples=[2, 3])
    delay: int = Field(0, description="Delay in seconds", examples=[0, 5])


class Task(BaseModel):
    task_id: UUID = Field(
        ..., description="Task ID", examples=["7ce6afd6-bc66-4db1-bf31-b99e6daa0f11"]
    )


class TaskResult(Task):
    task_status: str = Field(
        ..., description="Task status", examples=["SUCCESS", "FAILURE"]
    )
    task_result: int | None = Field(None, description="Task result", examples=[6, None])
