# Endpoint Statistics Application Runbook

This runbook provides comprehensive step-by-step instructions for deploying, testing, and managing the Endpoint Statistics application Kubernetes infrastructure. Follow these instructions to set up, validate, and maintain the application environment.

## Table of Contents

- [Prerequisites](#prerequisites)
- [1. Deploying the Cluster](#1-deploying-the-cluster)
- [2. Testing Components](#2-testing-components)
- [3. Deployment Strategies](#3-deployment-strategies)
- [4. Cleanup Procedures](#4-cleanup-procedures)
- [5. Troubleshooting](#5-troubleshooting)

## Prerequisites

Before proceeding, ensure you have the following tools and configurations in place:

- Kubernetes cluster (Minikube, Kind, or Docker Desktop Kubernetes)
- `kubectl` command-line tool installed and configured
- Docker installed for building and pushing images
- Git repository cloned locally

### Environment Setup

```bash
# Verify kubectl installation
kubectl version --client

# Verify Kubernetes cluster is running
kubectl cluster-info

# Ensure context is set correctly
kubectl config current-context
```

## 1. Deploying the Cluster

Follow these steps to deploy the complete Kubernetes infrastructure for the Endpoint Statistics application.

### 1.1 Create the Namespace

```bash
# Create a dedicated namespace for the application
kubectl apply -f k8s/core/namespace.yaml

# Verify the namespace was created
kubectl get namespaces | grep endpoint-stats
```

### 1.2 Deploy Storage Resources

```bash
# Create persistent volumes and claims
kubectl apply -f k8s/storage/persistent-volumes.yaml

# Verify persistent volumes and claims are created
kubectl get pv
kubectl get pvc -n endpoint-stats
```

### 1.3 Deploy Secrets

```bash
# Create Kubernetes secrets for sensitive information
kubectl apply -f k8s/security/secrets.yaml

# Verify secrets are created (no values will be displayed)
kubectl get secrets -n endpoint-stats
```

### 1.4 Deploy Database

```bash
# Deploy PostgreSQL database
kubectl apply -f k8s/database/postgres.yaml

# Verify PostgreSQL pods are running
kubectl get pods -n endpoint-stats -l app=postgres
kubectl get svc -n endpoint-stats -l app=postgres

# Wait for PostgreSQL to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n endpoint-stats --timeout=180s
```

### 1.5 Deploy Redis Cache

```bash
# Deploy Redis for caching
kubectl apply -f k8s/cache/redis.yaml

# Verify Redis pods are running
kubectl get pods -n endpoint-stats -l app=redis
kubectl get svc -n endpoint-stats -l app=redis

# Wait for Redis to be ready
kubectl wait --for=condition=ready pod -l app=redis -n endpoint-stats --timeout=120s
```

### 1.6 Deploy Flask API

```bash
# Deploy the Flask API application
kubectl apply -f k8s/core/flask-api.yaml

# Verify Flask API pods are running
kubectl get pods -n endpoint-stats -l app=flask-api
kubectl get svc -n endpoint-stats -l app=flask-api

# Wait for Flask API to be ready
kubectl wait --for=condition=ready pod -l app=flask-api -n endpoint-stats --timeout=120s
```

> **NOTE:** If you see `ErrImageNeverPull` errors in your pod status, this indicates that Kubernetes cannot find the specified Docker image locally.
> For example:
>
> ```output
> api-endpoint-stats-k8s % kubectl get pods -n endpoint-stats -l app=flask-api
> NAME                         READY   STATUS              RESTARTS   AGE
> flask-api-6c6dcbcccc-pmjkh   0/1     ErrImageNeverPull   0          7s
> flask-api-6c6dcbcccc-ztxmr   0/1     ErrImageNeverPull   0          7s
> ```
>
> To fix this:
>
> ```bash
> # Build the Docker image with the correct tag
> docker build -t endpoint-stats:v2 .
>
> # Load the image into Minikube
> minikube image load endpoint-stats:v2
>
> # Redeploy the Flask API
> kubectl delete -f k8s/core/flask-api.yaml && kubectl apply -f k8s/core/flask-api.yaml
> ```
>
> This ensures the image is available locally before deploying the pods. For local Kubernetes deployments, this step is necessary whenever you build new images or change image versions.

### 1.7 Configure Ingress

```bash
# Deploy ingress rules
kubectl apply -f k8s/networking/ingress.yaml

# Verify ingress is configured
kubectl get ingress -n endpoint-stats
```

### 1.8 Deploy Monitoring Stack

```bash
# First, deploy the CRDs (Custom Resource Definitions) required by the Prometheus Operator
kubectl apply -f k8s/monitoring/prometheus-operator-crds.yaml

# Then, deploy the rest of the monitoring resources
kubectl apply -f k8s/monitoring/ --validate=false

# Verify monitoring components are running
kubectl get pods -n endpoint-stats -l app=prometheus
kubectl get pods -n endpoint-stats -l app=grafana
kubectl get pods -n endpoint-stats -l app=alertmanager

# Wait for monitoring components to be ready
kubectl wait --for=condition=ready pod -l app=prometheus -n endpoint-stats --timeout=180s
kubectl wait --for=condition=ready pod -l app=grafana -n endpoint-stats --timeout=180s
```

> **NOTE:** The monitoring stack deployment requires Prometheus Operator CRDs to be installed first.
> If you see errors like `no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"`, it means the CRDs
> are not properly installed. Run the first command to install the CRDs before proceeding.
>
> We use `--validate=false` when applying the monitoring stack to skip validation for some of the JSON files
> that are meant to be consumed by Grafana rather than directly by Kubernetes.

### 1.9 Configure Monitoring Dashboards

```bash
# Set up port forwarding to access Grafana (run this in a new terminal and keep it running)
kubectl port-forward -n endpoint-stats svc/grafana 3000:3000

# In a different terminal, run the dashboard checker script
python scripts/monitoring/dashboard-checker.py

# Verify dashboards exist in Grafana
# Access Grafana UI at http://localhost:3000 in your browser (default credentials: admin/admin)
```

> **NOTE:** The dashboard checker script requires port forwarding to be active to connect to Grafana.
> If you see connection errors like `Connection refused`, make sure the port-forward command is
> running successfully in another terminal window before executing the script.

### 1.10 Access the Application

```bash
# Set up port forwarding to access the application
kubectl port-forward -n endpoint-stats svc/flask-api 9999:9999

# In a web browser, navigate to http://localhost:9999
# You should see the welcome message and access count
```

## 2. Testing Components

Follow these steps to verify that each component is working as expected.

### 2.1 Run Health Check Script

```bash
# Execute the health check script
./scripts/health-check.sh test-health-report.txt

# Review the health report
cat test-health-report.txt
```

### 2.2 Test Flask API

```bash
# Access the root endpoint (should return welcome message and access count)
curl http://localhost:9999/

# Access the stats endpoint (should return access statistics)
curl http://localhost:9999/stats

# Access the health endpoint (should return health status)
curl http://localhost:9999/health

# Access the metrics endpoint (should return Prometheus metrics)
curl http://localhost:9999/metrics
```

### 2.3 Test Database Connectivity

```bash
# Get the PostgreSQL pod name
POSTGRES_POD=$(kubectl get pods -n endpoint-stats -l app=postgres -o name | head -1)

# Test database connection and query data
kubectl exec -n endpoint-stats ${POSTGRES_POD} -- bash -c "PGPASSWORD=postgres psql -U postgres -d postgres -c 'SELECT * FROM endpoint_access LIMIT 5;'"
```

### 2.4 Test Redis Connectivity

```bash
# Get the Redis pod name
REDIS_POD=$(kubectl get pods -n endpoint-stats -l app=redis -o name | head -1)

# Test Redis connection and check cached keys
kubectl exec -n endpoint-stats ${REDIS_POD} -- redis-cli PING
kubectl exec -n endpoint-stats ${REDIS_POD} -- redis-cli KEYS "*"
```

### 2.5 Test Prometheus Metrics

```bash
# Set up port forwarding to access Prometheus
kubectl port-forward -n endpoint-stats svc/prometheus 9090:9090

# Access Prometheus in a web browser: http://localhost:9090
# Check the status of targets and api-endpoint-stats metrics
```

### 2.6 Test Grafana Dashboards

```bash
# Set up port forwarding to access Grafana
kubectl port-forward -n endpoint-stats svc/grafana 3000:3000

# Access Grafana in a web browser: http://localhost:3000
# Default credentials: admin/admin
# Verify dashboards are loading and displaying metrics

# Run the dashboard checker script to ensure the dashboard is present
source venv/bin/activate
python scripts/monitoring/dashboard-checker.py
```

## 3. Deployment Strategies

This section covers testing deployment strategies like rollback and disaster recovery.

### 3.1 Testing Rollback Procedure

```bash
# Deploy a new version of the application
./scripts/deployment/deploy.sh v2 endpoint-stats flask-api

# Verify the new version is deployed
kubectl get pods -n endpoint-stats -l app=flask-api

# Perform rollback to previous version
./scripts/deployment/rollback.sh flask-api endpoint-stats

# Verify rollback was successful
kubectl get pods -n endpoint-stats -l app=flask-api
kubectl rollout history deployment/flask-api -n endpoint-stats
```

### 3.2 Testing Disaster Recovery

```bash
# Create a database backup using the provided script
./scripts/backup/db-backup.sh endpoint-stats

# Verify the backup was created (it will be in the ./backups directory)
ls -lh ./backups

# Simulate a disaster (for testing purposes)
kubectl delete pod -n endpoint-stats -l app=postgres

# Wait for the database to recover automatically
kubectl wait --for=condition=ready pod -l app=postgres -n endpoint-stats --timeout=180s

# If needed, restore from backup (using the most recent backup file)
LATEST_BACKUP=$(ls -t ./backups/postgres-backup-*.sql | head -1)
./scripts/backup/dr-restore.sh ${LATEST_BACKUP}

# Verify database restoration
POSTGRES_POD=$(kubectl get pods -n endpoint-stats -l app=postgres -o name | head -1)
kubectl exec -n endpoint-stats ${POSTGRES_POD} -- bash -c "PGPASSWORD=postgres psql -U postgres -d postgres -c 'SELECT count(*) FROM information_schema.tables WHERE table_schema = '\'public\'';'"
```

## 4. Cleanup Procedures

Follow these steps to clean up all deployed resources after completion.

### 4.1 Delete Application Components

```bash
# Remove Flask API deployment
kubectl delete -f k8s/core/flask-api.yaml

# Remove Redis cache
kubectl delete -f k8s/cache/redis.yaml

# Remove PostgreSQL database
kubectl delete -f k8s/database/postgres.yaml
```

### 4.2 Delete Monitoring Stack

```bash
# First, ensure Prometheus Operator CRDs are installed (required to delete custom resources)
echo "Ensuring CRDs are installed before cleanup..."
kubectl apply -f k8s/monitoring/prometheus-operator-crds.yaml || true

# Wait a moment for the CRDs to be registered
sleep 5

# Now delete the monitoring components (custom resources first)
echo "Deleting monitoring components..."
kubectl delete -f k8s/monitoring/service-monitors.yaml --ignore-not-found=true
kubectl delete -f k8s/monitoring/redis-servicemonitor.yaml --ignore-not-found=true
kubectl delete -f k8s/monitoring/prometheus-rules.yaml --ignore-not-found=true
kubectl delete -f k8s/monitoring/endpoint-stats-alerts.yaml --ignore-not-found=true
kubectl delete -f k8s/monitoring/kube-state-metrics-deployment.yaml --ignore-not-found=true

# Then delete the rest of the monitoring components
kubectl delete -f k8s/monitoring/ --ignore-not-found=true

# Delete any remaining custom resources
kubectl delete servicemonitors.monitoring.coreos.com --all -n endpoint-stats 2>/dev/null || true
kubectl delete prometheusrules.monitoring.coreos.com --all -n endpoint-stats 2>/dev/null || true
kubectl delete podmonitors.monitoring.coreos.com --all -n endpoint-stats 2>/dev/null || true
kubectl delete alertmanagers.monitoring.coreos.com --all -n endpoint-stats 2>/dev/null || true
kubectl delete prometheuses.monitoring.coreos.com --all -n endpoint-stats 2>/dev/null || true

# Verify all monitoring resources are deleted
echo "Verifying monitoring resources are gone..."
kubectl get deployments,services,configmaps -n endpoint-stats -l app=prometheus
kubectl get deployments,services,configmaps -n endpoint-stats -l app=grafana
kubectl get deployments,services,configmaps -n endpoint-stats -l app=alertmanager

# Finally, delete the CRDs if they're no longer needed
echo "Deleting Prometheus Operator CRDs..."
kubectl delete -f k8s/monitoring/prometheus-operator-crds.yaml --ignore-not-found=true
```

### 4.3 Delete Ingress and Configuration

```bash
# Remove ingress rules
kubectl delete -f k8s/networking/ingress.yaml

# Remove secrets
kubectl delete -f k8s/security/secrets.yaml
```

### 4.4 Delete Storage Resources

```bash
# First verify no pods are using the volumes
kubectl get pods -n endpoint-stats

# Delete persistent volume claims
kubectl delete pvc -n endpoint-stats --all

# Delete persistent volumes
kubectl delete -f k8s/storage/persistent-volumes.yaml
```

### 4.5 Delete Namespace

```bash
# Delete the entire namespace (this will delete all resources in the namespace)
kubectl delete -f k8s/core/namespace.yaml

# Verify namespace is removed
kubectl get namespaces | grep endpoint-stats
```

## 5. Troubleshooting

This section provides guidance for resolving common issues that may arise.

### 5.1 Pod Startup Issues

If pods fail to start:

```bash
# Check pod status
kubectl get pods -n endpoint-stats

# Describe the problematic pod
kubectl describe pod <pod-name> -n endpoint-stats

# Check pod logs
kubectl logs <pod-name> -n endpoint-stats

# Check recent events
kubectl get events -n endpoint-stats --sort-by='.lastTimestamp'
```

### 5.2 Database Connection Issues

If applications cannot connect to PostgreSQL:

```bash
# Verify PostgreSQL pod is running
kubectl get pods -n endpoint-stats -l app=postgres

# Check PostgreSQL logs
POSTGRES_POD=$(kubectl get pods -n endpoint-stats -l app=postgres -o name | head -1)
kubectl logs -n endpoint-stats ${POSTGRES_POD}

# Test database connection from within the cluster
kubectl exec -n endpoint-stats deployment/flask-api -- curl -s http://postgres:5432

# Test database connection directly
kubectl exec -n endpoint-stats ${POSTGRES_POD} -- bash -c "PGPASSWORD=postgres psql -U postgres -d postgres -c 'SELECT 1;'"

# Verify volumes are properly mounted
kubectl describe pod ${POSTGRES_POD} -n endpoint-stats | grep -A5 Mounts:
```

### 5.3 Redis Connection Issues

If applications cannot connect to Redis:

```bash
# Verify Redis pod is running
kubectl get pods -n endpoint-stats -l app=redis

# Check Redis logs
REDIS_POD=$(kubectl get pods -n endpoint-stats -l app=redis -o name | head -1)
kubectl logs -n endpoint-stats ${REDIS_POD}

# Test Redis connection from within the cluster
kubectl exec -n endpoint-stats deployment/flask-api -- curl -s http://redis:6379
```

### 5.4 Monitoring Stack Issues

If Prometheus or Grafana is not working properly:

```bash
# Check Prometheus pod status
kubectl get pods -n endpoint-stats -l app=prometheus
kubectl logs -n endpoint-stats $(kubectl get pods -n endpoint-stats -l app=prometheus -o name | head -1)

# Check Grafana pod status
kubectl get pods -n endpoint-stats -l app=grafana
kubectl logs -n endpoint-stats $(kubectl get pods -n endpoint-stats -l app=grafana -o name | head -1)

# Verify ConfigMaps are correctly created
kubectl get configmaps -n endpoint-stats

# Verify persistent volumes are correctly bound
kubectl get pvc -n endpoint-stats
```

### 5.5 Resource Constraints

If pods are being terminated due to resource constraints:

```bash
# Check node resources
kubectl describe nodes

# Check pod resource usage
kubectl top pods -n endpoint-stats

# Adjust resource limits in deployment files if necessary
# Then reapply the modified configuration
kubectl apply -f <modified-file>
```

### 5.6 Service Discovery Issues

If services cannot find each other:

```bash
# Verify service endpoints
kubectl get endpoints -n endpoint-stats

# Check DNS resolution from a pod
kubectl exec -n endpoint-stats deployment/flask-api -- nslookup postgres
kubectl exec -n endpoint-stats deployment/flask-api -- nslookup redis

# Test connectivity between services
kubectl exec -n endpoint-stats deployment/flask-api -- curl -s http://postgres:5432
kubectl exec -n endpoint-stats deployment/flask-api -- curl -s http://redis:6379
```

### 5.7 Ingress Issues

If ingress is not properly routing traffic:

```bash
# Check ingress status
kubectl get ingress -n endpoint-stats
kubectl describe ingress -n endpoint-stats

# Verify ingress controller is running
kubectl get pods -n ingress-nginx

# Check ingress controller logs
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller
```

### 5.8 Monitoring Stack Deployment Issues

If you encounter errors when deploying the monitoring stack:

```bash
# If you see CRD-related errors like "no matches for kind 'ServiceMonitor' in version 'monitoring.coreos.com/v1'"
# Make sure to install the Prometheus Operator CRDs first
kubectl apply -f k8s/monitoring/prometheus-operator-crds.yaml

# If there are issues with JSON validation in the monitoring resources
kubectl apply -f k8s/monitoring/ --validate=false

# Check that the CRDs were properly installed
kubectl get crd | grep monitoring.coreos.com

# Verify the ServiceMonitor and PrometheusRule resources were created
kubectl get servicemonitors,prometheusrules -n endpoint-stats

# For issues with Grafana dashboards or configuration
kubectl logs -n endpoint-stats deployment/grafana
```

### 5.8.1 Dashboard Configuration Issues

If you encounter errors with the `dashboard-checker.py` script:

```bash
# Ensure the Grafana port-forward is running in another terminal
kubectl port-forward -n endpoint-stats svc/grafana 3000:3000

# Check if the dashboard JSON file exists in the expected location
ls -la create-dashboard.json

# If the file is missing, recreate it from the ConfigMap
kubectl get configmap -n endpoint-stats grafana-dashboard-definition -o jsonpath="{.data['create-dashboard\.json']}" > create-dashboard.json

# Verify you can access Grafana manually before running the script
curl http://localhost:3000/api/health

# Run the script with verbose output for debugging
PYTHONPATH=. python -m scripts.monitoring.dashboard-checker
```

### 5.8.2 Monitoring Stack Deletion Issues

If you encounter errors when deleting the monitoring stack:

```bash
# Error: "no matches for kind 'ServiceMonitor' in version 'monitoring.coreos.com/v1'"
# This means the CRDs are missing. First, reinstall the CRDs:
kubectl apply -f k8s/monitoring/prometheus-operator-crds.yaml || true

# Wait a moment for the CRDs to be registered
sleep 5

# Now try to delete the custom resources first
kubectl delete -f k8s/monitoring/service-monitors.yaml --ignore-not-found=true
kubectl delete -f k8s/monitoring/redis-servicemonitor.yaml --ignore-not-found=true
kubectl delete -f k8s/monitoring/prometheus-rules.yaml --ignore-not-found=true
kubectl delete -f k8s/monitoring/endpoint-stats-alerts.yaml --ignore-not-found=true

# Delete any remaining custom resources by type
kubectl delete servicemonitors.monitoring.coreos.com --all -n endpoint-stats
kubectl delete prometheusrules.monitoring.coreos.com --all -n endpoint-stats
kubectl delete podmonitors.monitoring.coreos.com --all -n endpoint-stats
kubectl delete alertmanagers.monitoring.coreos.com --all -n endpoint-stats
kubectl delete prometheuses.monitoring.coreos.com --all -n endpoint-stats

# Then delete the rest of the monitoring components
kubectl delete -f k8s/monitoring/ --ignore-not-found=true

# If there are still resources that can't be deleted, force delete them
# WARNING: Use force deletion with caution as it can leave resources in an inconsistent state
kubectl patch servicemonitors.monitoring.coreos.com flask-api -n endpoint-stats -p '{"metadata":{"finalizers":[]}}' --type=merge 2>/dev/null || true
kubectl patch prometheusrules.monitoring.coreos.com endpoint-stats-alerts -n endpoint-stats -p '{"metadata":{"finalizers":[]}}' --type=merge 2>/dev/null || true

# Finally, delete the CRDs themselves
kubectl delete -f k8s/monitoring/prometheus-operator-crds.yaml
```

### 5.9 General Diagnostic Commands

Useful commands for diagnosing various issues:

```bash
# Run comprehensive health check
./scripts/health-check.sh detailed-report.txt

# Check all resources in the namespace
kubectl get all -n endpoint-stats

# Check storage status
kubectl get pv,pvc -n endpoint-stats

# Check ConfigMaps and Secrets (without revealing values)
kubectl get configmaps,secrets -n endpoint-stats

# Check network policies
kubectl get networkpolicies -n endpoint-stats
```

### 5.10 Backup and Restore Issues

If you encounter issues with database backup or restore operations:

```bash
# Verify backup script permissions
chmod +x scripts/backup/db-backup.sh
chmod +x scripts/backup/dr-restore.sh

# Check if the backups directory exists
mkdir -p backups

# Manually create a backup for testing
POSTGRES_POD=$(kubectl get pods -n endpoint-stats -l app=postgres -o name | head -1)
kubectl exec -n endpoint-stats ${POSTGRES_POD} -- bash -c "PGPASSWORD=postgres pg_dump -U postgres postgres" > ./backups/manual-backup.sql

# Verify the backup file content
head -20 ./backups/manual-backup.sql

# Test database connectivity before attempting restore
kubectl exec -n endpoint-stats ${POSTGRES_POD} -- bash -c "PGPASSWORD=postgres psql -U postgres -d postgres -c 'SELECT 1;'"
```

This runbook should be kept up-to-date as the infrastructure evolves. For questions or issues not covered here, consult the project documentation or reach out to the DevOps team.

## ⚠️ PostgreSQL on macOS/Minikube: Known Limitation

> **IMPORTANT:**
> Due to a known limitation with Minikube's storage provisioner on macOS, the PostgreSQL pod may fail to start with a permissions error when using either persistent volumes or `emptyDir` for `/var/lib/postgresql/data`. This is caused by the way Minikube mounts host paths and handles user permissions on macOS, and is not an issue with your Kubernetes manifests.
>
> **Workarounds:**
> - This issue does not occur on Linux-based Kubernetes clusters.
> - For local development on macOS, you may need to use an alternative Postgres setup outside of Kubernetes, or use a remote Linux-based cluster for full Kubernetes testing.
> - Data persistence for Postgres in Kubernetes on macOS/Minikube is not supported at this time.
