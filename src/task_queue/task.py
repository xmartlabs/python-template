import time

from src.task_queue.celery_worker import celery_worker


@celery_worker.task(name="add")
def add(delay: int, x: int, y: int) -> int:
    time.sleep(delay)
    return x + y
