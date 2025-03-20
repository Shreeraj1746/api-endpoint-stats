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

- `GET http://localhost:9999/` - Returns a welcome message and access count
- `GET http://localhost:9999/stats` - Shows access counts for all endpoints

Each time you access an endpoint, its access count is incremented. For example:
1. Visit `http://localhost:9999/` in your browser - This will return a welcome message and increment the root endpoint's access count
2. Visit `http://localhost:9999/stats` - This will show you how many times each endpoint has been accessed

Example response from `/`:
```json
{
  "message": "Hello, World!",
  "access_count": 1
}
```

Example response from `/stats`:
```json
{
  "stats": {
    "/": 1,
    "/stats": 1
  },
  "access_count": 1
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
- **Ruff** (v0.3.3) - All-in-one Python linter and formatter
  - Code formatting (similar to Black)
  - Import sorting (similar to isort)
  - Code style checking (similar to flake8)
  - Static type checking (similar to mypy)
  - And many more checks!

### Testing Tools
- **pytest** (v8.0.2) - Testing framework
- **pytest-cov** (v4.1.0) - Test coverage
- **pytest-flask** (v1.3.0) - Flask testing utilities

### Git Hooks
- **pre-commit** (v3.6.2) - Git hook framework
- **commitizen** (v3.10.0) - Commit message formatting

To install the hooks:
```bash
pre-commit install  # Install pre-commit hooks
pre-commit install --hook-type pre-push  # Install pre-push hooks
```

### Pre-commit Checks
The following checks are performed automatically before each commit:
- Code formatting and linting (Ruff)
- YAML validation
- JSON validation
- Merge conflict detection
- Private key detection
- Commit message formatting (commitizen)

Additionally, all unit tests are automatically run in Docker before each push to ensure code quality. The hook ensures that:
1. The database container is up and running
2. The web service is built with the latest changes
3. All tests pass with coverage report

### Running Code Quality Checks

You can run Ruff manually to check and fix code quality issues:

```bash
# Check code quality
docker compose run --rm web ruff check .

# Fix issues automatically
docker compose run --rm web ruff check . --fix

# Format code
docker compose run --rm web ruff format .
```

To run all pre-commit checks in Docker:
```bash
docker compose run --rm web pre-commit run --all-files
```

## Notes

- The application uses PostgreSQL 15 for storing endpoint access counts
- The database is configured with health checks to ensure proper startup order
- All dependencies are managed through Docker, no local Python installation required
- Pre-commit hooks ensure consistent code quality and formatting
- The project uses conventional commits for commit messages
