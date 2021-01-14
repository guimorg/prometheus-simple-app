import time

from flask import request, Flask

from flask.wrappers import Response

from prometheus_client import Counter, Histogram


REQUEST_COUNT = Counter(
    name="http_request_count",
    documentation="Application Request Count",
    labelnames=["app_name", "method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    name="http_request_latency_seconds",
    documentation="Request Latency",
    labelnames=["app_name", "endpoint"]
)


def start_timer():
    request._prometheus_metrics_request_start_time = time.perf_counter()


def stop_timer(response):
    request_latency = time.perf_counter() - request._prometheus_metrics_request_start_time
    REQUEST_LATENCY.labels(
        app_name="webapp",
        endpoint=request.path
    ).observe(request_latency)
    return response


def record_request_data(response):
    """Simple count metric for method, endpoint and http_status"""
    REQUEST_COUNT.labels(
        app_name="webapp",
        method=request.method,
        endpoint=request.path,
        http_status=response.status_code
    ).inc()
    return response


def setup_metrics(app):
    """Adds simple middleware functions to Flask app.

    In order to setup the Prometheus metrics we create simple middleware
    functions to generate two simple metrics: latency and count.
    """
    app.before_request(start_timer)
    app.after_request(record_request_data)
    app.after_request(stop_timer)
