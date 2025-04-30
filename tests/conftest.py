"""Pytest configuration and fixtures."""

from collections.abc import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from app import (
    EndpointAccess,
    app as flask_app,
    db,
)


@pytest.fixture(autouse=True)  # type: ignore[misc]
def app() -> Flask:
    """Create and configure a test Flask application instance.

    Returns:
        Flask: A Flask application instance configured for testing.
    """
    # Use PostgreSQL for testing
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:postgres@db:5432/endpoint_stats"
    )
    flask_app.config["TESTING"] = True

    return flask_app


@pytest.fixture  # type: ignore[misc]
def client(app: Flask) -> FlaskClient:
    """Create a test client for the Flask application.

    Args:
        app: The Flask application fixture.

    Returns:
        FlaskClient: A test client for making requests.
    """
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.query(EndpointAccess).delete()
        db.session.commit()


@pytest.fixture(autouse=True)  # type: ignore[misc]
def db_session(app: Flask) -> Generator[SQLAlchemy, None, None]:
    """Create and configure the database for testing.

    Args:
        app: The Flask application fixture.

    Returns:
        Generator[SQLAlchemy, None, None]: The database instance.
    """
    with app.app_context():
        db.create_all()
        try:
            yield db
        finally:
            # Clean up all data
            db.session.query(EndpointAccess).delete()
            db.session.commit()
            db.session.remove()
            db.drop_all()
