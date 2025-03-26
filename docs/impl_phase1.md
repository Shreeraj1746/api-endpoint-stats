# Phase 1: Basic Infrastructure Setup

## Overview
This phase focuses on setting up the core infrastructure components for the Endpoint Statistics application. We'll create the necessary Kubernetes resources and establish the basic application structure. This phase provides the foundation that all other phases will build upon.

## Technology Choices
- **PostgreSQL**: Selected for its reliability, ACID compliance, and robust feature set for storing structured endpoint statistics data. It provides excellent performance for complex queries that will be needed for statistical analysis.
- **Redis**: Used as a caching layer and message broker to improve application performance and handle high request volumes. Redis's in-memory data structure store is ideal for tracking real-time metrics.
- **Flask API**: A lightweight and flexible Python web framework that enables rapid development and easy integration with PostgreSQL and Redis.
- **Nginx Ingress**: Provides external access to services with features like path-based routing, load balancing, and TLS termination.

## Implementation Steps

### 1. Namespace Setup
A dedicated namespace isolates the application resources, providing better resource management and access control.

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: endpoint-stats
  labels:
    name: endpoint-stats
```

### 2. Storage Configuration
Before deploying stateful applications, we need to configure persistent storage to ensure data isn't lost when pods restart.

```yaml
# persistent-volumes.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: standard
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

### 3. Database Setup
PostgreSQL serves as the primary data store for the application, storing endpoint access patterns, response times, and error rates.

```yaml
# postgres-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: endpoint-stats
spec:
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
        image: postgres:14
        env:
        - name: POSTGRES_DB
          value: endpoint_stats
        - name: POSTGRES_USER
          value: admin
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "200m"
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
```

```yaml
# postgres-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: endpoint-stats
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP
```

### 4. Redis Setup
Redis provides caching to reduce database load and enables real-time tracking of active requests and rate limiting.

```yaml
# redis-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: endpoint-stats
spec:
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
        image: redis:6
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-storage
          mountPath: /data
        resources:
          requests:
            memory: "128Mi"
            cpu: "50m"
          limits:
            memory: "256Mi"
            cpu: "100m"
        args: ["--appendonly", "yes"]  # Enable persistence
      volumes:
      - name: redis-storage
        persistentVolumeClaim:
          claimName: redis-pvc
```

```yaml
# redis-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: endpoint-stats
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
  type: ClusterIP
```

### 5. Flask API Setup
The Flask API serves as the application backend, processing and storing endpoint statistics while providing a REST API for data access.

```yaml
# flask-api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-api
  namespace: endpoint-stats
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-api
  template:
    metadata:
      labels:
        app: flask-api
    spec:
      containers:
      - name: flask-api
        image: your-registry/flask-api:latest
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URL
          value: postgresql://admin:$(POSTGRES_PASSWORD)@postgres:5432/endpoint_stats
        - name: REDIS_URL
          value: redis://redis:6379/0
        envFrom:
        - secretRef:
            name: flask-secrets
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 5
```

```yaml
# flask-api-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-api
  namespace: endpoint-stats
spec:
  selector:
    app: flask-api
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

### 6. Ingress Setup
Ingress exposes HTTP and HTTPS routes from outside the cluster to services within the cluster, providing external access to the API.

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: endpoint-stats-ingress
  namespace: endpoint-stats
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  rules:
  - host: api.endpoint-stats.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: flask-api
            port:
              number: 80
```

### 7. Secrets Management
Securely manage sensitive information such as database credentials and API keys.

```yaml
# secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: endpoint-stats
type: Opaque
data:
  password: <base64-encoded-password>  # Use 'echo -n "YourPassword" | base64' to generate
---
apiVersion: v1
kind: Secret
metadata:
  name: flask-secrets
  namespace: endpoint-stats
type: Opaque
data:
  POSTGRES_PASSWORD: <base64-encoded-password>
  API_KEY: <base64-encoded-api-key>
```

## Basic Security Considerations
- Limit container privileges by setting proper security contexts
- Use network policies to control pod-to-pod communication
- Create separate service accounts with minimum required permissions
- Store sensitive data in Kubernetes secrets
- Regularly update container images to include security patches

## Implementation Checklist
- [ ] Create namespace
- [ ] Create persistent volume claims
- [ ] Deploy PostgreSQL
- [ ] Deploy Redis
- [ ] Deploy Flask API
- [ ] Configure Ingress
- [ ] Set up secrets
- [ ] Verify connectivity between services
- [ ] Test basic API functionality
- [ ] Validate resource limits are appropriate

## Troubleshooting Tips
1. **Pod Startup Issues**:
   ```bash
   kubectl describe pod <pod-name> -n endpoint-stats
   ```
   Check the events section for errors.

2. **Container Logs**:
   ```bash
   kubectl logs <pod-name> -n endpoint-stats
   ```
   Review logs for application errors.

3. **Database Connection Issues**:
   - Verify the PostgreSQL pod is running
   - Check if the service resolves correctly:
     ```bash
     kubectl exec -it <any-pod> -n endpoint-stats -- nslookup postgres
     ```
   - Verify credentials are correct in secrets

4. **Service Discovery Problems**:
   ```bash
   kubectl get endpoints -n endpoint-stats
   ```
   Ensure endpoints are populated for each service.

5. **PVC Issues**:
   ```bash
   kubectl get pvc -n endpoint-stats
   ```
   Check if PVCs are in "Bound" state.

## Next Steps
After completing Phase 1, proceed to [Phase 2: Monitoring and Observability](impl_phase2.md) to set up comprehensive monitoring for the application.
