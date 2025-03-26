from celery import Celery

from src.core.config import settings

# Create the celery worker
celery_worker = Celery(
    "task_queue",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# The autodiscover_tasks method will search for tasks in the specified modules
# In real-world schenarios, you should add more modules to this list
celery_worker.autodiscover_tasks(["src.task_queue.task"])
