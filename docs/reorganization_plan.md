# Project Reorganization Plan

## 1. Current State

The project has a generally well-organized structure with most Kubernetes configurations properly organized in the `k8s/` directory and its subdirectories. However, there are a few issues to address:

1. There are discrepancies between file paths referenced in the Runbook and the actual file locations
2. Some scripts may be unused or redundant
3. The directory structure could be improved for clarity and maintainability

## 2. K8s Directory Structure

The current `k8s/` directory has subdirectories for specific components:
- `cache/` - Redis cache configurations
- `core/` - Core application components like Flask API and namespace
- `database/` - PostgreSQL database configurations
- `deployment-strategy/` - Deployment configuration for rollouts, scaling, etc.
- `maintenance/` - Maintenance tasks, backup jobs, etc.
- `monitoring/` - Prometheus, Grafana, and other monitoring tools
- `networking/` - Ingress and service configurations
- `security/` - RBAC, network policies, and secrets
- `storage/` - Persistent volume configurations

This structure is good, but the Runbook refers to files at the root of the `k8s/` directory, creating potential confusion.

## 2a. Redundancy Check (Detailed)

### Flask API Deployment
- **Files:**
  - `core/flask-api.yaml`
  - `core/flask-api-current.yaml`
  - `deployment-strategy/flask-api-deployment.yaml`
  - `security/flask-api-security.yaml`
- **Redundancy:** All define a Deployment for Flask API, with overlapping but not identical configuration. Only one should exist; security and strategy should be merged into the main Deployment YAML.

### Flask API Service
- **Files:**
  - `core/flask-api.yaml` (Service included)
- **Redundancy:** None.

### Ingress
- **Files:**
  - `networking/ingress.yaml`
  - `security/ingress-with-tls.yaml`
- **Redundancy:** Partial. Both define Ingress for Flask API; merge into one file with both HTTP and HTTPS rules if needed.

### Persistent Volumes/Claims
- **Files:**
  - `storage/persistent-volumes.yaml`
  - `maintenance/backup-pvc.yaml`
- **Redundancy:** None. Each PVC is for a different purpose.

### Database and Cache Deployments
- **Files:**
  - `database/postgres.yaml`
  - `cache/redis.yaml`
- **Redundancy:** None.

### Security Contexts
- **Files:**
  - `security/flask-api-security.yaml`
  - `security/postgres-security.yaml`
  - `security/redis-security.yaml`
- **Redundancy:** High. Security context should be merged into the main Deployment YAML for each component.

### Network Policies
- **Files:**
  - `security/api-network-policy.yaml`
  - `security/network-policies.yaml`
  - `security/postgres-network-policy.yaml`
  - `security/redis-network-policy.yaml`
  - `security/monitoring-network-policy.yaml`
- **Redundancy:** Low. This is a common pattern, but ensure there is no overlap in selectors or conflicting rules.

### Secrets
- **Files:**
  - `security/secrets.yaml`
  - `security/api-credentials.yaml`
- **Redundancy:** Partial. Consider consolidating to a single source of truth for DB credentials.

### Monitoring, Maintenance, Storage, RBAC
- **Redundancy:** None. Each file has a clear, unique purpose.

---

## 4. Reorganization Plan (Updated)

### 4.1 Merge Redundant Deployments
- For each component (Flask API, Postgres, Redis), have a **single Deployment YAML** that includes:
  - Security context
  - Resource limits
  - Probes
  - Strategy
- Remove `*-security.yaml` and `*-deployment.yaml` files for these components. Move their relevant sections into the main Deployment YAML.

### 4.2 Ingress
- Merge `ingress.yaml` and `ingress-with-tls.yaml` into a single file with both HTTP and HTTPS rules, or keep only the one you use.

### 4.3 Secrets
- Consolidate secrets into a single file per environment (e.g., `secrets.yaml`). Use one secret for all DB/API credentials if possible.

### 4.4 Network Policies
- Keep the default deny-all policy and one allow policy per component. Ensure selectors do not overlap or conflict.

### 4.5 Directory Structure
- For each major component, group all related files:
  ```
  k8s/
    core/
      flask-api.yaml         # Deployment + Service + securityContext
      namespace.yaml
    database/
      postgres.yaml          # Deployment + Service + securityContext
    cache/
      redis.yaml             # Deployment + Service + securityContext
    networking/
      ingress.yaml           # Ingress (with/without TLS)
    security/
      network-policies.yaml  # Default deny-all
      api-network-policy.yaml
      postgres-network-policy.yaml
      redis-network-policy.yaml
      rbac.yaml
      secrets.yaml
    storage/
      persistent-volumes.yaml
    maintenance/
      backup-job.yaml
      backup-pvc.yaml
      ...
    monitoring/
      ...
  ```

### 4.6 Remove/Archive
- Remove or archive:
  - `core/flask-api-current.yaml` (if it's a generated file)
  - `security/flask-api-security.yaml`, `security/postgres-security.yaml`, `security/redis-security.yaml` (after merging)
  - `deployment-strategy/flask-api-deployment.yaml` (after merging)
  - Duplicate or unused secrets

### 4.7 Documentation
- Update this document and the main README to reflect these changes.
- Add a section on how to extend/override base configs (e.g., overlays for dev/prod).

### 4.8 Scripts Organization

1. Categorize scripts by function:
   - Create a `scripts/deployment/` directory for deployment-related scripts
   - Create a `scripts/monitoring/` directory for monitoring-related scripts
   - Create a `scripts/backup/` directory for backup-related scripts (renaming the existing `backups/` to avoid confusion)

2. Move scripts to appropriate directories:
   - Move `deploy.sh` and `rollback.sh` to `scripts/deployment/`
   - Move `dashboard-checker.py` to `scripts/monitoring/`
   - Move `db-backup.sh` and `dr-restore.sh` to `scripts/backup/`
   - Keep `health-check.sh` at the root of `scripts/` as it's a general-purpose utility

3. Update script references in `Runbook.md` to reflect the new locations.

### 4.9 Documentation Updates

1. Create a project structure document that clearly explains the organization of the project, including:
   - The purpose of each directory
   - How the various components interact
   - Where to find specific configurations

2. Update the main README.md to include information about the project structure and how to navigate it.

### 4.10 Additional Improvements

1. Create a `.env.example` file to show required environment variables
2. Add a `CONTRIBUTING.md` file with guidelines for contributors
3. Add a simple `Makefile` with common operations for easy execution
4. Create a `scripts/setup.sh` script to help new developers set up the project

## 5. Implementation Plan

1. Create new directories
2. Move files to appropriate directories
3. Create symlinks for Runbook compatibility
4. Update documentation
5. Test all scripts and commands to ensure they still work
6. Clean up any remaining unused files

This plan will improve the organization of the project while maintaining compatibility with existing documentation and workflows.
