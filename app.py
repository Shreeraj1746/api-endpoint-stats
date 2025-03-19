"""Simple Flask application that serves a Hello World JSON response."""

from flask import Flask
from flask.typing import ResponseReturnValue

app = Flask(__name__)


@app.route("/", methods=["GET"])  # type: ignore[misc]
def hello() -> ResponseReturnValue:
    """Return a greeting message in JSON format.

    Returns:
        ResponseReturnValue: A dictionary containing the greeting message.
    """
    return {"message": "Hello from containerized Python application!"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)
