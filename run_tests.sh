#!/bin/bash
set -e

echo "Starting database container..."
docker compose up -d db

echo "Building web service..."
docker compose build web

echo "Running tests..."
docker compose run --rm web pytest -v

# Store the exit code
exit_code=$?

echo "Cleaning up..."
docker compose down

# Exit with the test exit code
exit $exit_code
