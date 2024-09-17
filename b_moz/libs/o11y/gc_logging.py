import logging


def get_log_formatter():
    from pythonjsonlogger import jsonlogger

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(message)s %(otelTraceID)s %(otelSpanID)s %(otelTraceSampled)s",
        rename_fields={
            "levelname": "severity",
            "asctime": "timestamp",
            "otelTraceID": "logging.googleapis.com/trace",
            "otelSpanID": "logging.googleapis.com/spanId",
            "otelTraceSampled": "logging.googleapis.com/trace_sampled",
        },
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    return formatter


def get_log_handler():
    logHandler = logging.StreamHandler()
    formatter = get_log_formatter()
    logHandler.setFormatter(formatter)
    return logHandler
