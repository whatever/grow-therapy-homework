import argparse

from .app import WikipediaCounterApp
from .routes import flask_app


def main():
    """
    Run the equivalent of gunicorn wikipedia_counter.cli:flask_app ...
    This serves the wikipeida counter api.
    """

    parser = argparse.ArgumentParser(description="knock*knock")
    parser.add_argument("--host", default="0.0.0.0", help="host address")
    parser.add_argument("--port", default=8181, help="port number")
    parser.add_argument("--workers", default=2, help="number of workers")
    args = parser.parse_args()

    options = {
        "bind": f"{args.host}:{args.port}",
        "workers": args.workers,
    }

    WikipediaCounterApp(flask_app, options).run()
