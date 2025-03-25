# Kubernetes Implementation Plan for Endpoint Statistics Application

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Implementation Order](#implementation-order)
  - [Quick Start Commands](#quick-start-commands)
  - [Complete Project Structure](#complete-project-structure)
  - [Implementation Checklist](#implementation-checklist)
- [Overview of Implementation Phases](#overview-of-implementation-phases)
- [Phase 1: Local Development Environment Setup](#phase-1-local-development-environment-setup---detailed-implementation)
  - [Installation of Required Tools](#1-installation-of-required-tools)
  - [Minikube Configuration](#2-minikube-configuration)
  - [Project Structure Setup](#3-project-structure-setup)
  - [Development Workflow Setup](#4-development-workflow-setup)
  - [Phase 1 Learning Outcomes](#learning-outcomes)
- [Phase 2: Service Implementation](#phase-2-service-implementation---detailed-implementation)
  - [Enhanced Flask API Service](#1-enhanced-flask-api-service)
  - [Rate Limiter Service](#2-rate-limiter-service)
  - [Analytics Service](#3-analytics-service)
  - [Grafana Dashboard](#4-grafana-dashboard)
  - [Testing Plan for Phase 2](#5-testing-plan)
- [Phase 3: Kubernetes Configuration](#phase-3-kubernetes-configuration---detailed-implementation)
  - [Namespace and RBAC Configuration](#1-namespace-and-rbac-configuration)
  - [Storage Configuration](#2-storage-configuration)
  - [Network Policies and Services](#3-implement-network-policies-and-services)
  - [Security Configurations](#4-create-security-configurations)
- [Phase 4: Deployment Strategy](#phase-4-deployment-strategy---detailed-implementation)
  - [Initial Deployment Sequence](#1-initial-deployment-sequence)
  - [Rolling Update Configuration](#2-rolling-update-configuration)
  - [Scaling Rules and Autoscaling](#3-scaling-rules-and-autoscaling)
  - [Health Checks and Probes](#4-health-checks-and-probes)
  - [Autoscaling Configuration](#5-autoscaling-configuration)
- [Phase 5: Monitoring and Maintenance](#phase-5-monitoring-and-maintenance---detailed-implementation)
  - [Grafana Dashboard Setup](#1-grafana-dashboard-setup)
  - [Backup Procedures](#2-backup-procedures)
  - [Update Strategies](#3-update-strategies)
  - [Troubleshooting Guides](#4-troubleshooting-guides)
- [Phase 6: Final Deployment and Testing](#phase-6-final-deployment-and-testing)
  - [Final Deployment](#1-final-deployment)
  - [Final Testing](#2-final-testing)
- [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)
  - [Minikube Issues](#minikube-issues)
  - [Kubernetes Issues](#kubernetes-issues)
  - [Application Issues](#application-issues)
  - [Advanced Debugging Techniques](#advanced-debugging-techniques)
- [Final Thoughts](#final-thoughts)
- [References](#references)
- [Next Steps](#next-steps)

---

## Getting Started

This guide provides a step-by-step approach to implement a comprehensive Kubernetes-based application for tracking endpoint statistics. To successfully implement this project, follow these steps in order:

### Prerequisites

Before beginning, ensure you have:
- A computer with at least 8GB RAM, 4 CPU cores, and 20GB of free disk space
- Administrator/sudo privileges on your machine
- Basic understanding of Docker, Kubernetes, and Python
- Internet connection for downloading tools and container images

### Implementation Order

For the best results, implement the phases in this order:

1. **Set up your development environment** (Phase 1)
   - Install all required tools (Docker, kubectl, Minikube, Helm)
   - Configure Minikube with appropriate resources
   - Create your project structure

2. **Develop the microservices** (Phase 2)
   - Implement the Flask API service
   - Create the Rate Limiter service
   - Build the Analytics service
   - Configure Grafana dashboards
   - Test the services locally using Docker Compose

3. **Configure Kubernetes foundation** (Phase 3)
   - Create namespaces and set up RBAC
   - Configure persistent storage
   - Implement network policies and services
   - Set up security with ConfigMaps and Secrets

4. **Deploy the application** (Phase 4)
   - Follow the deployment sequence
   - Configure rolling updates
   - Set up scaling and health checks

5. **Establish monitoring and maintenance** (Phase 5)
   - Finalize Grafana dashboards
   - Implement backup procedures
   - Document update strategies
   - Create troubleshooting guides

6. **Final testing and validation** (Phase 6)
   - Perform comprehensive testing
   - Validate all functionality works as expected

### Quick Start Commands

If you want to get started immediately, run these commands to set up your environment:

```bash
# Install required tools (macOS example with Homebrew)
brew install kubectl docker helm
brew install minikube

# Start Minikube with appropriate resources
minikube start --cpus=4 --memory=8192 --disk-size=20g --driver=hyperkit

# Clone the project repository (if available)
# git clone https://github.com/your-username/endpoint-stats.git

# Create project structure
mkdir -p kubernetes-endpoint-stats/{kubernetes/{base,services,config,network},app,scripts}
cd kubernetes-endpoint-stats

# Run the setup scripts in order
bash scripts/setup-minikube.sh
bash scripts/setup-namespace.sh
bash scripts/manage-volumes.sh create
bash scripts/setup-network.sh
```

Now you're ready to proceed with the detailed implementation of each phase as described in this document.

### Complete Project Structure

When you've finished the implementation, your project should have the following structure:

```
kubernetes-endpoint-stats/
├── app/
│   ├── api/
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   ├── models.py
│   │   └── requirements.txt
│   ├── rate-limiter/
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   └── requirements.txt
│   └── analytics/
│       ├── Dockerfile
│       ├── app.py
│       └── requirements.txt
├── kubernetes/
│   ├── base/
│   │   ├── namespace.yaml
│   │   ├── service-account.yaml
│   │   ├── role.yaml
│   │   ├── rolebinding.yaml
│   │   ├── resource-quota.yaml
│   │   └── limit-range.yaml
│   ├── services/
│   │   ├── flask-api-service.yaml
│   │   ├── rate-limiter-service.yaml
│   │   ├── analytics-service.yaml
│   │   ├── postgres-service.yaml
│   │   ├── redis-service.yaml
│   │   ├── grafana-service.yaml
│   │   └── ingress.yaml
│   ├── config/
│   │   ├── storage-class.yaml
│   │   ├── postgres-pvc.yaml
│   │   ├── redis-pvc.yaml
│   │   ├── grafana-pvc.yaml
│   │   ├── postgres-secrets.yaml
│   │   ├── redis-config.yaml
│   │   ├── rate-limiter-config.yaml
│   │   └── grafana-config.yaml
│   ├── network/
│   │   ├── default-deny.yaml
│   │   ├── allow-api-traffic.yaml
│   │   ├── allow-redis-traffic.yaml
│   │   └── allow-postgres-traffic.yaml
│   └── deployments/
│       ├── flask-api-deployment.yaml
│       ├── rate-limiter-deployment.yaml
│       ├── analytics-deployment.yaml
│       ├── postgres-deployment.yaml
│       ├── redis-deployment.yaml
│       └── grafana-deployment.yaml
├── scripts/
│   ├── setup-minikube.sh
│   ├── setup-namespace.sh
│   ├── manage-volumes.sh
│   ├── setup-network.sh
│   ├── debug-network.sh
│   ├── backup-postgres.sh
│   └── check-storage.sh
└── docker-compose.yml
```

This structure ensures that all the files referenced in this document are properly organized and can be easily located during implementation.

### Implementation Checklist

Use this checklist to track your progress as you work through the implementation:

#### Phase 1: Development Environment
- [ ] Install Docker
- [ ] Install kubectl
- [ ] Install Minikube
- [ ] Install Helm
- [ ] Configure Minikube resources
- [ ] Create project directory structure
- [ ] Set up development workflow scripts

#### Phase 2: Service Implementation
- [ ] Implement Flask API service
  - [ ] Create app.py with endpoint tracking
  - [ ] Add Redis caching
  - [ ] Implement Prometheus metrics
  - [ ] Add database model
- [ ] Implement Rate Limiter service
  - [ ] Create Redis-based rate limiting
  - [ ] Implement health checks
- [ ] Implement Analytics service
  - [ ] Create data collection endpoints
  - [ ] Add reporting endpoints
- [ ] Configure Grafana dashboards
  - [ ] Set up API usage dashboard
  - [ ] Set up system metrics dashboard
- [ ] Test services locally

#### Phase 3: Kubernetes Configuration
- [ ] Create and configure namespace
- [ ] Set up RBAC permissions
- [ ] Configure StorageClass
- [ ] Create PersistentVolumeClaims
- [ ] Set up network policies
- [ ] Configure services
- [ ] Set up ingress
- [ ] Implement security configurations

#### Phase 4: Deployment
- [ ] Deploy PostgreSQL
- [ ] Deploy Redis
- [ ] Deploy Flask API
- [ ] Deploy Rate Limiter
- [ ] Deploy Analytics service
- [ ] Deploy Grafana
- [ ] Configure rolling updates
- [ ] Set up health checks
- [ ] Configure autoscaling

#### Phase 5: Monitoring and Maintenance
- [ ] Finalize Grafana dashboards
- [ ] Set up backup procedures
- [ ] Document update strategies
- [ ] Create troubleshooting guides

#### Phase 6: Final Testing
- [ ] Perform load testing
- [ ] Run security checks
- [ ] Validate all functionality
- [ ] Document test results

---

## Overview of Implementation Phases

### Phase 1: Local Development Environment Setup
- Install required tools (Minikube, kubectl, Docker, Helm)
- Configure Minikube with appropriate resources
- Set up project structure and development workflow

### Phase 2: Service Implementation
- Enhance Flask API Service with monitoring, caching, and metrics
- Create Rate Limiter Service for API protection
- Develop Analytics Service for detailed usage statistics
- Configure Grafana for visualization dashboards

### Phase 3: Kubernetes Configuration
- Set up namespaces and RBAC rules
- Configure storage (PersistentVolumes)
- Implement network policies and services
- Create security configurations

### Phase 4: Deployment Strategy
- Initial deployment sequence
- Rolling update configuration
- Scaling rules and autoscaling
- Health checks and probes

### Phase 5: Monitoring and Maintenance
- Grafana dashboard setup
- Backup procedures
- Update strategies
- Troubleshooting guides

---

## Phase 1: Local Development Environment Setup - Detailed Implementation

### 1. Installing Required Tools

#### Minikube

**Purpose and Benefits:**
- Creates a local single-node Kubernetes cluster inside a VM or container
- Provides a realistic Kubernetes environment without cloud costs
- Allows for rapid development and testing of Kubernetes configurations
- Supports most Kubernetes features needed for our application

**Installation Options:**
```bash
# macOS (with Homebrew)
brew install minikube

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Windows (with Chocolatey)
choco install minikube

# Windows (manual)
# Download the installer from https://minikube.sigs.k8s.io/docs/start/
```

**Configuration Details:**
- **CPU & Memory Requirements:** Minimum 2 CPUs, 4GB RAM recommended for our multi-service setup
- **Storage:** At least 20GB free disk space for images and volumes
- **VM Drivers:**
  - **macOS:** hyperkit (preferred), virtualbox, or docker
  - **Linux:** kvm2 (preferred), virtualbox, or docker
  - **Windows:** hyperv (preferred) or virtualbox

**Startup Configuration:**
```bash
# Basic startup
minikube start

# Recommended configuration for our application
minikube start --cpus=4 --memory=8192 --disk-size=20g --driver=<driver>

# With Kubernetes version pinning (for reproducibility)
minikube start --kubernetes-version=v1.27.3 --cpus=4 --memory=8192
```

**Validation:**
```bash
# Check status
minikube status

# Should output something like:
# minikube
# type: Control Plane
# host: Running
# kubelet: Running
# apiserver: Running
# kubeconfig: Configured
```

#### kubectl

**Purpose and Benefits:**
- Command-line tool for interacting with Kubernetes clusters
- Essential for deploying, inspecting, and managing applications
- Works with any Kubernetes cluster, including Minikube and cloud providers

**Installation Options:**
```bash
# macOS (with Homebrew)
brew install kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Windows (with Chocolatey)
choco install kubernetes-cli

# Windows (manual)
# Download from https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
```

**Configuration Check:**
```bash
# Verify installation
kubectl version --client

# Confirm it connects to Minikube
kubectl cluster-info

# Should output something like:
# Kubernetes control plane is running at https://192.168.49.2:8443
# CoreDNS is running at https://192.168.49.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

**Essential Commands for Our Project:**
```bash
# List all resources in a namespace
kubectl get all -n endpoint-stats

# Apply our service configurations
kubectl apply -f kubernetes/base/

# Get logs from our Flask API service
kubectl logs deployment/flask-api -n endpoint-stats

# Execute a command in a pod (e.g., database migrations)
kubectl exec -it pod/postgres-0 -n endpoint-stats -- psql -U postgres
```

#### Docker

**Purpose in Our Setup:**
- Container runtime for building and testing services
- Used by Minikube for running Kubernetes containers
- Required for creating custom images of our services

**Installation Notes:**
- Docker Desktop includes Docker Engine, CLI, Docker Compose (recommended for macOS/Windows)
- On Linux, install Docker Engine directly
- Need minimum Docker version 20.10.x for best compatibility

**Integration with Minikube:**
```bash
# Point the Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# This allows us to build images directly in Minikube's VM
# without needing to push to a registry

# Verify connection
docker ps
# Should show Kubernetes system containers

# After this, we can build our images
docker build -t flask-api:latest ./src/api
```

**Important Docker Commands for Our Project:**
```bash
# Build all our service images
docker build -t flask-api:latest ./src/api
docker build -t rate-limiter:latest ./src/rate-limiter
docker build -t analytics:latest ./src/analytics

# List images to verify
docker images

# Test a service container locally before Kubernetes deployment
docker run --rm -p 9999:9999 flask-api:latest
```

#### Helm (Optional but Recommended)

**Purpose and Benefits:**
- Package manager for Kubernetes applications
- Simplifies deploying complex applications with many components
- Enables versioning and rollbacks
- Provides templating for environment-specific configurations

**Installation:**
```bash
# macOS
brew install helm

# Linux
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Windows (with Chocolatey)
choco install kubernetes-helm
```

**Verification:**
```bash
helm version
# Should output Helm version information
```

**Potential Helm Charts for Our Project:**
- PostgreSQL: For database deployment
- Redis: For caching and rate limiting
- Grafana: For dashboard visualization
- Custom chart for our services

**Basic Helm Commands (if we use it):**
```bash
# Add common repositories
helm repo add bitnami https://charts.bitnami.com/bitnami

# Install PostgreSQL
helm install postgres bitnami/postgresql --namespace endpoint-stats \
  --set postgresqlUsername=postgres,postgresqlPassword=postgres,postgresqlDatabase=endpoint_stats

# Create custom chart for our application (optional)
helm create endpoint-stats-chart
```

### 2. Minikube Configuration

#### Initial Cluster Setup

**Detailed Startup Process:**
```bash
# Start with additional diagnostics
minikube start --cpus 4 --memory 8192 --disk-size 20g --driver=<preferred_driver> --alsologtostderr -v=3

# Verify components
minikube status
kubectl get nodes
kubectl get pods -A
```

**Resource Planning:**
- **CPU:** 4 cores (1 for system, 1 for database, 2 for our services)
- **Memory:** 8GB (2GB for system, 2GB for database, 4GB for our services)
- **Storage:**
  - 1GB for PostgreSQL data
  - 500MB for Redis data
  - 500MB for Grafana dashboards
  - Rest for system, images, and buffers

#### Essential Addons for Our Project

```bash
# Enable the ingress controller for external access
minikube addons enable ingress

# Enable metrics-server for HPA (Horizontal Pod Autoscaler)
minikube addons enable metrics-server

# Optional: Enable dashboard for visual management
minikube addons enable dashboard

# Optional: Enable registry for local image storage
minikube addons enable registry
```

**Addon Details:**

1. **Ingress Controller**
   - Provides external access to services
   - Uses Nginx as the default controller
   - Enables hostname-based routing
   - We'll use it to expose our API and Grafana

2. **Metrics Server**
   - Collects resource metrics from nodes and pods
   - Required for Horizontal Pod Autoscaling
   - Enables scaling based on CPU/memory utilization

3. **Dashboard (Optional)**
   - Web interface for Kubernetes management
   - Helps visualize cluster state
   - Good for learning and debugging
   - Access with: `minikube dashboard`

4. **Registry (Optional)**
   - Local Docker registry for images
   - Alternative to using Minikube's Docker daemon
   - Useful for multi-node clusters

#### Advanced Minikube Configuration

**Persistent Configuration:**
```bash
# Save specific config for our project
minikube config set cpus 4
minikube config set memory 8192
minikube config set disk-size 20g
minikube config set driver <preferred_driver>

# View configuration
minikube config view
```

**Multiple Profiles (for different environments):**
```bash
# Create a development profile
minikube start -p dev-cluster --cpus 2 --memory 4096

# Create a testing profile with more resources
minikube start -p test-cluster --cpus 4 --memory 8192

# Switch between profiles
minikube profile dev-cluster
```

**Network Configuration:**
```bash
# Access service externally (during development)
minikube service flask-api --namespace endpoint-stats

# Get service URL
minikube service flask-api --namespace endpoint-stats --url

# Port forwarding (alternative to service exposure)
kubectl port-forward service/flask-api 9999:9999 -n endpoint-stats
```

#### Troubleshooting Tools

```bash
# Check Minikube VM status
minikube ssh "free -m && df -h"

# View Minikube logs
minikube logs

# Check addon status
minikube addons list

# SSH into Minikube VM for debugging
minikube ssh

# Restart Minikube if issues arise
minikube stop && minikube start
```

### 3. Development Workflow Setup

#### Project Structure Creation

**Complete Directory Hierarchy:**
```
endpoint-stats/
├── src/
│   ├── api/                  # Flask API service
│   │   ├── app.py
│   │   ├── models.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── rate-limiter/         # Rate limiting service
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── analytics/            # Analytics service
│       ├── app.py
│       ├── Dockerfile
│       └── requirements.txt
├── kubernetes/
│   ├── base/                 # Base Kubernetes configurations
│   │   ├── namespace.yaml
│   │   ├── postgres-statefulset.yaml
│   │   ├── redis-statefulset.yaml
│   │   ├── flask-deployment.yaml
│   │   ├── rate-limiter-deployment.yaml
│   │   └── analytics-deployment.yaml
│   ├── services/             # Service definitions
│   │   ├── postgres-service.yaml
│   │   ├── redis-service.yaml
│   │   ├── flask-service.yaml
│   │   ├── rate-limiter-service.yaml
│   │   ├── analytics-service.yaml
│   │   └── ingress.yaml
│   └── config/               # ConfigMaps and Secrets
│       ├── postgres-secrets.yaml
│       ├── redis-config.yaml
│       ├── rate-limiter-config.yaml
│       └── grafana-config.yaml
├── monitoring/               # Grafana dashboards
│   ├── dashboards/
│   │   ├── endpoint-stats.json
│   │   └── system-metrics.json
│   └── datasources/
│       └── postgres-datasource.yaml
├── scripts/                  # Helper scripts
│   ├── setup-minikube.sh
│   ├── build-images.sh
│   └── deploy-all.sh
├── .gitignore
├── README.md
└── docker-compose.yaml       # For local testing without Kubernetes
```

**Creating This Structure:**
```bash
# Create main directories
mkdir -p src/{api,rate-limiter,analytics}
mkdir -p kubernetes/{base,services,config}
mkdir -p monitoring/{dashboards,datasources}
mkdir -p scripts

# Create placeholder files
touch src/api/{app.py,models.py,Dockerfile,requirements.txt}
touch src/rate-limiter/{app.py,Dockerfile,requirements.txt}
touch src/analytics/{app.py,Dockerfile,requirements.txt}
touch scripts/{setup-minikube.sh,build-images.sh,deploy-all.sh}
touch README.md .gitignore
```

#### Git Setup for the Project

**Initial Git Configuration:**
```bash
# Initialize repository
git init

# Create comprehensive .gitignore
cat <<EOF > .gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Kubernetes
kubeconfig

# Minikube
.minikube/

# macOS
.DS_Store

# Docker
.docker/

# Logs
*.log
EOF

# Add all files to git
git add .

# First commit
git commit -m "Initial project structure for Kubernetes implementation"
```

#### Development Tools Configuration

**VS Code Configuration:**
```json
// .vscode/settings.json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "python.linting.pylintArgs": [
    "--disable=C0111"
  ],
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true
  },
  "python.testing.pytestEnabled": true
}
```

**Docker Compose for Local Testing:**
```yaml
# docker-compose.yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: endpoint_stats
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    command: ["redis-server", "--appendonly", "yes"]
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  flask-api:
    build: ./src/api
    depends_on:
      - postgres
      - redis
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/endpoint_stats
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - ANALYTICS_URL=http://analytics:5000
    ports:
      - "9999:9999"

  rate-limiter:
    build: ./src/rate-limiter
    depends_on:
      - redis
    environment:
      - REDIS_HOST=redis
    ports:
      - "5001:5000"

  analytics:
    build: ./src/analytics
    depends_on:
      - postgres
    environment:
      - POSTGRES_HOST=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=endpoint_stats
    ports:
      - "5002:5000"

  grafana:
    image: grafana/grafana:latest
    depends_on:
      - postgres
    environment:
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin
    volumes:
      - ./monitoring/datasources:/etc/grafana/provisioning/datasources
      - ./monitoring/dashboards:/etc/grafana/provisioning/dashboards
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"

volumes:
  postgres_data:
  redis_data:
  grafana_data:
```

#### Helper Scripts

**1. Setup Minikube Script:**
```bash
#!/bin/bash
# scripts/setup-minikube.sh

# Start Minikube with required resources
minikube start --cpus 4 --memory 8192 --disk-size 20g --driver=docker

# Enable necessary addons
minikube addons enable ingress
minikube addons enable metrics-server

# Configure Docker CLI to use Minikube's Docker daemon
eval $(minikube docker-env)

# Create namespace
kubectl create namespace endpoint-stats

echo "Minikube setup complete!"
echo "To use Minikube's Docker daemon in this terminal session:"
echo "  eval \$(minikube docker-env)"
```

**2. Build Images Script:**
```bash
#!/bin/bash
# scripts/build-images.sh

# Ensure we're using Minikube's Docker daemon
eval $(minikube docker-env)

# Build services
echo "Building Flask API image..."
docker build -t flask-api:latest ./src/api

echo "Building Rate Limiter image..."
docker build -t rate-limiter:latest ./src/rate-limiter

echo "Building Analytics image..."
docker build -t analytics:latest ./src/analytics

echo "All images built successfully!"
```

**3. Deploy All Script:**
```bash
#!/bin/bash
# scripts/deploy-all.sh

# Apply Kubernetes configurations in order
echo "Creating namespace and RBAC..."
kubectl apply -f kubernetes/base/namespace.yaml

echo "Creating ConfigMaps and Secrets..."
kubectl apply -f kubernetes/config/

echo "Deploying PostgreSQL and Redis..."
kubectl apply -f kubernetes/base/postgres-statefulset.yaml
kubectl apply -f kubernetes/base/redis-statefulset.yaml
kubectl apply -f kubernetes/services/postgres-service.yaml
kubectl apply -f kubernetes/services/redis-service.yaml

echo "Waiting for database to initialize..."
sleep 30

echo "Deploying application services..."
kubectl apply -f kubernetes/base/flask-deployment.yaml
kubectl apply -f kubernetes/base/rate-limiter-deployment.yaml
kubectl apply -f kubernetes/base/analytics-deployment.yaml
kubectl apply -f kubernetes/services/flask-service.yaml
kubectl apply -f kubernetes/services/rate-limiter-service.yaml
kubectl apply -f kubernetes/services/analytics-service.yaml

echo "Deploying Grafana..."
kubectl apply -f kubernetes/base/grafana-deployment.yaml
kubectl apply -f kubernetes/services/grafana-service.yaml

echo "Creating ingress rules..."
kubectl apply -f kubernetes/services/ingress.yaml

echo "Deployment complete!"
echo "Access the application at: $(minikube ip)"
echo "Grafana dashboard available at: http://$(minikube ip)/grafana"
```

#### Setting Up Development Environment

**Python Virtual Environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux
source venv/bin/activate
# On Windows
.\venv\Scripts\activate

# Install development dependencies
pip install black pylint pytest pytest-flask requests redis psycopg2-binary
```

**Make Scripts Executable:**
```bash
chmod +x scripts/*.sh
```

**Initialize Services:**
```bash
# Create initial Flask API
cat <<EOF > src/api/app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"message": "Hello from Kubernetes!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
EOF

# Create simple Dockerfile
cat <<EOF > src/api/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9999

CMD ["python", "app.py"]
EOF

# Create basic requirements
cat <<EOF > src/api/requirements.txt
Flask==2.0.1
EOF
```

### 4. Next Steps After Setup

Once Phase 1 is complete, you'll have:

1. A fully functioning Minikube cluster
2. A structured project ready for implementation
3. Basic Docker configurations for local testing
4. Helper scripts for common operations
5. Initial service scaffolding

The next phases will involve:
- Implementation of each microservice
- Creation of Kubernetes configurations
- Setting up monitoring and observability
- Implementing deployment workflows
- Testing and validation

## Learning Outcomes

By implementing this project, you'll gain practical experience with:

1. **Kubernetes Core Concepts**
   - Pods, Deployments, StatefulSets, Services
   - ConfigMaps and Secrets
   - Volumes and Persistent Storage
   - Ingress and Service networking

2. **Microservices Architecture**
   - Service communication patterns
   - API design
   - Stateless and stateful services

3. **DevOps Practices**
   - CI/CD workflows
   - Container optimizations
   - Infrastructure as Code

4. **Monitoring and Observability**
   - Metrics collection
   - Dashboard creation
   - Logging and alerting

5. **Performance and Scaling**
   - Horizontal Pod Autoscaling
   - Load testing
   - Resource optimization

---

## Phase 2: Service Implementation - Detailed Implementation

In this phase, we will develop the core microservices that make up our application. We'll enhance the basic Flask API, implement a Rate Limiter service, create an Analytics service, and set up Grafana dashboards.

### 1. Enhanced Flask API Service

#### Architecture Overview

The Flask API service serves as the main application entry point and now includes:
- Database interaction with PostgreSQL
- Redis caching for improved performance
- Prometheus metrics for monitoring
- Integration with other microservices
- Kubernetes-aware configuration

#### Database Model Implementation

**models.py**:
```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class EndpointAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(255), unique=True, nullable=False)
    access_count = db.Column(db.Integer, default=0)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)

    # New fields for enhanced tracking
    response_time = db.Column(db.Float, default=0)
    client_ip = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    pod_name = db.Column(db.String(255), nullable=True)
    error_count = db.Column(db.Integer, default=0)
    success_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'endpoint': self.endpoint,
            'access_count': self.access_count,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'response_time': self.response_time,
            'success_rate': (self.success_count / self.access_count * 100) if self.access_count > 0 else 100,
            'pod_name': self.pod_name
        }
```

#### Enhanced Flask Application

**app.py**:
```python
import os
import time
import socket
import json
import redis
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import prometheus_client
from prometheus_client import Counter, Histogram
import threading
from models import db, EndpointAccess

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Configure database from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql://postgres:postgres@postgres:5432/endpoint_stats'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Configure Redis connection
redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
try:
    redis_client = redis.Redis(host=redis_host, port=redis_port)
    app.logger.info(f"Connected to Redis at {redis_host}:{redis_port}")
except Exception as e:
    app.logger.error(f"Redis connection error: {str(e)}")
    redis_client = None

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])
CACHE_HIT = Counter('cache_hit_total', 'Cache Hit Count', ['endpoint'])
CACHE_MISS = Counter('cache_miss_total', 'Cache Miss Count', ['endpoint'])

# Request tracking middleware
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    # Calculate response time
    request_latency = time.time() - getattr(request, 'start_time', time.time())

    # Update Prometheus metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.path
    ).observe(request_latency)

    # Store response time for endpoint tracking
    request.environ['RESPONSE_TIME'] = request_latency

    return response

# Enhanced endpoint tracking
def track_access(endpoint, is_error=False):
    """
    Track access to an endpoint with enhanced metrics
    """
    with app.app_context():
        access = EndpointAccess.query.filter_by(endpoint=endpoint).first()
        if not access:
            access = EndpointAccess(
                endpoint=endpoint,
                access_count=0,
                success_count=0,
                error_count=0
            )
            db.session.add(access)

        # Handle None access_count
        if access.access_count is None:
            access.access_count = 0

        access.access_count += 1

        if is_error:
            access.error_count = (access.error_count or 0) + 1
        else:
            access.success_count = (access.success_count or 0) + 1

        access.last_accessed = datetime.utcnow()

        # New functionality - store additional metadata
        access.response_time = request.environ.get('RESPONSE_TIME', 0)
        access.client_ip = request.remote_addr
        access.user_agent = request.headers.get('User-Agent', '')
        access.pod_name = socket.gethostname()  # Kubernetes pod name

        db.session.commit()

        # Cache the result in Redis
        if redis_client:
            try:
                cache_key = f"endpoint:{endpoint}"
                cache_data = access.to_dict()
                redis_client.setex(
                    cache_key,
                    3600,  # 1 hour expiration
                    json.dumps(cache_data)
                )
            except Exception as e:
                app.logger.error(f"Redis caching error: {str(e)}")

        # Asynchronously notify the analytics service
        threading.Thread(
            target=notify_analytics,
            args=(endpoint, access)
        ).start()

        return access

def notify_analytics(endpoint, access):
    """
    Send access data to the analytics service
    """
    try:
        analytics_url = os.environ.get('ANALYTICS_URL', 'http://analytics:5000/collect')
        requests.post(
            analytics_url,
            json={
                "endpoint": endpoint,
                "timestamp": datetime.utcnow().isoformat(),
                "response_time": access.response_time,
                "client_ip": access.client_ip,
                "user_agent": access.user_agent,
                "pod_name": access.pod_name,
                "is_error": access.error_count > 0
            },
            timeout=1  # Don't wait too long for response
        )
    except Exception as e:
        app.logger.error(f"Failed to notify analytics: {str(e)}")

def check_rate_limit(endpoint):
    """
    Check if the request should be rate limited
    """
    if not redis_client:
        return True  # Allow if Redis is not available

    client_ip = request.remote_addr
    rate_limit_url = os.environ.get('RATE_LIMITER_URL', 'http://rate-limiter:5000/check')

    try:
        response = requests.get(
            rate_limit_url,
            params={
                "endpoint": endpoint,
                "client_ip": client_ip
            },
            timeout=0.5  # Short timeout to prevent blocking
        )

        if response.status_code == 429:  # Too Many Requests
            return False

        return True
    except Exception as e:
        app.logger.error(f"Rate limiter error: {str(e)}")
        return True  # Fail open if rate limiter is unavailable

# Routes
@app.route('/')
def index():
    # Check rate limit first
    if not check_rate_limit('/'):
        return jsonify({
            "error": "Rate limit exceeded",
            "message": "Too many requests"
        }), 429

    # Try to get from cache first
    if redis_client:
        try:
            cached_data = redis_client.get("endpoint:/")
            if cached_data:
                CACHE_HIT.labels(endpoint='/').inc()
                return jsonify({
                    "message": "Welcome to the API Access Tracker",
                    "pod": socket.gethostname(),
                    "timestamp": datetime.utcnow().isoformat(),
                    "from_cache": True
                })
        except Exception as e:
            app.logger.error(f"Cache retrieval error: {str(e)}")

    CACHE_MISS.labels(endpoint='/').inc()
    track_access('/')

    return jsonify({
        "message": "Welcome to the API Access Tracker",
        "pod": socket.gethostname(),
        "timestamp": datetime.utcnow().isoformat(),
        "from_cache": False
    })

@app.route('/stats')
def stats():
    # Check rate limit first
    if not check_rate_limit('/stats'):
        return jsonify({
            "error": "Rate limit exceeded",
            "message": "Too many requests"
        }), 429

    track_access('/stats')

    # Try to get from cache first
    if redis_client:
        try:
            cached_stats = []
            for key in redis_client.scan_iter("endpoint:*"):
                cached_data = redis_client.get(key)
                if cached_data:
                    data = json.loads(cached_data)
                    data['from_cache'] = True
                    cached_stats.append(data)

            if cached_stats:
                CACHE_HIT.labels(endpoint='/stats').inc()
                return jsonify({"endpoints": cached_stats})
        except Exception as e:
            app.logger.error(f"Cache retrieval error: {str(e)}")

    CACHE_MISS.labels(endpoint='/stats').inc()

    # If cache failed or no data, get from database
    endpoints = EndpointAccess.query.all()
    return jsonify({
        "endpoints": [endpoint.to_dict() for endpoint in endpoints]
    })

@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype="text/plain")

@app.route('/health')
def health():
    # Check database connection
    db_healthy = True
    try:
        db.session.execute('SELECT 1')
    except Exception as e:
        db_healthy = False
        app.logger.error(f"Database health check failed: {str(e)}")

    # Check Redis connection
    redis_healthy = True
    if redis_client:
        try:
            redis_client.ping()
        except Exception as e:
            redis_healthy = False
            app.logger.error(f"Redis health check failed: {str(e)}")

    is_healthy = db_healthy and redis_healthy
    status_code = 200 if is_healthy else 503

    return jsonify({
        "status": "healthy" if is_healthy else "unhealthy",
        "database": "up" if db_healthy else "down",
        "redis": "up" if redis_healthy else "down",
        "hostname": socket.gethostname(),
        "timestamp": datetime.utcnow().isoformat()
    }), status_code

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9999))
    app.run(host='0.0.0.0', port=port)
```

#### Updated Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9999

CMD ["python", "app.py"]
```

#### Updated requirements.txt

```
Flask==2.0.1
Flask-SQLAlchemy==2.5.1
SQLAlchemy==1.4.23
psycopg2-binary==2.9.1
redis==3.5.3
prometheus-client==0.11.0
requests==2.26.0
gunicorn==20.1.0
```

### 2. Rate Limiter Service

#### Architecture Overview

The Rate Limiter service is a lightweight microservice that:
- Provides API rate limiting based on client IP and endpoint
- Uses Redis as a backend for distributed rate limiting
- Exposes a RESTful API for rate limit checks
- Implements configurable rate limits via Kubernetes ConfigMap

#### Service Implementation

**app.py**:
```python
from flask import Flask, request, jsonify
import redis
import time
import os
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Redis connection parameters from environment
redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = int(os.environ.get('REDIS_PORT', 6379))

# Connect to Redis
try:
    redis_client = redis.Redis(host=redis_host, port=redis_port)
    redis_client.ping()  # Test connection
    app.logger.info(f"Connected to Redis at {redis_host}:{redis_port}")
except Exception as e:
    app.logger.error(f"Redis connection error: {str(e)}")
    redis_client = None

# Load rate limit configuration from environment or ConfigMap
try:
    rate_limits_json = os.environ.get('RATE_LIMITS', '{}')
    RATE_LIMITS = json.loads(rate_limits_json)
    app.logger.info(f"Loaded rate limits: {RATE_LIMITS}")
except Exception as e:
    app.logger.error(f"Error loading rate limits: {str(e)}")
    RATE_LIMITS = {}

# Default rate limits if not configured
DEFAULT_LIMITS = {
    '/': 100,              # 100 requests per minute for root
    '/stats': 60,          # 60 requests per minute for stats
    '/metrics': 200,       # 200 requests per minute for metrics
    'default': 120         # Default for other endpoints
}

# Use configured limits or defaults
for endpoint, limit in DEFAULT_LIMITS.items():
    if endpoint not in RATE_LIMITS:
        RATE_LIMITS[endpoint] = limit

@app.route('/check', methods=['GET'])
def check_rate_limit():
    """
    Check if a request should be rate limited.

    Query parameters:
    - endpoint: The endpoint path
    - client_ip: The client's IP address

    Returns:
    - 200 OK if request is allowed
    - 429 Too Many Requests if rate limit exceeded
    """
    endpoint = request.args.get('endpoint', '/')
    client_ip = request.args.get('client_ip', '0.0.0.0')

    # Get rate limit for endpoint
    limit = RATE_LIMITS.get(endpoint, RATE_LIMITS.get('default', 120))

    # If Redis is not available, fail open (allow requests)
    if redis_client is None:
        app.logger.warning("Redis unavailable, allowing request")
        return jsonify({
            'allowed': True,
            'limit': limit,
            'current': 0,
            'remaining': limit,
            'redis_status': 'unavailable'
        })

    # Create a key combining IP and endpoint
    key = f"rate:{client_ip}:{endpoint}"

    # Current timestamp
    now = int(time.time())
    minute = now // 60

    # Create a window key for the current minute
    window_key = f"{key}:{minute}"

    try:
        # Get current count
        count = redis_client.get(window_key)
        count = int(count) if count else 0

        # Check if over limit
        if count >= limit:
            app.logger.info(f"Rate limit exceeded: {client_ip} on {endpoint} ({count}/{limit})")
            return jsonify({
                'allowed': False,
                'limit': limit,
                'current': count,
                'reset_after': 60 - (now % 60)
            }), 429

        # Increment and set expiration
        pipe = redis_client.pipeline()
        pipe.incr(window_key)
        pipe.expire(window_key, 90)  # Expire after 90 seconds
        pipe.execute()

        return jsonify({
            'allowed': True,
            'limit': limit,
            'current': count + 1,
            'remaining': limit - count - 1
        })
    except Exception as e:
        app.logger.error(f"Redis error: {str(e)}")
        # Fail open on error
        return jsonify({
            'allowed': True,
            'limit': limit,
            'error': str(e),
            'redis_status': 'error'
        })

@app.route('/limits', methods=['GET'])
def get_limits():
    """
    Get current rate limits configuration
    """
    return jsonify({
        'rate_limits': RATE_LIMITS
    })

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for Kubernetes probes
    """
    is_healthy = True
    redis_status = "up"

    # Check Redis connection
    if redis_client is not None:
        try:
            redis_client.ping()
        except Exception as e:
            is_healthy = False
            redis_status = f"down: {str(e)}"
            app.logger.error(f"Redis health check failed: {str(e)}")
    else:
        is_healthy = False
        redis_status = "not configured"

    status_code = 200 if is_healthy else 503

    return jsonify({
        'status': 'healthy' if is_healthy else 'unhealthy',
        'redis': redis_status,
        'rate_limits': RATE_LIMITS
    }), status_code

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

#### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose application port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["python", "app.py"]
```

#### requirements.txt

```
Flask==2.0.1
redis==3.5.3
requests==2.26.0
```

#### ConfigMap for Rate Limits

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: rate-limiter-config
  namespace: endpoint-stats
data:
  rate-limits.json: |
    {
      "/": 100,
      "/stats": 60,
      "/metrics": 200,
      "default": 120
    }
```

### 3. Analytics Service

#### Architecture Overview

The Analytics service is responsible for:
- Collecting and processing API usage statistics
- Storing time-series data in PostgreSQL
- Providing aggregated views for dashboards
- Performing background data aggregation
- Exposing analytics APIs for Grafana

#### Service Implementation

**app.py**:
```python
from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras
import os
import datetime
import json
import logging
from threading import Thread
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Database connection parameters from environment
DB_PARAMS = {
    'host': os.environ.get('POSTGRES_HOST', 'postgres'),
    'port': os.environ.get('POSTGRES_PORT', 5432),
    'database': os.environ.get('POSTGRES_DB', 'endpoint_stats'),
    'user': os.environ.get('POSTGRES_USER', 'postgres'),
    'password': os.environ.get('POSTGRES_PASSWORD', 'postgres')
}

def get_db_connection():
    """Create a new database connection"""
    conn = psycopg2.connect(**DB_PARAMS)
    conn.autocommit = True
    return conn

def init_db():
    """Initialize database schema"""
    app.logger.info("Initializing database schema...")
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Create detailed analytics table
        cur.execute('''
        CREATE TABLE IF NOT EXISTS endpoint_analytics (
            id SERIAL PRIMARY KEY,
            endpoint VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            response_time FLOAT,
            client_ip VARCHAR(45),
            user_agent TEXT,
            pod_name VARCHAR(255),
            is_error BOOLEAN DEFAULT FALSE
        )
        ''')

        # Create index on timestamp and endpoint
        cur.execute('''
        CREATE INDEX IF NOT EXISTS idx_endpoint_analytics_time_endpoint
        ON endpoint_analytics (timestamp, endpoint)
        ''')

        # Create analytics view
        cur.execute('''
        CREATE OR REPLACE VIEW endpoint_stats AS
        SELECT
            endpoint,
            COUNT(*) as access_count,
            AVG(response_time) as avg_response_time,
            MAX(timestamp) as last_accessed,
            COUNT(DISTINCT client_ip) as unique_clients,
            SUM(CASE WHEN is_error THEN 1 ELSE 0 END) as error_count
        FROM endpoint_analytics
        WHERE timestamp > NOW() - INTERVAL '24 hours'
        GROUP BY endpoint
        ''')

        # Create hourly aggregation table
        cur.execute('''
        CREATE TABLE IF NOT EXISTS hourly_stats (
            id SERIAL PRIMARY KEY,
            endpoint VARCHAR(255) NOT NULL,
            hour TIMESTAMP NOT NULL,
            access_count INTEGER,
            avg_response_time FLOAT,
            p95_response_time FLOAT,
            unique_clients INTEGER,
            error_count INTEGER,
            UNIQUE(endpoint, hour)
        )
        ''')

        # Create geographic distribution table (using IP)
        cur.execute('''
        CREATE TABLE IF NOT EXISTS geo_stats (
            id SERIAL PRIMARY KEY,
            country_code VARCHAR(2),
            region VARCHAR(100),
            city VARCHAR(100),
            endpoint VARCHAR(255),
            date DATE,
            access_count INTEGER,
            UNIQUE(country_code, endpoint, date)
        )
        ''')

        conn.close()
        app.logger.info("Database schema initialized successfully")
    except Exception as e:
        app.logger.error(f"Database initialization error: {str(e)}")
        raise

# Background task for hourly aggregation
def aggregate_hourly_stats():
    """Aggregate statistics hourly"""
    while True:
        try:
            # Sleep until next hour
            now = datetime.datetime.now()
            next_hour = now.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
            sleep_seconds = (next_hour - now).total_seconds()

            # But don't sleep longer than 15 minutes for testing
            sleep_seconds = min(sleep_seconds, 900)
            time.sleep(sleep_seconds)

            app.logger.info("Running hourly aggregation...")

            conn = get_db_connection()
            cur = conn.cursor()

            # Calculate the previous hour
            previous_hour = datetime.datetime.now() - datetime.timedelta(hours=1)
            hour_start = previous_hour.replace(minute=0, second=0, microsecond=0)
            hour_end = hour_start + datetime.timedelta(hours=1)

            # Aggregate data for the previous hour
            cur.execute('''
            INSERT INTO hourly_stats
                (endpoint, hour, access_count, avg_response_time, p95_response_time,
                unique_clients, error_count)
            SELECT
                endpoint,
                %s as hour,
                COUNT(*) as access_count,
                AVG(response_time) as avg_response_time,
                percentile_cont(0.95) WITHIN GROUP (ORDER BY response_time) as p95_response_time,
                COUNT(DISTINCT client_ip) as unique_clients,
                SUM(CASE WHEN is_error THEN 1 ELSE 0 END) as error_count
            FROM endpoint_analytics
            WHERE timestamp >= %s AND timestamp < %s
            GROUP BY endpoint
            ON CONFLICT (endpoint, hour) DO UPDATE SET
                access_count = EXCLUDED.access_count,
                avg_response_time = EXCLUDED.avg_response_time,
                p95_response_time = EXCLUDED.p95_response_time,
                unique_clients = EXCLUDED.unique_clients,
                error_count = EXCLUDED.error_count
            ''', (hour_start, hour_start, hour_end))

            conn.close()
            app.logger.info("Hourly aggregation completed")

        except Exception as e:
            app.logger.error(f"Aggregation error: {str(e)}")
            time.sleep(60)  # Wait a minute and try again

# Start background aggregation thread
aggregation_thread = Thread(target=aggregate_hourly_stats)
aggregation_thread.daemon = True
aggregation_thread.start()

@app.route('/collect', methods=['POST'])
def collect_analytics():
    """Collect analytics data from API service"""
    data = request.json

    # Validate required fields
    if not all(k in data for k in ('endpoint', 'timestamp')):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert analytics data
        cur.execute('''
        INSERT INTO endpoint_analytics
        (endpoint, timestamp, response_time, client_ip, user_agent, pod_name, is_error)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            data.get('endpoint'),
            data.get('timestamp'),
            data.get('response_time', 0),
            data.get('client_ip'),
            data.get('user_agent'),
            data.get('pod_name'),
            data.get('is_error', False)
        ))

        conn.close()
        return jsonify({'status': 'success'}), 201
    except Exception as e:
        app.logger.error(f"Error collecting analytics: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get endpoint statistics"""
    endpoint = request.args.get('endpoint')
    period = request.args.get('period', '24h')

    # Convert period to SQL interval
    interval_map = {
        '1h': '1 hour',
        '6h': '6 hours',
        '24h': '24 hours',
        '7d': '7 days',
        '30d': '30 days'
    }
    interval = interval_map.get(period, '24 hours')

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if endpoint:
            # Get stats for specific endpoint
            cur.execute('''
            SELECT
                endpoint,
                COUNT(*) as access_count,
                AVG(response_time) as avg_response_time,
                PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time) as p95_response_time,
                MAX(timestamp) as last_accessed,
                COUNT(DISTINCT client_ip) as unique_clients,
                SUM(CASE WHEN is_error THEN 1 ELSE 0 END) as error_count
            FROM endpoint_analytics
            WHERE endpoint = %s AND timestamp > NOW() - INTERVAL %s
            GROUP BY endpoint
            ''', (endpoint, interval))
        else:
            # Get stats for all endpoints
            cur.execute('''
            SELECT
                endpoint,
                COUNT(*) as access_count,
                AVG(response_time) as avg_response_time,
                PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time) as p95_response_time,
                MAX(timestamp) as last_accessed,
                COUNT(DISTINCT client_ip) as unique_clients,
                SUM(CASE WHEN is_error THEN 1 ELSE 0 END) as error_count
            FROM endpoint_analytics
            WHERE timestamp > NOW() - INTERVAL %s
            GROUP BY endpoint
            ''', (interval,))

        results = []
        for row in cur:
            results.append(dict(row))

        conn.close()
        return jsonify({'stats': results})
    except Exception as e:
        app.logger.error(f"Error getting stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/timeseries', methods=['GET'])
def get_timeseries():
    """Get time series data for endpoints"""
    endpoint = request.args.get('endpoint')
    period = request.args.get('period', '24h')
    interval = request.args.get('interval', '1h')

    # Convert period to SQL interval
    period_map = {
        '6h': '6 hours',
        '24h': '24 hours',
        '7d': '7 days',
        '30d': '30 days'
    }
    sql_period = period_map.get(period, '24 hours')

    # Convert interval to SQL interval for grouping
    interval_map = {
        '5m': 'date_trunc(\'minute\', timestamp) + INTERVAL \'5 min\' * (EXTRACT(MINUTE FROM timestamp)::INTEGER / 5)',
        '15m': 'date_trunc(\'minute\', timestamp) + INTERVAL \'15 min\' * (EXTRACT(MINUTE FROM timestamp)::INTEGER / 15)',
        '1h': 'date_trunc(\'hour\', timestamp)',
        '1d': 'date_trunc(\'day\', timestamp)'
    }
    sql_interval = interval_map.get(interval, 'date_trunc(\'hour\', timestamp)')

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if endpoint:
            # Time series for specific endpoint
            cur.execute(f'''
            SELECT
                {sql_interval} as time_bucket,
                COUNT(*) as access_count,
                AVG(response_time) as avg_response_time,
                SUM(CASE WHEN is_error THEN 1 ELSE 0 END) as error_count
            FROM endpoint_analytics
            WHERE endpoint = %s AND timestamp > NOW() - INTERVAL %s
            GROUP BY time_bucket
            ORDER BY time_bucket
            ''', (endpoint, sql_period))

            results = []
            for row in cur:
                results.append({
                    'timestamp': row['time_bucket'].isoformat() if row['time_bucket'] else None,
                    'access_count': row['access_count'],
                    'avg_response_time': float(row['avg_response_time']) if row['avg_response_time'] else 0,
                    'error_count': row['error_count']
                })
        else:
            # Time series for all endpoints
            cur.execute(f'''
            SELECT
                {sql_interval} as time_bucket,
                endpoint,
                COUNT(*) as access_count,
                AVG(response_time) as avg_response_time,
                SUM(CASE WHEN is_error THEN 1 ELSE 0 END) as error_count
            FROM endpoint_analytics
            WHERE timestamp > NOW() - INTERVAL %s
            GROUP BY time_bucket, endpoint
            ORDER BY time_bucket, endpoint
            ''', (sql_period,))

            results = []
            for row in cur:
                results.append({
                    'timestamp': row['time_bucket'].isoformat() if row['time_bucket'] else None,
                    'endpoint': row['endpoint'],
                    'access_count': row['access_count'],
                    'avg_response_time': float(row['avg_response_time']) if row['avg_response_time'] else 0,
                    'error_count': row['error_count']
                })

        conn.close()
        return jsonify({'timeseries': results})
    except Exception as e:
        app.logger.error(f"Error getting timeseries: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes probes"""
    is_healthy = True
    error_msg = None

    try:
        # Check database connection
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        conn.close()
    except Exception as e:
        is_healthy = False
        error_msg = str(e)
        app.logger.error(f"Health check failed: {error_msg}")

    status_code = 200 if is_healthy else 503
    return jsonify({
        'status': 'healthy' if is_healthy else 'unhealthy',
        'error': error_msg
    }), status_code

# Initialize database on startup
try:
    init_db()
except Exception as e:
    app.logger.error(f"Failed to initialize database: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

#### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose application port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["python", "app.py"]
```

#### requirements.txt

```
Flask==2.0.1
psycopg2-binary==2.9.1
```

### 4. Grafana Dashboard Setup

#### Architecture Overview

The Grafana dashboard provides:
- Visual representation of API usage statistics
- Real-time monitoring of service health
- Historical data analysis
- Customizable dashboards for different metrics
- Persistent storage for dashboard configurations

#### Implementation Details

##### Data Source Configuration

We configure PostgreSQL as a data source in Grafana to access our analytics data:

**postgres-datasource.yaml**:
```yaml
apiVersion: 1
datasources:
  - name: PostgreSQL
    type: postgres
    url: postgres:5432
    database: endpoint_stats
    user: postgres
    secureJsonData:
      password: postgres
    jsonData:
      sslmode: "disable"
      maxOpenConns: 5
      maxIdleConns: 2
      connMaxLifetime: 14400
      postgresVersion: 1500  # For PostgreSQL 15
```

##### Dashboard Configuration

**dashboards.yaml**:
```yaml
apiVersion: 1
providers:
  - name: 'default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    options:
      path: /var/lib/grafana/dashboards
```

##### API Usage Dashboard

**endpoint-stats.json** (simplified version):
```json
{
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "gnetId": null,
  "graphTooltip": 0,
  "id": 1,
  "links": [],
  "panels": [
    {
      "title": "Endpoint Requests",
      "type": "graph",
      "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
      "datasource": "PostgreSQL",
      "targets": [
        {
          "format": "time_series",
          "group": [],
          "metricColumn": "none",
          "rawQuery": true,
          "rawSql": "SELECT\n  time_bucket as time,\n  access_count\nFROM\n(\n  SELECT\n    DATE_TRUNC('hour', timestamp) as time_bucket,\n    COUNT(*) as access_count\n  FROM endpoint_analytics\n  WHERE\n    $__timeFilter(timestamp)\n  GROUP BY time_bucket\n  ORDER BY time_bucket\n) subquery",
          "refId": "A"
        }
      ]
    },
    {
      "title": "Response Time",
      "type": "graph",
      "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
      "datasource": "PostgreSQL",
      "targets": [
        {
          "format": "time_series",
          "group": [],
          "metricColumn": "none",
          "rawQuery": true,
          "rawSql": "SELECT\n  time_bucket as time,\n  avg_response_time\nFROM\n(\n  SELECT\n    DATE_TRUNC('hour', timestamp) as time_bucket,\n    AVG(response_time) as avg_response_time\n  FROM endpoint_analytics\n  WHERE\n    $__timeFilter(timestamp)\n  GROUP BY time_bucket\n  ORDER BY time_bucket\n) subquery",
          "refId": "A"
        }
      ]
    },
    {
      "title": "Error Rate",
      "type": "graph",
      "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
      "datasource": "PostgreSQL",
      "targets": [
        {
          "format": "time_series",
          "group": [],
          "metricColumn": "none",
          "rawQuery": true,
          "rawSql": "SELECT\n  time_bucket as time,\n  (error_count::float / NULLIF(total_count, 0) * 100) as error_rate\nFROM\n(\n  SELECT\n    DATE_TRUNC('hour', timestamp) as time_bucket,\n    COUNT(*) as total_count,\n    SUM(CASE WHEN is_error THEN 1 ELSE 0 END) as error_count\n  FROM endpoint_analytics\n  WHERE\n    $__timeFilter(timestamp)\n  GROUP BY time_bucket\n  ORDER BY time_bucket\n) subquery",
          "refId": "A"
        }
      ]
    },
    {
      "title": "Endpoint Distribution",
      "type": "pie",
      "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
      "datasource": "PostgreSQL",
      "targets": [
        {
          "format": "table",
          "group": [],
          "metricColumn": "none",
          "rawQuery": true,
          "rawSql": "SELECT\n  endpoint,\n  COUNT(*) as count\nFROM endpoint_analytics\nWHERE\n  $__timeFilter(timestamp)\nGROUP BY endpoint\nORDER BY count DESC",
          "refId": "A"
        }
      ]
    }
  ],
  "refresh": "5s",
  "schemaVersion": 26,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "",
  "title": "API Usage Statistics",
  "uid": "api-usage",
  "version": 1
}
```

##### System Metrics Dashboard

**system-metrics.json** (simplified version):
```json
{
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "gnetId": null,
  "graphTooltip": 0,
  "id": 2,
  "links": [],
  "panels": [
    {
      "title": "CPU Usage by Pod",
      "type": "graph",
      "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
      "datasource": "Prometheus",
      "targets": [
        {
          "expr": "sum by (pod) (rate(container_cpu_usage_seconds_total{namespace=\"endpoint-stats\"}[5m]))",
          "legendFormat": "{{pod}}",
          "refId": "A"
        }
      ]
    },
    {
      "title": "Memory Usage by Pod",
      "type": "graph",
      "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
      "datasource": "Prometheus",
      "targets": [
        {
          "expr": "sum by (pod) (container_memory_usage_bytes{namespace=\"endpoint-stats\"})",
          "legendFormat": "{{pod}}",
          "refId": "A"
        }
      ]
    },
    {
      "title": "Network I/O",
      "type": "graph",
      "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
      "datasource": "Prometheus",
      "targets": [
        {
          "expr": "sum by (pod) (rate(container_network_receive_bytes_total{namespace=\"endpoint-stats\"}[5m]))",
          "legendFormat": "{{pod}} - RX",
          "refId": "A"
        },
        {
          "expr": "sum by (pod) (rate(container_network_transmit_bytes_total{namespace=\"endpoint-stats\"}[5m]))",
          "legendFormat": "{{pod}} - TX",
          "refId": "B"
        }
      ]
    },
    {
      "title": "Pod Restarts",
      "type": "stat",
      "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
      "datasource": "Prometheus",
      "targets": [
        {
          "expr": "kube_pod_container_status_restarts_total{namespace=\"endpoint-stats\"}",
          "legendFormat": "{{pod}}",
          "refId": "A"
        }
      ]
    }
  ],
  "refresh": "10s",
  "schemaVersion": 26,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-1h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "",
  "title": "System Metrics",
  "uid": "system-metrics",
  "version": 1
}
```

#### Kubernetes Deployment

**grafana-deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: endpoint-stats
  labels:
    app: grafana
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      securityContext:
        fsGroup: 472
        supplementalGroups:
          - 0
      containers:
      - name: grafana
        image: grafana/grafana:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 3000
          name: http-grafana
          protocol: TCP
        readinessProbe:
          failureThreshold: 3
          httpGet:
            path: /api/health
            port: 3000
            scheme: HTTP
          periodSeconds: 10
          timeoutSeconds: 1
        livenessProbe:
          failureThreshold: 3
          initialDelaySeconds: 60
          httpGet:
            path: /api/health
            port: 3000
            scheme: HTTP
          periodSeconds: 10
          timeoutSeconds: 1
        resources:
          limits:
            cpu: 200m
            memory: 256Mi
          requests:
            cpu: 100m
            memory: 128Mi
        env:
        - name: GF_AUTH_ANONYMOUS_ENABLED
          value: "true"
        - name: GF_AUTH_ANONYMOUS_ORG_ROLE
          value: "Admin"
        - name: GF_INSTALL_PLUGINS
          value: "grafana-clock-panel,grafana-simple-json-datasource"
        volumeMounts:
        - name: grafana-datasources
          mountPath: /etc/grafana/provisioning/datasources
        - name: grafana-dashboards-config
          mountPath: /etc/grafana/provisioning/dashboards
        - name: grafana-dashboards
          mountPath: /var/lib/grafana/dashboards
        - name: grafana-storage
          mountPath: /var/lib/grafana
      volumes:
      - name: grafana-datasources
        configMap:
          name: grafana-datasources
      - name: grafana-dashboards-config
        configMap:
          name: grafana-dashboards-config
      - name: grafana-dashboards
        configMap:
          name: grafana-dashboards
      - name: grafana-storage
        persistentVolumeClaim:
          claimName: grafana-storage
```

**grafana-service.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: grafana
  namespace: endpoint-stats
spec:
  selector:
    app: grafana
  ports:
  - port: 80
    targetPort: 3000
  type: ClusterIP
```

**grafana-ingress.yaml**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: grafana-ingress
  namespace: endpoint-stats
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /grafana
        pathType: Prefix
        backend:
          service:
            name: grafana
            port:
              number: 80
```

**grafana-pvc.yaml**:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: grafana-storage
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: endpoint-stats-storage
  resources:
    requests:
      storage: 1Gi
```

### 5. Service Integration and Testing

Once all the services are implemented, we need to ensure they integrate correctly with each other. Here is a testing plan for Phase 2:

#### Integration Testing

1. **Database Connection Test**
   ```bash
   # Check if API can connect to PostgreSQL
   kubectl exec -it deployment/flask-api -n endpoint-stats -- curl localhost:9999/health

   # Check if Analytics service can connect to PostgreSQL
   kubectl exec -it deployment/analytics -n endpoint-stats -- curl localhost:5000/health
   ```

2. **Redis Connection Test**
   ```bash
   # Check if API can connect to Redis
   kubectl exec -it deployment/flask-api -n endpoint-stats -- curl localhost:9999/health

   # Check if Rate Limiter can connect to Redis
   kubectl exec -it deployment/rate-limiter -n endpoint-stats -- curl localhost:5000/health
   ```

3. **API Functionality Test**
   ```bash
   # Generate some test traffic
   for i in {1..100}; do
     kubectl exec -it deployment/flask-api -n endpoint-stats -- curl localhost:9999/
     kubectl exec -it deployment/flask-api -n endpoint-stats -- curl localhost:9999/stats
     sleep 0.1
   done
   ```

4. **Rate Limiter Test**
   ```bash
   # Test if rate limiting works
   for i in {1..200}; do
     kubectl exec -it deployment/flask-api -n endpoint-stats -- curl localhost:9999/
     sleep 0.01
   done
   ```

5. **Analytics Collection Test**
   ```bash
   # Check if data is being collected
   kubectl exec -it deployment/analytics -n endpoint-stats -- curl localhost:5000/stats
   ```

6. **Grafana Dashboard Test**
   ```bash
   # Access Grafana through port-forwarding
   kubectl port-forward service/grafana 3000:80 -n endpoint-stats

   # Access in browser: http://localhost:3000
   ```

#### Performance Testing

1. **Load Testing**
   ```bash
   # Install k6 in the API pod for testing
   kubectl exec -it deployment/flask-api -n endpoint-stats -- apt-get update
   kubectl exec -it deployment/flask-api -n endpoint-stats -- apt-get install -y curl

   # Create a simple script
   cat <<EOF > load-test.js
   import http from 'k6/http';
   import { sleep } from 'k6';

   export default function() {
     http.get('http://flask-api/');
     http.get('http://flask-api/stats');
     sleep(0.1);
   }
   EOF

   # Copy script to pod
   kubectl cp load-test.js flask-api-pod:/app/load-test.js -n endpoint-stats

   # Run the test
   kubectl exec -it deployment/flask-api -n endpoint-stats -- k6 run --vus 10 --duration 30s /app/load-test.js
   ```

2. **Cache Performance Test**
   ```bash
   # Test API performance with Redis
   time kubectl exec -it deployment/flask-api -n endpoint-stats -- curl -s localhost:9999/stats > /dev/null

   # Disable Redis temporarily and test again
   kubectl exec -it deployment/flask-api -n endpoint-stats -- bash -c "export REDIS_HOST=none && time curl -s localhost:9999/stats > /dev/null"
   ```

#### Monitoring Integration Test

1. **Check Prometheus Metrics**
   ```bash
   # Get metrics from API
   kubectl exec -it deployment/flask-api -n endpoint-stats -- curl localhost:9999/metrics
   ```

2. **Verify Grafana Dashboards**
   - Access the Grafana UI
   - Check if dashboards are properly loaded
   - Verify data is being displayed
   - Test dashboard filtering and time range selection

With all these tests complete, we can verify that our Phase 2 implementation is working correctly and ready for the next phase of Kubernetes configuration.

## Learning Outcomes

By implementing this project, you'll gain practical experience with:

1. **Kubernetes Core Concepts**
   - Pods, Deployments, StatefulSets, Services
   - ConfigMaps and Secrets
   - Volumes and Persistent Storage
   - Ingress and Service networking

2. **Microservices Architecture**
   - Service communication patterns
   - API design
   - Stateless and stateful services

3. **DevOps Practices**
   - CI/CD workflows
   - Container optimizations
   - Infrastructure as Code

4. **Monitoring and Observability**
   - Metrics collection
   - Dashboard creation
   - Logging and alerting

5. **Performance and Scaling**
   - Horizontal Pod Autoscaling
   - Load testing
   - Resource optimization

---

## Phase 3: Kubernetes Configuration - Detailed Implementation

In this phase, we will set up the core Kubernetes infrastructure components needed for our application. This includes creating namespaces, configuring RBAC permissions, setting up persistent storage, implementing network policies, and establishing security configurations. These components form the foundation for a secure, scalable, and maintainable Kubernetes deployment.

### 1. Namespace and RBAC Configuration

#### Namespace Creation and Organization

Namespaces provide a mechanism to isolate groups of resources within a Kubernetes cluster. For our application, we'll create a dedicated namespace and organize our resources within it.

**namespace.yaml**:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: endpoint-stats
  labels:
    name: endpoint-stats
    environment: production
```

**Benefits of Using Namespaces:**
- Isolation of resources
- Scope for names (allows same resource names in different namespaces)
- Ability to apply resource quotas per namespace
- Simplified access control with RBAC

**Creating the Namespace**:
```bash
kubectl apply -f kubernetes/base/namespace.yaml
```

#### Service Account Configuration

Service accounts provide an identity for processes that run in a Pod.

**service-account.yaml**:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: endpoint-stats-sa
  namespace: endpoint-stats
```

**Creating the Service Account**:
```bash
kubectl apply -f kubernetes/base/service-account.yaml
```

#### Role-Based Access Control (RBAC)

RBAC is a method of regulating access to computer or network resources based on the roles of individual users.

**role.yaml**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: endpoint-stats-role
  namespace: endpoint-stats
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps", "secrets"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments", "statefulsets"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get", "list", "watch"]
```

**rolebinding.yaml**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: endpoint-stats-rolebinding
  namespace: endpoint-stats
subjects:
- kind: ServiceAccount
  name: endpoint-stats-sa
  namespace: endpoint-stats
roleRef:
  kind: Role
  name: endpoint-stats-role
  apiGroup: rbac.authorization.k8s.io
```

**Creating the RBAC Resources**:
```bash
kubectl apply -f kubernetes/base/role.yaml
kubectl apply -f kubernetes/base/rolebinding.yaml
```

#### Resource Quotas

Resource quotas provide constraints that limit aggregate resource consumption per namespace.

**resource-quota.yaml**:
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: endpoint-stats-quota
  namespace: endpoint-stats
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    pods: "20"
    services: "10"
    configmaps: "20"
    secrets: "20"
    persistentvolumeclaims: "10"
```

**Creating the Resource Quota**:
```bash
kubectl apply -f kubernetes/base/resource-quota.yaml
```

#### Limit Ranges

Limit ranges enforce minimum and maximum compute resource usage per Pod or Container in a namespace.

**limit-range.yaml**:
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: endpoint-stats-limits
  namespace: endpoint-stats
spec:
  limits:
  - type: Container
    default:
      memory: 512Mi
      cpu: 500m
    defaultRequest:
      memory: 256Mi
      cpu: 200m
    max:
      memory: 2Gi
      cpu: 2000m
    min:
      memory: 128Mi
      cpu: 100m
  - type: PersistentVolumeClaim
    max:
      storage: 10Gi
    min:
      storage: 1Gi
```

**Creating the Limit Range**:
```bash
kubectl apply -f kubernetes/base/limit-range.yaml
```

#### Namespace Configuration Script

Let's create a script to set up all these resources at once:

**setup-namespace.sh**:
```bash
#!/bin/bash
# scripts/setup-namespace.sh

echo "Creating namespace and RBAC resources..."

# Apply namespace
kubectl apply -f kubernetes/base/namespace.yaml

# Apply service account
kubectl apply -f kubernetes/base/service-account.yaml

# Apply RBAC
kubectl apply -f kubernetes/base/role.yaml
kubectl apply -f kubernetes/base/rolebinding.yaml

# Apply resource constraints
kubectl apply -f kubernetes/base/resource-quota.yaml
kubectl apply -f kubernetes/base/limit-range.yaml

echo "Namespace endpoint-stats configured successfully!"
```

**Make the script executable**:
```bash
chmod +x scripts/setup-namespace.sh
```

### 2. Storage Configuration

#### Understanding Kubernetes Storage Options

For our application, we need persistent storage to maintain data across pod restarts and reschedules. Kubernetes provides several abstraction layers for storage:

1. **PersistentVolume (PV)**: A cluster resource that represents a piece of storage
2. **PersistentVolumeClaim (PVC)**: A request for storage by a user
3. **StorageClass**: Defines different "classes" of storage with different properties

#### Storage Architecture for Our Application

Our application requires storage for:
- PostgreSQL database data
- Redis cache data
- Grafana dashboard configurations

We'll implement storage using:
- Dynamic provisioning with StorageClasses (for cloud environments)
- Minikube's built-in storage for local development

#### Setting Up StorageClass

**storage-class.yaml**:
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: endpoint-stats-storage
  namespace: endpoint-stats
provisioner: k8s.io/minikube-hostpath
reclaimPolicy: Retain
volumeBindingMode: Immediate
parameters:
  type: ssd
```

For cloud environments, you would use the appropriate provisioner:
```yaml
# Example for AWS EBS
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2

# Example for GCE PD
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard

# Example for Azure Disk
provisioner: kubernetes.io/azure-disk
parameters:
  storageaccounttype: Standard_LRS
```

**Create the StorageClass**:
```bash
kubectl apply -f kubernetes/config/storage-class.yaml
```

#### PostgreSQL Persistent Storage

**postgres-pvc.yaml**:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-data
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: endpoint-stats-storage
  resources:
    requests:
      storage: 5Gi
```

**Update PostgreSQL StatefulSet to use the PVC**:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: endpoint-stats
spec:
  serviceName: "postgres"
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
          name: postgres
        env:
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: password
        - name: POSTGRES_DB
          value: endpoint_stats
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "512Mi"
            cpu: "300m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
      volumes:
      - name: postgres-data
        persistentVolumeClaim:
          claimName: postgres-data
```

#### Redis Persistent Storage

**redis-pvc.yaml**:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-data
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: endpoint-stats-storage
  resources:
    requests:
      storage: 2Gi
```

**Update Redis StatefulSet to use the PVC**:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
  namespace: endpoint-stats
spec:
  serviceName: "redis"
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7
        command: ["redis-server", "--appendonly", "yes"]
        ports:
        - containerPort: 6379
          name: redis
        volumeMounts:
        - name: redis-data
          mountPath: /data
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      volumes:
      - name: redis-data
        persistentVolumeClaim:
          claimName: redis-data
```

#### Grafana Persistent Storage

**grafana-pvc.yaml**:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: grafana-storage
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: endpoint-stats-storage
  resources:
    requests:
      storage: 1Gi
```

#### Backup Strategy for Persistent Data

It's important to have a backup strategy for persistent data. Here's a simple backup script for PostgreSQL:

**backup-postgres.sh**:
```bash
#!/bin/bash
# scripts/backup-postgres.sh

TIMESTAMP=$(date +%Y%m%d%H%M%S)
BACKUP_DIR="/backups"
POSTGRES_POD=$(kubectl get pods -n endpoint-stats -l app=postgres -o jsonpath='{.items[0].metadata.name}')

# Create backup
echo "Creating PostgreSQL backup..."
kubectl exec -n endpoint-stats $POSTGRES_POD -- bash -c "mkdir -p $BACKUP_DIR && \
  pg_dump -U postgres endpoint_stats | gzip > $BACKUP_DIR/endpoint_stats_$TIMESTAMP.sql.gz"

# Copy backup to local machine
echo "Copying backup to local machine..."
kubectl cp endpoint-stats/$POSTGRES_POD:$BACKUP_DIR/endpoint_stats_$TIMESTAMP.sql.gz ./endpoint_stats_$TIMESTAMP.sql.gz

echo "Backup completed: ./endpoint_stats_$TIMESTAMP.sql.gz"
```

**Make the script executable**:
```bash
chmod +x scripts/backup-postgres.sh
```

#### Volume Management Script

Let's create a script to manage all our volume operations:

**manage-volumes.sh**:
```bash
#!/bin/bash
# scripts/manage-volumes.sh

function create_volumes() {
  echo "Creating storage class..."
  kubectl apply -f kubernetes/config/storage-class.yaml

  echo "Creating PostgreSQL PVC..."
  kubectl apply -f kubernetes/config/postgres-pvc.yaml

  echo "Creating Redis PVC..."
  kubectl apply -f kubernetes/config/redis-pvc.yaml

  echo "Creating Grafana PVC..."
  kubectl apply -f kubernetes/config/grafana-pvc.yaml

  echo "Waiting for volumes to be bound..."
  kubectl wait --for=condition=Bound pvc/postgres-data -n endpoint-stats --timeout=60s
  kubectl wait --for=condition=Bound pvc/redis-data -n endpoint-stats --timeout=60s
  kubectl wait --for=condition=Bound pvc/grafana-storage -n endpoint-stats --timeout=60s

  echo "All volumes created successfully!"
}

function list_volumes() {
  echo "Listing all PVCs in endpoint-stats namespace:"
  kubectl get pvc -n endpoint-stats

  echo "Listing all PVs used by endpoint-stats namespace:"
  kubectl get pv | grep endpoint-stats
}

function delete_volumes() {
  echo "WARNING: This will delete all persistent volumes and claims!"
  read -p "Are you sure you want to continue? (y/n): " confirm

  if [ "$confirm" == "y" ]; then
    echo "Deleting PVCs..."
    kubectl delete pvc -n endpoint-stats --all

    echo "Waiting for PVs to be released..."
    sleep 10

    echo "Deleting unreleased PVs (if any)..."
    kubectl get pv | grep endpoint-stats | awk '{print $1}' | xargs -r kubectl delete pv

    echo "Volumes deleted."
  else
    echo "Operation canceled."
  fi
}

# Main script
case "$1" in
  create)
    create_volumes
    ;;
  list)
    list_volumes
    ;;
  delete)
    delete_volumes
    ;;
  *)
    echo "Usage: $0 {create|list|delete}"
    exit 1
    ;;
esac
```

**Make the script executable**:
```bash
chmod +x scripts/manage-volumes.sh
```

#### Monitoring Storage Usage

To monitor storage usage, we can create a small script that checks volume utilization:

**check-storage.sh**:
```bash
#!/bin/bash
# scripts/check-storage.sh

POSTGRES_POD=$(kubectl get pods -n endpoint-stats -l app=postgres -o jsonpath='{.items[0].metadata.name}')
REDIS_POD=$(kubectl get pods -n endpoint-stats -l app=redis -o jsonpath='{.items[0].metadata.name}')

echo "PostgreSQL storage usage:"
kubectl exec -n endpoint-stats $POSTGRES_POD -- df -h /var/lib/postgresql/data

echo "Redis storage usage:"
kubectl exec -n endpoint-stats $REDIS_POD -- df -h /data

echo "PVC status:"
kubectl get pvc -n endpoint-stats
```

**Make the script executable**:
```bash
chmod +x scripts/check-storage.sh
```

### 3. Implement network policies and services

#### Network Architecture Overview

The network architecture for our Endpoint Statistics application consists of the following components:

1. **Service Layer**: Exposes pods to other pods and external clients
2. **Network Policies**: Control traffic flow between pods based on labels
3. **Ingress Controller**: Manages external access to the services
4. **Service Mesh (Optional)**: Provides advanced traffic management and observability

Let's implement each of these components.

#### Service Configuration

Services in Kubernetes provide stable endpoints for pods. We'll create services for each component of our application.

**flask-api-service.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-api
  namespace: endpoint-stats
  labels:
    app: flask-api
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/path: "/metrics"
    prometheus.io/port: "9999"
spec:
  selector:
    app: flask-api
  ports:
  - port: 80
    targetPort: 9999
    name: http
  type: ClusterIP
```

**rate-limiter-service.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: rate-limiter
  namespace: endpoint-stats
  labels:
    app: rate-limiter
spec:
  selector:
    app: rate-limiter
  ports:
  - port: 80
    targetPort: 5000
    name: http
  type: ClusterIP
```

**analytics-service.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: analytics
  namespace: endpoint-stats
  labels:
    app: analytics
spec:
  selector:
    app: analytics
  ports:
  - port: 80
    targetPort: 5000
    name: http
  type: ClusterIP
```

**postgres-service.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: endpoint-stats
  labels:
    app: postgres
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
    name: postgres
  type: ClusterIP
```

**redis-service.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: endpoint-stats
  labels:
    app: redis
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
    name: redis
  type: ClusterIP
```

#### Ingress Configuration

Ingress exposes HTTP and HTTPS routes from outside the cluster to services within the cluster.

**ingress.yaml**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: endpoint-stats-ingress
  namespace: endpoint-stats
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$1
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
    nginx.ingress.kubernetes.io/use-regex: "true"
spec:
  rules:
  - http:
      paths:
      - path: /api(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: flask-api
            port:
              number: 80
      - path: /grafana(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: grafana
            port:
              number: 80
```

#### Network Policies

Network Policies specify how groups of pods are allowed to communicate with each other and other network endpoints.

**default-deny.yaml**:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: endpoint-stats
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

**allow-api-traffic.yaml**:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-traffic
  namespace: endpoint-stats
spec:
  podSelector:
    matchLabels:
      app: flask-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 0.0.0.0/0
    ports:
    - protocol: TCP
      port: 9999
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379
  - to:
    - podSelector:
        matchLabels:
          app: rate-limiter
    ports:
    - protocol: TCP
      port: 5000
  - to:
    - podSelector:
        matchLabels:
          app: analytics
    ports:
    - protocol: TCP
      port: 5000
```

**allow-redis-traffic.yaml**:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-redis-traffic
  namespace: endpoint-stats
spec:
  podSelector:
    matchLabels:
      app: redis
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: flask-api
    - podSelector:
        matchLabels:
          app: rate-limiter
    ports:
    - protocol: TCP
      port: 6379
```

**allow-postgres-traffic.yaml**:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-postgres-traffic
  namespace: endpoint-stats
spec:
  podSelector:
    matchLabels:
      app: postgres
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: flask-api
    - podSelector:
        matchLabels:
          app: analytics
    - podSelector:
        matchLabels:
          app: grafana
    ports:
    - protocol: TCP
      port: 5432
```

#### Internal DNS for Service Discovery

Kubernetes provides DNS-based service discovery by default. Here's how our services will resolve:

- `flask-api.endpoint-stats.svc.cluster.local` or simply `flask-api`
- `rate-limiter.endpoint-stats.svc.cluster.local` or simply `rate-limiter`
- `analytics.endpoint-stats.svc.cluster.local` or simply `analytics`
- `postgres.endpoint-stats.svc.cluster.local` or simply `postgres`
- `redis.endpoint-stats.svc.cluster.local` or simply `redis`
- `grafana.endpoint-stats.svc.cluster.local` or simply `grafana`

#### Service Mesh (Optional)

For more complex applications, a service mesh like Istio can provide advanced traffic management, security, and observability features. Here's a basic Istio configuration for our API service:

**flask-api-virtualservice.yaml**:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: flask-api
  namespace: endpoint-stats
spec:
  hosts:
  - "api.example.com"
  gateways:
  - endpoint-stats-gateway
  http:
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: flask-api
        port:
          number: 80
    retries:
      attempts: 3
      perTryTimeout: 2s
    timeout: 10s
```

#### Network Debugging Tools

Let's create a diagnostic pod for network debugging:

**network-debug.yaml**:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: network-debug
  namespace: endpoint-stats
spec:
  containers:
  - name: network-tools
    image: nicolaka/netshoot
    command: ["sleep", "infinity"]
  restartPolicy: Always
```

**debug-network.sh**:
```bash
#!/bin/bash
# scripts/debug-network.sh

POD_NAME="network-debug"
NAMESPACE="endpoint-stats"

# Check if pod exists
kubectl get pod $POD_NAME -n $NAMESPACE >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "Creating network debug pod..."
  kubectl apply -f kubernetes/debug/network-debug.yaml

  echo "Waiting for pod to be ready..."
  kubectl wait --for=condition=Ready pod/$POD_NAME -n $NAMESPACE --timeout=60s
fi

# Start interactive shell
kubectl exec -it $POD_NAME -n $NAMESPACE -- /bin/bash
```

**Make the script executable**:
```bash
chmod +x scripts/debug-network.sh
```

#### Network Configuration Script

Let's create a script to set up all network components:

**setup-network.sh**:
```bash
#!/bin/bash
# scripts/setup-network.sh

echo "Setting up Kubernetes network components..."

# Apply service definitions
echo "Creating services..."
kubectl apply -f kubernetes/services/flask-api-service.yaml
kubectl apply -f kubernetes/services/rate-limiter-service.yaml
kubectl apply -f kubernetes/services/analytics-service.yaml
kubectl apply -f kubernetes/services/postgres-service.yaml
kubectl apply -f kubernetes/services/redis-service.yaml
kubectl apply -f kubernetes/services/grafana-service.yaml

# Apply ingress configuration
echo "Creating ingress..."
kubectl apply -f kubernetes/services/ingress.yaml

# Apply network policies
echo "Creating network policies..."
kubectl apply -f kubernetes/network/default-deny.yaml
kubectl apply -f kubernetes/network/allow-api-traffic.yaml
kubectl apply -f kubernetes/network/allow-redis-traffic.yaml
kubectl apply -f kubernetes/network/allow-postgres-traffic.yaml

echo "Network setup complete!"
```

**Make the script executable**:
```bash
chmod +x scripts/setup-network.sh
```

### 4. Create security configurations

#### ConfigMaps and Secrets

We'll create ConfigMaps and Secrets for our application configuration.

**postgres-secrets.yaml**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-secrets
  namespace: endpoint-stats
data:
  username: postgres
  password: postgres
  database: endpoint_stats
```

**redis-config.yaml**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
  namespace: endpoint-stats
data:
  host: redis
  port: "6379"
```

**rate-limiter-config.yaml**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: rate-limiter-config
  namespace: endpoint-stats
data:
  rate-limits:
    /: 100
    /stats: 60
    /metrics: 200
    default: 120
```

**grafana-config.yaml**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-config
  namespace: endpoint-stats
data:
  admin-user: admin
  admin-password: password
```

#### Security Context

We'll set up security contexts for our containers to ensure they run with the correct permissions.

**flask-api-securitycontext.yaml**:
```yaml
apiVersion: v1
kind: PodSecurityPolicy
metadata:
  name: flask-api-psp
spec:
  privileged: false
  runAsUser:
    rule: RunAsAny
  fsGroup:
    rule: RunAsAny
  seLinux:
    rule: RunAsAny
  supplementalGroups:
    rule: RunAsAny
  volumes:
    - "*"
```

**flask-api-role.yaml**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: flask-api-role
  namespace: endpoint-stats
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch", "create", "update", "delete"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get", "list", "watch"]
```

**flask-api-rolebinding.yaml**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: flask-api-rolebinding
  namespace: endpoint-stats
subjects:
- kind: ServiceAccount
  name: flask-api-sa
  namespace: endpoint-stats
roleRef:
  kind: Role
  name: flask-api-role
  apiGroup: rbac.authorization.k8s.io
```

**flask-api-serviceaccount.yaml**:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: flask-api-sa
  namespace: endpoint-stats
```

**flask-api-deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-api
  namespace: endpoint-stats
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-api
  template:
    metadata:
      labels:
        app: flask-api
    spec:
      securityContext:
        runAsUser: 1000
        runAsGroup: 3000
        fsGroup: 3000
      containers:
      - name: flask-api
        image: flask-api:latest
        env:
        - name: DATABASE_URL
          value: postgresql://postgres:postgres@postgres:5432/endpoint_stats
        - name: REDIS_HOST
          value: redis
        - name: REDIS_PORT
          value: "6379"
        - name: ANALYTICS_URL
          value: http://analytics:5000
        ports:
        - containerPort: 9999
          name: http
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
        - name: redis-data
          mountPath: /data
        - name: grafana-dashboards
          mountPath: /var/lib/grafana/dashboards
        - name: grafana-storage
          mountPath: /var/lib/grafana
      volumes:
      - name: postgres-data
        persistentVolumeClaim:
          claimName: postgres-data
      - name: redis-data
        persistentVolumeClaim:
          claimName: redis-data
      - name: grafana-dashboards
        persistentVolumeClaim:
          claimName: grafana-storage
      - name: grafana-storage
        persistentVolumeClaim:
          claimName: grafana-storage
```

**rate-limiter-securitycontext.yaml**:
```yaml
apiVersion: v1
kind: PodSecurityPolicy
metadata:
  name: rate-limiter-psp
spec:
  privileged: false
  runAsUser:
    rule: RunAsAny
  fsGroup:
    rule: RunAsAny
  seLinux:
    rule: RunAsAny
  supplementalGroups:
    rule: RunAsAny
  volumes:
    - "*"
```

**rate-limiter-role.yaml**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: rate-limiter-role
  namespace: endpoint-stats
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch", "create", "update", "delete"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get", "list", "watch"]
```

**rate-limiter-rolebinding.yaml**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: rate-limiter-rolebinding
  namespace: endpoint-stats
subjects:
- kind: ServiceAccount
  name: rate-limiter-sa
  namespace: endpoint-stats
roleRef:
  kind: Role
  name: rate-limiter-role
  apiGroup: rbac.authorization.k8s.io
```

**rate-limiter-serviceaccount.yaml**:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rate-limiter-sa
  namespace: endpoint-stats
```

**rate-limiter-deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rate-limiter
  namespace: endpoint-stats
spec:
  replicas: 1
  selector:
    matchLabels:
      app: rate-limiter
  template:
    metadata:
      labels:
        app: rate-limiter
    spec:
      securityContext:
        runAsUser: 1000
        runAsGroup: 3000
        fsGroup: 3000
      containers:
      - name: rate-limiter
        image: rate-limiter:latest
        env:
        - name: REDIS_HOST
          value: redis
        - name: REDIS_PORT
          value: "6379"
        ports:
        - containerPort: 5000
          name: http
        volumeMounts:
        - name: redis-data
          mountPath: /data
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      volumes:
      - name: redis-data
        persistentVolumeClaim:
          claimName: redis-data
```

**analytics-securitycontext.yaml**:
```yaml
apiVersion: v1
kind: PodSecurityPolicy
metadata:
  name: analytics-psp
spec:
  privileged: false
  runAsUser:
    rule: RunAsAny
  fsGroup:
    rule: RunAsAny
  seLinux:
    rule: RunAsAny
  supplementalGroups:
    rule: RunAsAny
  volumes:
    - "*"
```

**analytics-role.yaml**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: analytics-role
  namespace: endpoint-stats
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch", "create", "update", "delete"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get", "list", "watch"]
```

**analytics-rolebinding.yaml**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: analytics-rolebinding
  namespace: endpoint-stats
subjects:
- kind: ServiceAccount
  name: analytics-sa
  namespace: endpoint-stats
roleRef:
  kind: Role
  name: analytics-role
  apiGroup: rbac.authorization.k8s.io
```

**analytics-serviceaccount.yaml**:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: analytics-sa
  namespace: endpoint-stats
```

**analytics-deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: analytics
  namespace: endpoint-stats
spec:
  replicas: 1
  selector:
    matchLabels:
      app: analytics
  template:
    metadata:
      labels:
        app: analytics
    spec:
      securityContext:
        runAsUser: 1000
        runAsGroup: 3000
        fsGroup: 3000
      containers:
      - name: analytics
        image: analytics:latest
        env:
        - name: POSTGRES_HOST
          value: postgres
        - name: POSTGRES_USER
          value: postgres
        - name: POSTGRES_PASSWORD
          value: postgres
        - name: POSTGRES_DB
          value: endpoint_stats
        ports:
        - containerPort: 5000
          name: http
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "512Mi"
            cpu: "300m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
      volumes:
      - name: postgres-data
        persistentVolumeClaim:
          claimName: postgres-data
```

**postgres-securitycontext.yaml**:
```yaml
apiVersion: v1
kind: PodSecurityPolicy
metadata:
  name: postgres-psp
spec:
  privileged: false
  runAsUser:
    rule: RunAsAny
  fsGroup:
    rule: RunAsAny
  seLinux:
    rule: RunAsAny
  supplementalGroups:
    rule: RunAsAny
  volumes:
    - "*"
```

**postgres-role.yaml**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: postgres-role
  namespace: endpoint-stats
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch", "create", "update", "delete"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get", "list", "watch"]
```

**postgres-rolebinding.yaml**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: postgres-rolebinding
  namespace: endpoint-stats
subjects:
- kind: ServiceAccount
  name: postgres-sa
  namespace: endpoint-stats
roleRef:
  kind: Role
  name: postgres-role
  apiGroup: rbac.authorization.k8s.io
```

**postgres-serviceaccount.yaml**:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: postgres-sa
  namespace: endpoint-stats
```

**postgres-deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: endpoint-stats
spec:
  serviceName: "postgres"
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      securityContext:
        runAsUser: 1000
        runAsGroup: 3000
        fsGroup: 3000
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
          name: postgres
        env:
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: password
        - name: POSTGRES_DB
          value: endpoint_stats
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "512Mi"
            cpu: "300m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
      volumes:
      - name: postgres-data
        persistentVolumeClaim:
          claimName: postgres-data
```

**redis-securitycontext.yaml**:
```yaml
apiVersion: v1
kind: PodSecurityPolicy
metadata:
  name: redis-psp
spec:
  privileged: false
  runAsUser:
    rule: RunAsAny
  fsGroup:
    rule: RunAsAny
  seLinux:
    rule: RunAsAny
  supplementalGroups:
    rule: RunAsAny
  volumes:
    - "*"
```

**redis-role.yaml**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: redis-role
  namespace: endpoint-stats
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch", "create", "update", "delete"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get", "list", "watch"]
```

**redis-rolebinding.yaml**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: redis-rolebinding
  namespace: endpoint-stats
subjects:
- kind: ServiceAccount
  name: redis-sa
  namespace: endpoint-stats
roleRef:
  kind: Role
  name: redis-role
  apiGroup: rbac.authorization.k8s.io
```

**redis-serviceaccount.yaml**:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: redis-sa
  namespace: endpoint-stats
```

**redis-deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
  namespace: endpoint-stats
spec:
  serviceName: "redis"
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      securityContext:
        runAsUser: 1000
        runAsGroup: 3000
        fsGroup: 3000
      containers:
      - name: redis
        image: redis:7
        command: ["redis-server", "--appendonly", "yes"]
        ports:
        - containerPort: 6379
          name: redis
        volumeMounts:
        - name: redis-data
          mountPath: /data
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      volumes:
      - name: redis-data
        persistentVolumeClaim:
          claimName: redis-data
```

**grafana-securitycontext.yaml**:
```yaml
apiVersion: v1
kind: PodSecurityPolicy
metadata:
  name: grafana-psp
spec:
  privileged: false
  runAsUser:
    rule: RunAsAny
  fsGroup:
    rule: RunAsAny
  seLinux:
    rule: RunAsAny
  supplementalGroups:
    rule: RunAsAny
  volumes:
    - "*"
```

**grafana-role.yaml**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: grafana-role
  namespace: endpoint-stats
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch", "create", "update", "delete"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get", "list", "watch"]
```

**grafana-rolebinding.yaml**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: grafana-rolebinding
  namespace: endpoint-stats
subjects:
- kind: ServiceAccount
  name: grafana-sa
  namespace: endpoint-stats
roleRef:
  kind: Role
  name: grafana-role
  apiGroup: rbac.authorization.k8s.io
```

**grafana-serviceaccount.yaml**:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: grafana-sa
  namespace: endpoint-stats
```

**grafana-deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: endpoint-stats
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      securityContext:
        runAsUser: 1000
        runAsGroup: 3000
        fsGroup: 3000
      containers:
      - name: grafana
        image: grafana/grafana:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 3000
          name: http-grafana
          protocol: TCP
        readinessProbe:
          failureThreshold: 3
          httpGet:
            path: /api/health
            port: 3000
            scheme: HTTP
          periodSeconds: 10
          timeoutSeconds: 1
        livenessProbe:
          failureThreshold: 3
          initialDelaySeconds: 60
          httpGet:
            path: /api/health
            port: 3000
            scheme: HTTP
          periodSeconds: 10
          timeoutSeconds: 1
        resources:
          limits:
            cpu: 200m
            memory: 256Mi
          requests:
            cpu: 100m
            memory: 128Mi
        env:
        - name: GF_AUTH_ANONYMOUS_ENABLED
          value: "true"
        - name: GF_AUTH_ANONYMOUS_ORG_ROLE
          value: "Admin"
        - name: GF_INSTALL_PLUGINS
          value: "grafana-clock-panel,grafana-simple-json-datasource"
        volumeMounts:
        - name: grafana-datasources
          mountPath: /etc/grafana/provisioning/datasources
        - name: grafana-dashboards-config
          mountPath: /etc/grafana/provisioning/dashboards
        - name: grafana-dashboards
          mountPath: /var/lib/grafana/dashboards
        - name: grafana-storage
          mountPath: /var/lib/grafana
      volumes:
      - name: grafana-datasources
        configMap:
          name: grafana-datasources
      - name: grafana-dashboards-config
        configMap:
          name: grafana-dashboards-config
      - name: grafana-dashboards
        configMap:
          name: grafana-dashboards
      - name: grafana-storage
        persistentVolumeClaim:
          claimName: grafana-storage
```

**grafana-service.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: grafana
  namespace: endpoint-stats
spec:
  selector:
    app: grafana
  ports:
  - port: 80
    targetPort: 3000
  type: ClusterIP
```

**grafana-ingress.yaml**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: grafana-ingress
  namespace: endpoint-stats
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /grafana
        pathType: Prefix
        backend:
          service:
            name: grafana
            port:
              number: 80
```

**grafana-pvc.yaml**:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: grafana-storage
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: endpoint-stats-storage
  resources:
    requests:
      storage: 1Gi
```

## Learning Outcomes

By implementing this project, you'll gain practical experience with:

1. **Kubernetes Core Concepts**
   - Pods, Deployments, StatefulSets, Services
   - ConfigMaps and Secrets
   - Volumes and Persistent Storage
   - Ingress and Service networking

2. **Microservices Architecture**
   - Service communication patterns
   - API design
   - Stateless and stateful services

3. **DevOps Practices**
   - CI/CD workflows
   - Container optimizations
   - Infrastructure as Code

4. **Monitoring and Observability**
   - Metrics collection
   - Dashboard creation
   - Logging and alerting

5. **Performance and Scaling**
   - Horizontal Pod Autoscaling
   - Load testing
   - Resource optimization

---

## Phase 4: Deployment Strategy - Detailed Implementation

In this phase, we'll set up the initial deployment sequence, rolling update configuration, scaling rules, and health checks. We'll also implement autoscaling based on CPU/memory utilization.

### 1. Initial Deployment Sequence

We'll deploy our services in a specific order to ensure dependencies are met.

1. **PostgreSQL**: Database service
2. **Redis**: Caching service
3. **Flask API**: Main application service
4. **Rate Limiter**: API rate limiting service
5. **Analytics**: Analytics service
6. **Grafana**: Dashboard visualization service

### 2. Rolling Update Configuration

Rolling updates allow us to deploy new versions of our services without downtime.

**Rolling Update Strategy**:
- New pods are created one at a time
- Old pods are terminated one at a time
- New pods are verified before being promoted to production

### 3. Scaling Rules and Autoscaling

We'll set up scaling rules for each service based on their requirements.

- **Flask API**: Scales based on incoming traffic
- **Rate Limiter**: Scales based on incoming traffic
- **Analytics**: Scales based on incoming traffic
- **Grafana**: Scales based on incoming traffic

**Horizontal Pod Autoscaling (HPA)**:
- Automatically scales the number of pods based on CPU/memory utilization

### 4. Health Checks and Probes

We'll set up health checks and probes for each service to ensure they're running correctly.

- **Liveness Probe**: Checks if a pod is still responsive
- **Readiness Probe**: Checks if a pod is ready to receive traffic

### 5. Autoscaling Configuration

We'll set up autoscaling rules for each service based on their requirements.

- **Flask API**: Scales based on incoming traffic
- **Rate Limiter**: Scales based on incoming traffic
- **Analytics**: Scales based on incoming traffic
- **Grafana**: Scales based on incoming traffic

## Learning Outcomes

By implementing this project, you'll gain practical experience with:

1. **Kubernetes Core Concepts**
   - Pods, Deployments, StatefulSets, Services
   - ConfigMaps and Secrets
   - Volumes and Persistent Storage
   - Ingress and Service networking

2. **Microservices Architecture**
   - Service communication patterns
   - API design
   - Stateless and stateful services

3. **DevOps Practices**
   - CI/CD workflows
   - Container optimizations
   - Infrastructure as Code

4. **Monitoring and Observability**
   - Metrics collection
   - Dashboard creation
   - Logging and alerting

5. **Performance and Scaling**
   - Horizontal Pod Autoscaling
   - Load testing
   - Resource optimization

---

## Phase 5: Monitoring and Maintenance - Detailed Implementation

In this phase, we'll set up Grafana dashboards for monitoring and alerting, implement backup procedures, and establish update strategies.

### 1. Grafana Dashboard Setup

We'll set up Grafana dashboards to visualize our application's performance and health.

**Grafana Dashboard Configuration**:
- **API Usage**: Visualizes API usage statistics
- **System Metrics**: Shows CPU, memory, network, and pod usage
- **Error Rate**: Shows error rates for different endpoints
- **Endpoint Distribution**: Shows geographic distribution of API requests

### 2. Backup Procedures

We'll set up a backup procedure for our application data.

**Backup Strategy**:
- **PostgreSQL**: Backup PostgreSQL data daily
- **Redis**: Backup Redis data daily
- **Grafana**: Backup Grafana dashboards daily

### 3. Update Strategies

We'll establish update strategies for our services.

**Blue-Green Deployment**:
- Deploy new versions of services side-by-side
- Test new versions in a staging environment
- Switch traffic to new version only if tests are successful

**Rolling Update**:
- Deploy new versions of services one at a time
- Old versions are gradually replaced with new versions

### 4. Troubleshooting Guides

We'll create troubleshooting guides for common issues.

**Common Issues**:
- **Database Connection**: Troubleshooting PostgreSQL connection issues
- **Redis Connection**: Troubleshooting Redis connection issues
- **Service Unavailability**: Identifying and resolving service unavailability
- **Performance Degradation**: Identifying and resolving performance issues

## Learning Outcomes

By implementing this project, you'll gain practical experience with:

1. **Kubernetes Core Concepts**
   - Pods, Deployments, StatefulSets, Services
   - ConfigMaps and Secrets
   - Volumes and Persistent Storage
   - Ingress and Service networking

2. **Microservices Architecture**
   - Service communication patterns
   - API design
   - Stateless and stateful services

3. **DevOps Practices**
   - CI/CD workflows
   - Container optimizations
   - Infrastructure as Code

4. **Monitoring and Observability**
   - Metrics collection
   - Dashboard creation
   - Logging and alerting

5. **Performance and Scaling**
   - Horizontal Pod Autoscaling
   - Load testing
   - Resource optimization

---

## Phase 6: Final Deployment and Testing

In this phase, we'll deploy our application to a production environment and perform final testing.

### 1. Final Deployment

We'll deploy our application to a production environment.

**Production Environment**:
- **Kubernetes Cluster**: Production-grade Kubernetes cluster
- **Ingress Controller**: Configured for external access
- **Service Mesh**: Integrated with Istio for advanced traffic management

### 2. Final Testing

We'll perform final testing to ensure our application is ready for production.

**Testing Strategy**:
- **Load Testing**: Test application under production load
- **Stress Testing**: Test application under extreme load
- **Security Testing**: Test application for security vulnerabilities
- **Performance Testing**: Test application performance under production conditions

## Learning Outcomes

By implementing this project, you'll gain practical experience with:

1. **Kubernetes Core Concepts**
   - Pods, Deployments, StatefulSets, Services
   - ConfigMaps and Secrets
   - Volumes and Persistent Storage
   - Ingress and Service networking

2. **Microservices Architecture**
   - Service communication patterns
   - API design
   - Stateless and stateful services

3. **DevOps Practices**
   - CI/CD workflows
   - Container optimizations
   - Infrastructure as Code

4. **Monitoring and Observability**
   - Metrics collection
   - Dashboard creation
   - Logging and alerting

5. **Performance and Scaling**
   - Horizontal Pod Autoscaling
   - Load testing
   - Resource optimization

---

## Common Issues and Troubleshooting

During the implementation of this project, you might encounter various issues. Here are some common problems and their solutions:

### Minikube Issues

1. **Insufficient Resources**
   - **Problem**: Minikube fails to start due to insufficient resources
   - **Solution**: Increase the resources allocated to Minikube:
     ```bash
     minikube delete
     minikube start --cpus=4 --memory=8192 --disk-size=20g
     ```

2. **Driver Issues**
   - **Problem**: Default driver doesn't work on your system
   - **Solution**: Try alternative drivers:
     ```bash
     minikube start --driver=docker
     # or
     minikube start --driver=virtualbox
     ```

3. **Network Issues**
   - **Problem**: Unable to pull images
   - **Solution**: Use the Minikube Docker daemon:
     ```bash
     eval $(minikube docker-env)
     ```

### Kubernetes Issues

1. **PersistentVolumeClaim Not Binding**
   - **Problem**: PVCs remain in Pending state
   - **Solution**: Check StorageClass configuration and make sure dynamic provisioning is enabled:
     ```bash
     kubectl get sc
     kubectl describe pvc <pvc-name> -n endpoint-stats
     ```

2. **Service Discovery Issues**
   - **Problem**: Services cannot communicate with each other
   - **Solution**: Verify network policies and DNS resolution:
     ```bash
     kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -n endpoint-stats -- bash
     # Then use dig, curl, etc. to test connectivity
     ```

3. **Pod Crashes or CrashLoopBackOff**
   - **Problem**: Containers keep restarting
   - **Solution**: Check logs and events:
     ```bash
     kubectl logs <pod-name> -n endpoint-stats
     kubectl describe pod <pod-name> -n endpoint-stats
     ```

### Application Issues

1. **Database Connection Failures**
   - **Problem**: API service cannot connect to PostgreSQL
   - **Solution**: Verify secrets, environment variables, and network policies:
     ```bash
     kubectl exec -it <api-pod-name> -n endpoint-stats -- env | grep DATABASE
     kubectl exec -it <api-pod-name> -n endpoint-stats -- ping postgres
     ```

2. **Redis Connection Issues**
   - **Problem**: Rate limiter cannot connect to Redis
   - **Solution**: Check Redis service and network policies:
     ```bash
     kubectl exec -it <rate-limiter-pod-name> -n endpoint-stats -- redis-cli -h redis ping
     ```

3. **Grafana Dashboard Not Loading**
   - **Problem**: Unable to view Grafana dashboards
   - **Solution**: Check ingress configuration and Grafana deployment:
     ```bash
     kubectl port-forward svc/grafana 3000:80 -n endpoint-stats
     # Then access http://localhost:3000 in your browser
     ```

### Advanced Debugging Techniques

For more complex issues, use these advanced debugging techniques:

1. **Interactive Debugging Pod**
   ```bash
   kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -n endpoint-stats -- bash
   ```

2. **Monitoring Network Traffic**
   ```bash
   kubectl exec -it <pod-name> -n endpoint-stats -- tcpdump -i any -n
   ```

3. **Checking Resource Usage**
   ```bash
   kubectl top pods -n endpoint-stats
   kubectl top nodes
   ```

4. **Verbose Kubernetes API Logs**
   ```bash
   kubectl get events -n endpoint-stats --sort-by='.lastTimestamp'
   ```

If you encounter issues not covered here, consult the [Kubernetes Troubleshooting Guide](https://kubernetes.io/docs/tasks/debug/debug-application/) or the relevant service documentation.

---

## Final Thoughts

This project provides a comprehensive overview of implementing a microservices architecture on Kubernetes. By following this plan, you'll gain practical experience with Kubernetes core concepts, microservices architecture, DevOps practices, monitoring and observability, performance and scaling, and deployment strategies.

---

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Microservices Architecture](https://microservices.io/)
- [DevOps Practices](https://www.devopsinstitute.com/)
- [Monitoring and Observability](https://www.oreilly.com/library/view/monitoring-and-observability/)
- [Performance and Scaling](https://www.oreilly.com/library/view/performance-and-scaling/)

---

## Conclusion

This project provides a comprehensive overview of implementing a microservices architecture on Kubernetes. By following this plan, you'll gain practical experience with Kubernetes core concepts, microservices architecture, DevOps practices, monitoring and observability, performance and scaling, and deployment strategies.

---

## Next Steps

- **Continuous Integration/Continuous Deployment (CI/CD)**: Set up CI/CD pipelines for automated testing and deployment
- **Service Mesh**: Integrate with a service mesh like Istio for advanced traffic management and observability
- **Monitoring and Alerting**: Set up more advanced monitoring and alerting solutions
- **Performance Optimization**: Optimize application performance under production conditions

---

## Acknowledgments

- **Kubernetes Community**: For providing a powerful and flexible container orchestration platform
- **Microservices Community**: For promoting the benefits of microservices architecture
- **DevOps Community**: For sharing best practices in DevOps practices
- **Monitoring and Observability Community**: For sharing insights on monitoring and observability
- **Performance and Scaling Community**: For sharing best practices in performance and scaling

---

## Contact Information

- **Project Lead**: [Your Name](mailto:your.email@example.com)
- **Project Contributors**: [List of Contributors](https://github.com/your-project/contributors)
- **Project Repository**: [GitHub Repository](https://github.com/your-project)

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
