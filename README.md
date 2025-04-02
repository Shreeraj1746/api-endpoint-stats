# Endpoint Statistics Application: Docker to Kubernetes Learning Journey

This project serves as a comprehensive learning experience for transitioning from Docker to Kubernetes. It starts with a simple Flask application running in Docker and guides you through transforming it into a production-ready Kubernetes deployment.

## Table of Contents

- [Project Overview](#project-overview)
- [Learning Journey](#learning-journey)
  - [Part 1: Docker Basics](#part-1-docker-basics)
  - [Part 2: Kubernetes Implementation](#part-2-kubernetes-implementation)
- [Development Tools](#development-tools)
- [Project Structure](#project-structure)
- [Additional Resources](#additional-resources)

## Project Overview

This is a Flask application that tracks endpoint access counts using PostgreSQL. While it's a simple application, it provides an excellent foundation for learning both Docker and Kubernetes concepts.

### Key Features

- Endpoint access tracking
- PostgreSQL data persistence
- Comprehensive test suite
- Production-ready development tools
- Detailed Kubernetes implementation guide

## Learning Journey

### Part 1: Docker Basics

Start by understanding the application running in Docker. This phase helps you grasp container concepts and Docker Compose basics.

#### Prerequisites

- Docker and Docker Compose

#### Running the Application

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

#### Testing

Run tests in a Docker container for consistent results:

```bash
# Run tests with normal output
docker compose run --rm web pytest -v

# Run tests with coverage report
docker compose run --rm web pytest -v --cov=app
```

#### Using the Application

The application runs on port 9999 and provides these endpoints:

- `GET http://localhost:9999/` - Welcome message and access count
- `GET http://localhost:9999/stats` - Access counts for all endpoints

Example responses:

```json
// GET /
{
  "message": "Hello, World!",
  "access_count": 1
}

// GET /stats
{
  "stats": {
    "/": 1,
    "/stats": 1
  },
  "access_count": 1
}
```

### Part 2: Kubernetes Implementation

Once you're comfortable with the Docker setup, follow the comprehensive guides in the `docs/` directory to transform this application into a Kubernetes deployment.

#### Prerequisites for Kubernetes

- A local Kubernetes cluster (Minikube, Kind, or Docker Desktop Kubernetes)
- `kubectl` command-line tool
- Basic understanding of Docker and container concepts
- Familiarity with YAML syntax

#### Documentation Structure

The `docs/` directory contains detailed guides organized into five phases:

- `impl_phase1.md`: Basic Infrastructure Setup
- `impl_phase2.md`: Monitoring and Observability
- `impl_phase3.md`: Security Implementation
- `impl_phase4.md`: Deployment Strategy
- `impl_phase5.md`: Monitoring and Maintenance
- `implementation_checklist.md`: Consolidated checklist for tracking progress

#### Learning Approach

1. Start with Phase 1 to understand basic Kubernetes concepts
2. Follow each phase sequentially as they build upon each other
3. Use the implementation checklist to track your progress
4. Experiment with different configurations and observe their effects

#### Tips for Learning Kubernetes

1. **Hands-on Practice**:
   - Create a new namespace for your learning environment
   - Try different configurations and observe their effects
   - Use `kubectl describe` and `kubectl logs` to understand what's happening
   - Experiment with scaling, updates, and rollbacks

2. **Debugging Tips**:
   - Use `kubectl get events` to see what's happening in your cluster
   - Check pod logs with `kubectl logs <pod-name>`
   - Use `kubectl describe` to get detailed information about resources
   - Enable verbose logging with `kubectl --v=6` for more details

3. **Best Practices**:
   - Always use namespaces to isolate your learning environment
   - Clean up resources when you're done to avoid cluster clutter
   - Use `kubectl apply -f` instead of `kubectl create` for idempotency
   - Take notes on what works and what doesn't

4. **Common Pitfalls to Avoid**:
   - Don't forget to set resource limits
   - Always use health checks
   - Implement proper security contexts
   - Use secrets for sensitive data
   - Consider scalability in your design

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
- `docs/` - Kubernetes implementation guides and documentation

## Additional Resources

### Kubernetes Learning Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Kubernetes Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Patterns](https://k8spatterns.io/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)

### Project Notes

- The application uses PostgreSQL 15 for storing endpoint access counts
- The database is configured with health checks to ensure proper startup order
- All dependencies are managed through Docker, no local Python installation required
- Pre-commit hooks ensure consistent code quality and formatting
- The project uses conventional commits for commit messages

Remember: This project is designed as a learning journey from Docker to Kubernetes. Take your time to understand each concept before moving to the next phase. The documentation in the `docs/` directory is designed to guide you through this journey step by step.
