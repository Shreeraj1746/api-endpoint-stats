# Endpoint Statistics Application: Docker to Kubernetes Learning Journey

This project is a complete, production-grade example of transitioning a Python Flask application from Docker Compose to a fully monitored, secure, and observable Kubernetes deployment. It includes persistent storage, caching, monitoring, backup, and a robust CI/testing setup.

---

**For all deployment and testing steps, please follow the detailed instructions in the [RUNBOOK.md](Runbook.md).**

---

## Project Overview

- Flask API for endpoint access tracking
- PostgreSQL for data persistence
- Redis for caching
- Grafana and Prometheus for monitoring and observability
- Automated dashboard provisioning
- Comprehensive test suite and health checks
- All Kubernetes manifests and scripts included

## Current Status (May 2025)

- All components are deployed and managed via Kubernetes (see `k8s/`)
- Monitoring stack (Prometheus, Grafana) is fully integrated
- Automated dashboard creation and health checks are in place
- All deployment, testing, and troubleshooting steps are maintained in [RUNBOOK.md](Runbook.md)
- Docker Compose setup is still available for local development/learning

## Quick Start

### Local Docker (for learning)

```bash
docker compose up -d
# ...
docker compose run --rm web pytest -v
```

### Kubernetes (Production/Full Stack)

**Follow the steps in [RUNBOOK.md](Runbook.md) for all Kubernetes deployment, testing, and troubleshooting.**

- Prerequisites: Minikube (or Kind/Docker Desktop), kubectl, Docker
- All manifests are in `k8s/` (organized by component)
- Use the Makefile for common tasks (setup, deploy, test, clean)
- Monitoring stack and dashboards are provisioned automatically

## Project Structure

- `k8s/` — All Kubernetes manifests (core, database, cache, networking, security, storage, maintenance, monitoring)
- `scripts/` — Operational scripts (deployment, monitoring, backup, health-check)
- `docs/` — Implementation guides and project documentation
- `tests/` — Automated tests
- `Runbook.md` — **Main reference for deploying, testing, and managing the cluster**

## Development & Testing Tools

- **Ruff** — Python linter/formatter
- **pytest** — Testing framework
- **pre-commit** — Git hooks
- **commitizen** — Commit message formatting

## Monitoring & Observability

- **Grafana**: http://localhost:3000 (default: admin/admin)
- **Prometheus**: http://localhost:9090
- **Dashboards**: Automatically provisioned (see Runbook)

## Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Kubernetes Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Project Structure Guide](docs/project_structure.md)

---

**For all Kubernetes deployment and testing, always refer to [RUNBOOK.md](Runbook.md) for the latest, correct, and complete instructions.**
