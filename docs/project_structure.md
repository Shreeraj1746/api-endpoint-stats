# Project Structure (as of May 2025)

This document describes the current organization of the Endpoint Stats project. The structure is designed for clarity, maintainability, and ease of use.

## Directory Layout

- `k8s/` — Kubernetes manifests, organized by component:
  - `core/` — Main app (Flask API) and namespace
  - `database/` — PostgreSQL
  - `cache/` — Redis
  - `networking/` — Ingress, services
  - `security/` — RBAC, secrets, network policies
  - `storage/` — Persistent volumes
  - `maintenance/` — Backup and maintenance jobs
  - `monitoring/` — Prometheus, Grafana, exporters
  - Symlinks at the root of `k8s/` provide compatibility with the Runbook and quick access to key manifests.
- `scripts/` — Operational scripts
  - `deployment/` — Deployment and rollback scripts
  - `monitoring/` — Monitoring setup scripts
  - `backup/` — Backup and restore scripts
  - `health-check.sh` — General health check utility
  - `setup.sh` — Project setup utility
- `docs/` — Documentation and implementation plans
- `tests/` — Automated tests
- `backups/` — Database backup files
- `certs/` — TLS certificates

## Notes
- Each resource is defined in a single, canonical location, with no redundant or conflicting YAML files.
- Security, scaling, and operational best practices are integrated into the main manifests for each component.
- Use the `k8s/` subdirectories for all Kubernetes resources. Symlinks at the root of `k8s/` provide compatibility with the Runbook.
- Scripts for deployment, monitoring, and backup are in their respective subfolders under `scripts/`.
