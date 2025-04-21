from typing import Any

from celery import Celery
from celery.signals import task_postrun
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from src.core.config import settings
from src.core.trace import otlp_metric_exporter

# Create the celery worker
celery_worker = Celery(
    "task_queue",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# The autodiscover_tasks method will search for tasks in the specified modules
# In real-world schenarios, you should add more modules to this list
celery_worker.autodiscover_tasks(["src.task_queue.task"])

# OpenTelemetry setup
meter_provider = MeterProvider(metric_readers=[PeriodicExportingMetricReader(otlp_metric_exporter)])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter("celery_worker")

# Define a custom metric for task execution count
task_execution_counter = meter.create_counter(
    name="celery_task_executions",
    description="Counts the number of tasks executed by the Celery worker",
    unit="1",
)


# Signal handler to increment the counter after task execution
@task_postrun.connect
def task_postrun_handler(task: Any = None, **extras: Any) -> None:
    task_execution_counter.add(1, {"task_name": task.name})
