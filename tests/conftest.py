"""Pytest configuration and fixtures."""

from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from app import EndpointAccess
from app import app as flask_app
from app import db as flask_db


@pytest.fixture(autouse=True)  # type: ignore[misc]
def app() -> Flask:
    """Create and configure a test Flask application instance.

    Returns:
        Flask: A Flask application instance configured for testing.
    """
    # Use SQLite for testing
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
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
    return app.test_client()


@pytest.fixture(autouse=True)  # type: ignore[misc]
def db(app: Flask) -> Generator[SQLAlchemy, None, None]:
    """Create and configure the database for testing.

    Args:
        app: The Flask application fixture.

    Returns:
        SQLAlchemy: The database instance.
    """
    with app.app_context():
        flask_db.create_all()
        try:
            yield flask_db
        finally:
            # Clean up all data
            flask_db.session.query(EndpointAccess).delete()
            flask_db.session.commit()
            flask_db.session.remove()
            flask_db.drop_all()
