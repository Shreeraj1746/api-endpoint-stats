# Python Application with Docker

This is a basic Python application that can be containerized using Docker. The project includes a comprehensive set of development tools for code quality and consistency.

## Prerequisites

- Python 3.11+
- Docker

## Local Development

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up pre-commit hooks:
```bash
pre-commit install
pre-commit install --hook-type commit-msg  # For commit message validation
```

4. Run the application locally:
```bash
python app.py
```

## Docker Build and Run

1. Build the Docker image:
```bash
docker build -t python-app .
```

2. Run the container:
```bash
docker run -p 9999:9999 python-app
```

## Project Structure

- `app.py` - Main Python application
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration
- `.gitignore` - Git ignore rules
- `.pre-commit-config.yaml` - Pre-commit hooks configuration

## Development Tools

This project uses a comprehensive set of development tools to ensure code quality and consistency:

### Code Quality Tools
- **Black** (v24.2.0) - Code formatting
- **isort** (v5.13.2) - Import sorting
- **flake8** (v7.0.0) - Code style checking
- **flake8-docstrings** (v1.7.0) - Docstring checking
- **mypy** (v1.8.0) - Static type checking
- **types-all** (v1.0.0) - Type stubs for mypy

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

To run the checks manually:
```bash
pre-commit run --all-files
```

## API Endpoints

The application provides the following endpoints:

- `GET /` - Returns a welcome message
- `GET /health` - Health check endpoint
- `GET /api/status` - Application status information

## Notes

- The application runs on port 9999
- All development tools are automatically installed via `requirements.txt`
- Pre-commit hooks are automatically installed via `pre-commit install`
