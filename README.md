# Python Application with Docker

This is a Flask application that tracks endpoint access counts using PostgreSQL. The project includes a comprehensive set of development tools for code quality and consistency.

## Prerequisites

- Docker and Docker Compose

## Docker Compose Environment

1. Start the application and database:
```bash
docker compose up -d
```

2. Check the logs:
```bash
docker compose logs -f
```

3. Stop and clean up:
```bash
docker compose down
```

## Running Tests

The tests run in a Docker container to ensure a consistent environment across all development machines.

1. Run the tests:
```bash
# Run tests with normal output
docker compose run --rm web pytest -v

# Run tests with coverage report
docker compose run --rm web pytest -v --cov=app
```

2. Clean up after testing:
```bash
docker compose down
```

## Using the Application

The application runs on port 9999 and provides the following endpoints:

- `GET http://localhost:9999/` - Returns a welcome message
- `GET http://localhost:9999/stats` - Shows access counts for all endpoints

Each time you access an endpoint, its access count is incremented. For example:
1. Visit `http://localhost:9999/` in your browser - This will return a welcome message and increment the root endpoint's access count
2. Visit `http://localhost:9999/stats` - This will show you how many times each endpoint has been accessed

Example response from `/stats`:
```json
{
  "endpoints": [
    {
      "endpoint": "/",
      "access_count": 1,
      "last_accessed": "2025-03-19T07:58:37.766141"
    },
    {
      "endpoint": "/stats",
      "access_count": 1,
      "last_accessed": "2025-03-19T07:58:37.766141"
    }
  ]
}
```

## Project Structure

- `app.py` - Main Flask application with endpoint tracking
- `requirements.txt` - Python dependencies
- `requirements-test.txt` - Test dependencies
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Docker Compose configuration
- `tests/` - Test files
- `.gitignore` - Git ignore rules
- `.pre-commit-config.yaml` - Pre-commit hooks configuration
- `pyproject.toml` - Python tool configurations

## Development Tools

This project uses a comprehensive set of development tools to ensure code quality and consistency:

### Code Quality Tools
- **Black** (v24.2.0) - Code formatting
- **isort** (v5.13.2) - Import sorting
- **flake8** (v7.0.0) - Code style checking
- **flake8-docstrings** (v1.7.0) - Docstring checking
- **mypy** (v1.9.0) - Static type checking

### Testing Tools
- **pytest** (v8.0.2) - Testing framework
- **pytest-cov** (v4.1.0) - Test coverage
- **pytest-flask** (v1.3.0) - Flask testing utilities

### Git Hooks
- **pre-commit** (v3.6.2) - Git hook framework
- **commitizen** (v3.10.0) - Commit message formatting

### Pre-commit Checks
The following checks are performed automatically before each commit:
- Code formatting (Black)
- Import sorting (isort)
- Code style (flake8)
- Type checking (mypy)
- YAML validation
- JSON validation
- Merge conflict detection
- Private key detection
- Commit message formatting (commitizen)

To run the checks in Docker:
```bash
docker compose run --rm web pre-commit run --all-files
```

## Notes

- The application uses PostgreSQL for storing endpoint access counts
- Tests use SQLite in-memory database for faster execution
- All dependencies are managed through Docker, no local Python installation required
- Pre-commit hooks can be run in Docker to ensure consistent code quality checks
