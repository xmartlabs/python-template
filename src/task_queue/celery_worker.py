from celery import Celery

from src.core.config import settings

celery_worker = Celery(
    "task_queue",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_worker.autodiscover_tasks(["src.task_queue.task"])
