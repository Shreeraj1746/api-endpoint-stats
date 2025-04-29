# Endpoint Statistics Application: Docker to Kubernetes Learning Journey

This project serves as a comprehensive learning experience for transitioning from Docker to Kubernetes. It starts with a simple Flask application running in Docker and guides you through transforming it into a production-ready Kubernetes deployment with monitoring and observability tools.

## Table of Contents

- [Project Overview](#project-overview)
- [Learning Journey](#learning-journey)
  - [Part 1: Docker Basics](#part-1-docker-basics)
  - [Part 2: Kubernetes Implementation](#part-2-kubernetes-implementation)
- [Development Tools](#development-tools)
- [Using the Makefile](#using-the-makefile)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Additional Resources](#additional-resources)

## Project Overview

This is a Flask application that tracks endpoint access counts using PostgreSQL. While it's a simple application, it provides an excellent foundation for learning both Docker and Kubernetes concepts. The project includes a complete Kubernetes infrastructure with monitoring components.

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

Note: You may need to run port forwarding to access these URLs from your host:
```bash
kubectl port-forward -n endpoint-stats svc/flask-api 9999:9999
```

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
- `kubernetes_implementation_plan.md`: Overall implementation strategy

## Development Tools

This project uses a comprehensive set of development tools to ensure code quality and consistency:

### Code Quality Tools

- **Ruff** (v0.3.3) - All-in-one Python linter and formatter
  - Code formatting (similar to Black)
  - Import sorting (similar to isort)
  - Code style checking (similar to flake8)
  - Static type checking (similar to mypy)

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

## Using the Makefile

This project includes a comprehensive Makefile that simplifies common development and operational tasks.

### Available Make Commands

| Command | Description |
|---------|-------------|
| `make help` | Display all available commands with descriptions |
| `make setup` | Set up both development and Kubernetes environments |
| `make setup-dev` | Set up development environment only |
| `make setup-k8s` | Set up Kubernetes environment only |
| `make deploy-all` | Deploy all components to Kubernetes |
| `make test-all` | Run all tests |
| `make health-check` | Run health check and generate report |
| `make backup-db` | Backup the database |
| `make restore-db` | Restore the database from backup |
| `make clean` | Clean up all resources |

### Common Usage Examples

**Setting up your environment**:
```bash
# Complete setup (both dev and k8s)
make setup

# Just development environment
make setup-dev

# Just Kubernetes environment
make setup-k8s
```

**Deployment workflow**:
```bash
# Deploy all components
make deploy-all

# Verify deployment health
make health-check
```

## Project Structure

The project has a well-organized structure to improve maintainability and clarity:

- `app.py` - Main Flask application with endpoint tracking
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Docker Compose configuration
- `Makefile` - Common operations for development and deployment
- `k8s/` - Kubernetes YAML configurations organized by component
  - `core/` - Core application components (namespace, Flask API)
  - `database/` - Database configurations
  - `cache/` - Redis cache configurations
  - `storage/` - Persistent storage configurations
  - `networking/` - Ingress and service configurations
  - `security/` - RBAC, network policies, and secrets
  - `monitoring/` - Monitoring stack configurations
  - `deployment-strategy/` - Deployment configuration for rollouts, scaling
  - `maintenance/` - Maintenance tasks, backup jobs, etc.
- `scripts/` - Operational scripts organized by function
  - `deployment/` - Deployment and rollback scripts
  - `backup/` - Backup and restore scripts
  - `monitoring/` - Monitoring configuration scripts
  - `health-check.sh` - Health check utility
  - `setup.sh` - Environment setup script
- `tests/` - Test files
- `docs/` - Kubernetes implementation guides and documentation
  - `project_structure.md` - Detailed project structure documentation

For a more detailed explanation of the project structure, please see [docs/project_structure.md](docs/project_structure.md).

## Getting Started

### Starting from the Beginning

If you want to start this tutorial from the beginning without any of the generated Kubernetes infrastructure components, you can checkout the checkpoint branch:

```bash
git checkout checkpoint-2025-04-26
```

This branch represents the initial state of the project with only the Docker setup and without any Kubernetes components or Python utilities.

### Deploying the Complete Application

The recommended way to deploy the complete application is using the Makefile:

```bash
# Set up Kubernetes environment
make setup-k8s

# Deploy all components
make deploy-all
```

For step-by-step deployment instructions, please refer to the [Runbook.md](Runbook.md).

### Exploring the Monitoring Stack

Once the application is deployed, you can access:

- The Flask API at the ingress endpoint
- Grafana at http://localhost:3000 (default credentials: admin/admin)
- Prometheus at http://localhost:9090

Note: You may need to run port forwarding to access these URLs from your host:
```bash
kubectl port-forward -n endpoint-stats svc/grafana 3000:3000
kubectl port-forward -n endpoint-stats svc/prometheus 9090:9090
```

## Additional Resources

### Kubernetes Learning Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Kubernetes Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)

Remember: This project is designed as a learning journey from Docker to Kubernetes. Take your time to understand each concept before moving to the next phase. The documentation in the `docs/` directory is designed to guide you through this journey step by step.
