import os
from functools import wraps

from opentelemetry import trace

tracer = trace.get_tracer_provider().get_tracer(__name__)


def use_tracer():
    return os.environ.get("DISABLE_TRACING", None) is None


def tracing(func):
    if not use_tracer():
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        tracer_args = {
            "context": extract(request.headers),
            "kind": SpanKind.SERVER,
            "attributes": collect_request_attributes(request.environ),
        }
        with tracer.start_as_current_span(func.__name__, **tracer_args):
        """
        parent_span = trace.get_current_span()
        with tracer.start_as_current_span(
                name=func.__qualname__,
                links=[trace.Link(parent_span.get_span_context())]):
            return func(*args, **kwargs)

    return wrapper
