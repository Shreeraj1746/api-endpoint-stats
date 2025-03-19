"""Test cases for application routes."""

from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy


def test_hello_endpoint(client: FlaskClient) -> None:
    """Test the root endpoint returns the expected message.

    Args:
        client: The test client fixture.
    """
    response = client.get("/")
    assert response.status_code == 200
    expected_msg = "Hello from containerized Python application!"
    assert response.json == {"message": expected_msg}


def test_stats_endpoint(client: FlaskClient, db: SQLAlchemy) -> None:
    """Test the stats endpoint returns correct access counts.

    Args:
        client: The test client fixture.
        db: The database fixture.
    """
    # First request to root endpoint
    client.get("/")

    # Check stats
    response = client.get("/stats")
    assert response.status_code == 200

    stats = response.json["endpoints"]
    assert len(stats) == 2  # Two endpoints accessed

    # Find root endpoint stats
    root_stats = next(s for s in stats if s["endpoint"] == "/")
    assert root_stats["access_count"] == 1

    # Find stats endpoint stats
    stats_stats = next(s for s in stats if s["endpoint"] == "/stats")
    assert stats_stats["access_count"] == 1


def test_multiple_accesses(client: FlaskClient, db: SQLAlchemy) -> None:
    """Test that multiple accesses to endpoints are correctly counted.

    Args:
        client: The test client fixture.
        db: The database fixture.
    """
    # Access root endpoint multiple times
    client.get("/")
    client.get("/")
    client.get("/")

    # Check stats
    response = client.get("/stats")
    assert response.status_code == 200

    stats = response.json["endpoints"]
    root_stats = next(s for s in stats if s["endpoint"] == "/")
    assert root_stats["access_count"] == 3

    stats_stats = next(s for s in stats if s["endpoint"] == "/stats")
    assert stats_stats["access_count"] == 1
