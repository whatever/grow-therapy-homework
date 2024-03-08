from flask import Flask, request


flask_app = Flask(__name__)


@flask_app.route("/api/1/")
def womp():
    return {"status": "ok"}, 200


@flask_app.route("/api/1/count")
def count():
    return {"count": 420}, 200
