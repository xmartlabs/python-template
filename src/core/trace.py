import functools
from typing import Any, Callable

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from src.core.config import settings

# Configure OpenTelemetry
resource = Resource(attributes={"service.name": "python-template"})
tracer_provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(
    endpoint=settings.otel_exporter_otlp_endpoint, insecure=True
)
otlp_metric_exporter = OTLPMetricExporter(
    endpoint="http://otel-collector:4317", insecure=True
)
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)


def instrument(name: str = "request") -> Callable:
    """
    Decorator to instrument a method with OpenTelemetry tracing.
    Args:
        name (str): The name of the span.
    Returns:
        Callable: The decorated method.
    """

    def decorator(method: Callable) -> Callable:
        @functools.wraps(method)
        def wrapper(*args: Any, **kwargs: dict[Any, Any]) -> Any:
            tracer = tracer_provider.get_tracer(__name__)
            with tracer.start_as_current_span(name=name) as span:  # noqa: F841
                response = method(*args, **kwargs)
                return response

        return wrapper

    return decorator


#
