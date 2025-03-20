"""Flask application that serves endpoints and tracks their access counts."""

import os
from datetime import datetime

from flask import Flask, jsonify
from flask.typing import ResponseReturnValue
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class EndpointAccess(db.Model):  # type: ignore[name-defined]
    """Model to track endpoint access counts."""

    __tablename__ = "endpoint_access"

    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(255), nullable=False)
    access_count = db.Column(db.Integer, default=0)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """Return string representation of the model."""
        return f"<EndpointAccess {self.endpoint}: {self.access_count}>"


def track_access(endpoint: str) -> int:
    """Track access to an endpoint by incrementing its count.

    Args:
        endpoint: The endpoint path being accessed.

    Returns:
        int: The updated access count for the endpoint.
    """
    access = EndpointAccess.query.filter_by(endpoint=endpoint).first()
    if access is None:
        access = EndpointAccess(endpoint=endpoint, access_count=0)
        db.session.add(access)
        db.session.commit()  # Commit to ensure access_count is initialized
    if access.access_count is None:
        access.access_count = 0
    access.access_count = access.access_count + 1
    access.last_accessed = datetime.utcnow()
    db.session.commit()
    return access.access_count or 0  # Ensure we always return an int


@app.route("/", methods=["GET"])  # type: ignore[misc]
def hello() -> ResponseReturnValue:
    """Return a greeting message in JSON format and track the access.

    Returns:
        ResponseReturnValue: A dictionary containing the greeting message.
    """
    count = track_access("/")
    return jsonify({"message": "Hello, World!", "access_count": count})


@app.route("/stats", methods=["GET"])  # type: ignore[misc]
def stats() -> ResponseReturnValue:
    """Return endpoint access statistics.

    Returns:
        ResponseReturnValue: A dictionary containing endpoint access stats.
    """
    count = track_access("/stats")
    accesses = EndpointAccess.query.all()
    stats_data = {access.endpoint: access.access_count for access in accesses}
    return jsonify({"stats": stats_data, "access_count": count})


# Create database tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)
