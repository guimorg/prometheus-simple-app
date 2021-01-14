import prometheus_client

from flask import Flask

from werkzeug.middleware.dispatcher import DispatcherMiddleware

from app.helpers.middleware import setup_metrics


def index():
    return "Hello World!"


def cpu():
    """Simple function to simulate a cpu-intensive task"""
    for i in range(10000):
        i ** i  # Exponential operations are REALLY cpu-intensive
    return "CPU-intensive task is complete!"


def memory():
    """Simple function to simulate a memory-intensive task"""
    d = {}
    for i in range(10000000):
        i = str(i)
        i += "xyz"
        d[i] = i
    return "Memory-intensive task is complete!"


def create_app():
    main_app = Flask(__name__)

    main_app.add_url_rule("/", "index", index)
    main_app.add_url_rule("/cpu", "cpu", cpu)
    main_app.add_url_rule("/memory", "memory", memory)
    setup_metrics(main_app)

    app = DispatcherMiddleware(
        app=main_app.wsgi_app,
        mounts={"/metrics": prometheus_client.make_wsgi_app()}
    )

    return app
