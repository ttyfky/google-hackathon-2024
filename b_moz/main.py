import logging
import os

from flask import Flask
from opentelemetry import trace
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from waitress import serve

import api


def setup_tracing():
    tracer_provider = TracerProvider(
        resource=Resource(
            attributes={
                "service.name": "b_moz",
            }
        )
    )

    if os.environ.get("K_SERVICE", ""):  # Cloud Run
        from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        processor = BatchSpanProcessor(CloudTraceSpanExporter())

        from opentelemetry.propagate import set_global_textmap
        from opentelemetry.propagators.cloud_trace_propagator import (
            CloudTraceFormatPropagator,
        )

        # Set the X-Cloud-Trace-Context header
        set_global_textmap(CloudTraceFormatPropagator())

    else:
        from opentelemetry.sdk.trace.export import (
            SimpleSpanProcessor,
            ConsoleSpanExporter,
        )

        processor = SimpleSpanProcessor(ConsoleSpanExporter())

    tracer_provider.add_span_processor(processor)
    trace.set_tracer_provider(tracer_provider)

    # Required to log traceId and spanId
    LoggingInstrumentor().instrument()


def create_app():
    flask_app = Flask(__name__)
    api.register(flask_app)
    return flask_app


if __name__ == "__main__":
    _logger = logging.getLogger(__name__)

    is_local = os.environ.get("IS_LOCAL") == "true"

    if is_local:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
        import google.cloud.logging

        client = google.cloud.logging.Client()
        client.setup_logging()
    setup_tracing()
    if is_local:
        create_app().run(host="", port=3000, debug=True)
    else:
        serve(create_app(), port=int(os.environ.get("PORT", 3000)))
