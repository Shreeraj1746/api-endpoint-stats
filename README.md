# Endpoint Statistics Application: Docker to Kubernetes Learning Journey

This project serves as a comprehensive learning experience for transitioning from Docker to Kubernetes. It starts with a simple Flask application running in Docker and guides you through transforming it into a production-ready Kubernetes deployment with monitoring and observability tools.

## Table of Contents

- [Project Overview](#project-overview)
- [Learning Journey](#learning-journey)
  - [Part 1: Docker Basics](#part-1-docker-basics)
  - [Part 2: Kubernetes Implementation](#part-2-kubernetes-implementation)
- [Development Tools](#development-tools)
- [Project Structure](#project-structure)
- [Additional Resources](#additional-resources)
- [Getting Started](#getting-started)

## Project Overview

This is a Flask application that tracks endpoint access counts using PostgreSQL. While it's a simple application, it provides an excellent foundation for learning both Docker and Kubernetes concepts. The project now includes a complete Kubernetes infrastructure with monitoring components.

### Key Features

- Endpoint access tracking
- PostgreSQL data persistence
- Redis caching
- Grafana and Prometheus monitoring
- Python-based dashboard checker
- Comprehensive test suite
- Production-ready development tools
- Detailed Kubernetes implementation guide
- Persistent volumes and storage management

### Current Status

The project has been fully migrated from a Docker-only setup to a Kubernetes infrastructure with monitoring and observability tools. Key components include:

- Flask API deployed as a Kubernetes service
- PostgreSQL with persistent storage
- Redis for caching
- Grafana for visualization
- Prometheus for metrics collection
- Python utility for dashboard management
- Complete YAML configurations for all Kubernetes resources
- Step-by-step implementation documentation

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

#### Implemented Kubernetes Components

The project now includes the following Kubernetes resources:

- **Namespace**: Dedicated namespace for the application
- **Flask API**: Deployment and service for the main application
- **PostgreSQL**: StatefulSet with persistent volume claims
- **Redis**: Deployment and service for caching
- **Ingress**: Rules for external access
- **Secrets**: Secure storage for sensitive information
- **Monitoring Stack**:
  - Prometheus for metrics collection
  - Grafana for visualization and dashboards
  - ConfigMaps for configuration
  - Persistent volumes for data storage

#### Python Dashboard Checker

The project includes a Python utility (`scripts/dashboard-checker.py`) that:

1. Checks if a specific dashboard exists in Grafana
2. Creates the dashboard if it doesn't exist
3. Uses Grafana API to interact with the monitoring system
4. Implements proper error handling and logging

This tool is useful for ensuring that monitoring dashboards are properly set up when deploying the application.

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

### Utility Scripts

- **dashboard-checker.py** - Python script for managing Grafana dashboards:
  - Checks for existing dashboards
  - Creates dashboards from JSON templates
  - Handles authentication securely
  - Provides detailed logging
  - Uses best practices for error handling

To run the dashboard checker:

```bash
# Make sure Grafana is running
python scripts/dashboard-checker.py
```

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
- `k8s/` - Kubernetes YAML configurations
  - `namespace.yaml` - Namespace definition
  - `flask-api.yaml` - Main application deployment
  - `postgres.yaml` - Database configuration
  - `redis.yml` - Redis cache configuration
  - `persistent-volumes.yaml` - Storage configuration
  - `secrets.yaml` - Secure credentials
  - `ingress.yaml` - External access rules
  - `monitoring/` - Monitoring configurations
    - `prometheus-*.yaml` - Prometheus setup files
    - `grafana-*.yaml` - Grafana setup files
- `scripts/` - Utility scripts
  - `dashboard-checker.py` - Grafana dashboard management utility
- `create-dashboard.json` - Grafana dashboard template
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
- Monitoring is implemented with Prometheus and Grafana
- Python dashboard checker ensures Grafana dashboards are correctly set up

## Getting Started

### Starting from the Beginning

If you want to start this tutorial from the beginning without any of the generated Kubernetes infrastructure components, you can checkout the checkpoint branch:

```bash
git checkout checkpoint-2025-04-26
```

This branch represents the initial state of the project with only the Docker setup and without any Kubernetes components or Python utilities.

### Deploying the Complete Application

To deploy the complete application with all Kubernetes components:

1. Ensure you have a working Kubernetes cluster (Minikube, Kind, or Docker Desktop Kubernetes)

2. Create the namespace:
   ```bash
   kubectl apply -f k8s/namespace.yaml
   ```

3. Deploy the persistent volumes:
   ```bash
   kubectl apply -f k8s/persistent-volumes.yaml
   ```

4. Deploy the secrets:
   ```bash
   kubectl apply -f k8s/secrets.yaml
   ```

5. Deploy the database:
   ```bash
   kubectl apply -f k8s/postgres.yaml
   ```

6. Deploy Redis:
   ```bash
   kubectl apply -f k8s/redis.yml
   ```

7. Deploy the Flask API:
   ```bash
   kubectl apply -f k8s/flask-api.yaml
   ```

8. Deploy the monitoring stack:
   ```bash
   kubectl apply -f k8s/monitoring/
   ```

9. Deploy the ingress rules:
   ```bash
   kubectl apply -f k8s/ingress.yaml
   ```

10. Verify the dashboard is properly set up:
    ```bash
    python scripts/dashboard-checker.py
    ```

### Exploring the Monitoring Stack

Once the application is deployed, you can access:

- The Flask API at the ingress endpoint
- Grafana at http://localhost:3000 (default credentials: admin/admin)
- Prometheus at http://localhost:9090

Remember: This project is designed as a learning journey from Docker to Kubernetes. Take your time to understand each concept before moving to the next phase. The documentation in the `docs/` directory is designed to guide you through this journey step by step.
# Test comment
