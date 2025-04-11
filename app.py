"""Flask application that serves endpoints and tracks their access counts."""

import os
from datetime import UTC, datetime

from flask import Flask, Response, jsonify
from flask.typing import ResponseReturnValue
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

app = Flask(__name__)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/postgres",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    "flask_http_request_total",
    "Total HTTP Requests",
    ["endpoint"],
)


class EndpointAccess(db.Model):  # type: ignore[name-defined]
    """Model to track endpoint access counts."""

    __tablename__ = "endpoint_access"

    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(255), nullable=False)
    access_count = db.Column(db.Integer, default=0)
    last_accessed = db.Column(db.DateTime, default=datetime.now(UTC))

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
    access.last_accessed = datetime.now(UTC)
    db.session.commit()

    # Increment Prometheus counter
    REQUEST_COUNT.labels(endpoint=endpoint).inc()

    return access.access_count or 0  # Ensure we always return an int


@app.route("/", methods=["GET"])  # type: ignore[misc]
def hello() -> ResponseReturnValue:
    """Return a greeting message in JSON format and track the access.

    Returns:
        ResponseReturnValue: A dictionary containing the greeting message.
    """
    count = track_access("/")
    return jsonify(
        {
            "message": "Hello, World!",
            "access_count": count,
        },
    )


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


@app.route("/health", methods=["GET"])  # type: ignore[misc]
def health() -> ResponseReturnValue:
    """Health check endpoint for Kubernetes liveness probe.

    Returns:
        ResponseReturnValue: A simple health status message.
    """
    return jsonify({"status": "ok"})


@app.route("/metrics", methods=["GET"])  # type: ignore[misc]
def metrics() -> Response:
    """Metrics endpoint for Prometheus scraping.

    Returns:
        Response: Prometheus metrics in the expected format.
    """
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


# Create database tables
# In Flask, database operations need to be performed within an application context
# The app_context() creates a context where Flask knows which application is active
# This is necessary because Flask applications can have multiple databases or
# configurations db.create_all() uses the SQLAlchemy models defined above to create
# all database tables if they don't already exist.
# This ensures the database schema is properly set up before the application starts
# handling requests.
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)  # noqa: S104 - Binding to all interfaces is intentional for container environments
