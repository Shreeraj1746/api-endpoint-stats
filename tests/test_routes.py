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
    assert response.json["message"] == "Hello, World!"
    assert "access_count" in response.json


def test_stats_endpoint(client: FlaskClient, db_session: SQLAlchemy) -> None:
    """Test the stats endpoint returns correct access counts.

    Args:
        client: The test client fixture.
        db_session: The database fixture.
    """
    # First request to root endpoint
    client.get("/")

    # Check stats
    response = client.get("/stats")
    assert response.status_code == 200

    stats = response.json["stats"]
    assert len(stats) == 2  # Two endpoints accessed

    # Check root endpoint stats
    assert stats["/"] == 1

    # Check stats endpoint stats
    assert stats["/stats"] == 1


def test_multiple_accesses(
    client: FlaskClient,
    db_session: SQLAlchemy,
) -> None:
    """Test that multiple accesses to endpoints are correctly counted.

    Args:
        client: The test client fixture.
        db_session: The database fixture.
    """
    # Access root endpoint multiple times
    client.get("/")
    client.get("/")
    client.get("/")

    # Check stats
    response = client.get("/stats")
    assert response.status_code == 200

    stats = response.json["stats"]
    assert stats["/"] == 3
    assert stats["/stats"] == 1
