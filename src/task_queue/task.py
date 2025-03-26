import time

from src.task_queue.celery_worker import celery_worker


# A simple example of a Celery task.
# In real-world scenarios, you should implement the task logic here.
# Don't forget to add the task name and then add the task to the autodiscover_tasks method in
# the src/task_queue/celery_worker.py file.
# In case you need to create more task files to organize your tasks, you can add them to the
# autodiscover_tasks method as well.
@celery_worker.task(name="add")
def add(delay: int, x: int, y: int) -> int:
    time.sleep(delay)
    return x + y
