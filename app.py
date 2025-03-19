"""Flask application that serves endpoints and tracks their access counts."""

import os
from datetime import datetime

from flask import Flask
from flask.typing import ResponseReturnValue
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
db_host = "postgresql://postgres:postgres@localhost:5432"
db_name = "endpoint_tracker"
default_db_url = f"{db_host}/{db_name}"
db_url = os.environ.get("DATABASE_URL", default_db_url)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
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


def track_endpoint_access(endpoint: str) -> None:
    """Track access to an endpoint by incrementing its count.

    Args:
        endpoint: The endpoint path being accessed.
    """
    access = EndpointAccess.query.filter_by(endpoint=endpoint).first()
    if access is None:
        access = EndpointAccess(endpoint=endpoint, access_count=1)
        db.session.add(access)
    else:
        access.access_count += 1
        access.last_accessed = datetime.utcnow()
    db.session.commit()


@app.route("/", methods=["GET"])  # type: ignore[misc]
def hello() -> ResponseReturnValue:
    """Return a greeting message in JSON format and track the access.

    Returns:
        ResponseReturnValue: A dictionary containing the greeting message.
    """
    track_endpoint_access("/")
    msg = "Hello from containerized Python application!"
    return {"message": msg}


@app.route("/stats", methods=["GET"])  # type: ignore[misc]
def stats() -> ResponseReturnValue:
    """Return endpoint access statistics.

    Returns:
        ResponseReturnValue: A dictionary containing endpoint access stats.
    """
    # Track access to /stats endpoint first
    track_endpoint_access("/stats")

    # Get stats after tracking this access
    stats_data = EndpointAccess.query.all()
    return {
        "endpoints": [
            {
                "endpoint": stat.endpoint,
                "access_count": stat.access_count,
                "last_accessed": stat.last_accessed.isoformat(),
            }
            for stat in stats_data
        ]
    }


with app.app_context():
    # Create tables on application startup
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)
