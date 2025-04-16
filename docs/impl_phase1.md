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
---
apiVersion: v1
kind: Namespace
metadata:
  name: endpoint-stats  # Unique identifier for the namespace
  labels:
    name: endpoint-stats  # Label that can be used for selecting this namespace
```

### 2. Storage Configuration

Before deploying stateful applications, we need to configure persistent storage to ensure data isn't lost when pods restart.

```yaml
# persistent-volumes.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgres-pv  # Persistent volume for PostgreSQL database
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce  # Only one node can mount the volume as read-write
  capacity:
    storage: 100Mi   # Storage capacity for the PostgreSQL database
  hostPath:
    path: /data/postgres-pv  # Path on the host where data is stored
  storageClassName: standard  # Default storage class

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc  # Name referenced by the PostgreSQL deployment
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Mi  # Must match or be less than the PV capacity
  storageClassName: standard

---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: redis-pv  # Persistent volume for Redis cache
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 100Mi  # Storage capacity for Redis data
  hostPath:
    path: /data/redis-pv  # Path on the host where data is stored
  storageClassName: standard

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc  # Name referenced by the Redis deployment
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Mi  # Must match or be less than the PV capacity
  storageClassName: standard
```

### 3. Database Setup

PostgreSQL serves as the primary data store for the application, storing endpoint access patterns, response times, and error rates.

```yaml
# postgres.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: endpoint-stats
spec:
  replicas: 1  # Single instance for development; use StatefulSet for production
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres  # Label used by the service for routing traffic
    spec:
      containers:
        - name: postgres
          image: postgres:15  # Latest stable PostgreSQL 15.x
          ports:
            - containerPort: 5432  # Standard PostgreSQL port
          env:
            - name: POSTGRES_PASSWORD
              value: postgres  # In production, should use a Secret instead
          resources:
            requests:
              cpu: 100m        # 0.1 CPU cores, minimum needed for PostgreSQL
              memory: 100Mi    # 100MB minimum memory for PostgreSQL
            limits:
              cpu: 100m        # Limit to prevent resource starvation
              memory: 100Mi    # Memory limit to prevent excessive usage
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql/data  # Standard PostgreSQL data directory
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-pvc  # Reference to the PVC defined earlier

---
# Service to expose PostgreSQL within the cluster
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: endpoint-stats
spec:
  selector:
    app: postgres  # Matches the label on the PostgreSQL pod
  ports:
    - protocol: TCP
      port: 5432       # Port the service exposes
      targetPort: 5432  # Port in the container to forward to
```

### 4. Redis Setup

Redis provides caching to reduce database load and enables real-time tracking of active requests and rate limiting.

```yaml
# redis.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: endpoint-stats
spec:
  replicas: 1  # Single instance for development; consider Redis Cluster for production
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis  # Label used by service for routing traffic
    spec:
      containers:
        - name: redis
          image: redis:latest  # Using the latest stable Redis image
          ports:
            - containerPort: 6379  # Standard Redis port
          resources:
            requests:
              cpu: 100m       # 0.1 CPU cores, sufficient for basic Redis usage
              memory: 100Mi   # 100MB minimum memory for Redis
            limits:
              cpu: 100m       # Limit to prevent resource starvation
              memory: 100Mi   # Memory limit to prevent excessive usage
          args: ["--appendonly", "yes"]  # Enable persistence mode for Redis
          volumeMounts:
            - name: redis-storage
              mountPath: /data  # Standard Redis data directory
      volumes:
        - name: redis-storage
          persistentVolumeClaim:
            claimName: redis-pvc  # Reference to the PVC defined earlier

---
# Service to expose Redis within the cluster
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: endpoint-stats
spec:
  selector:
    app: redis  # Matches the label on the Redis pod
  ports:
    - protocol: TCP
      port: 6379       # Port the service exposes
      targetPort: 6379  # Port in the container to forward to
```

### 5. Flask API Setup

The Flask API serves as the application backend, processing and storing endpoint statistics while providing a REST API for data access.

```yaml
# flask-api.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-api
  namespace: endpoint-stats
spec:
  replicas: 2  # Run two instances for high availability
  selector:
    matchLabels:
      app: flask-api
  template:
    metadata:
      labels:
        app: flask-api  # Label used by service for routing traffic
      annotations:
        prometheus.io/scrape: "true"  # Enable Prometheus scraping
        prometheus.io/path: "/metrics"  # Path where metrics are exposed
        prometheus.io/port: "9999"  # Port where metrics are exposed
    spec:
      containers:
        - name: flask-api
          image: endpoint-stats:v2  # Use versioned tag to avoid cache issues
          imagePullPolicy: Never  # For local Minikube development only
          ports:
            - containerPort: 9999  # Port the container listens on
          resources:
            requests:
              cpu: 100m     # Minimum CPU required for Flask
              memory: 100Mi  # Minimum memory required for Flask
            limits:
              cpu: 100m     # Maximum CPU allowed
              memory: 100Mi  # Maximum memory allowed
          livenessProbe:  # Ensures container is restarted if it becomes unresponsive
            httpGet:
              path: /health  # Health check endpoint
              port: 9999
            initialDelaySeconds: 5  # Wait time before first probe
            periodSeconds: 10  # Frequency of probes
          env:
            - name: DATABASE_URL  # Connection string for PostgreSQL
              value: postgresql://postgres:postgres@postgres:5432/postgres
            - name: REDIS_URL  # Connection string for Redis
              value: redis://redis:6379/0
          envFrom:
            - secretRef:
                name: flask-api-secret  # Reference to the Secret for credentials
---
# Service to expose the Flask API within the cluster
apiVersion: v1
kind: Service
metadata:
  name: flask-api
  namespace: endpoint-stats
spec:
  selector:
    app: flask-api  # Match pods with this label
  ports:
    - protocol: TCP
      port: 9999  # Port the service exposes
      targetPort: 9999  # Port to forward to in the pods
```

### 6. Ingress Setup

Ingress exposes HTTP and HTTPS routes from outside the cluster to services within the cluster, providing external access to the API.

```yaml
# ingress.yaml
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-api-ingress
  namespace: endpoint-stats
spec:
  rules:
    - host: api.endpoint-stats.com  # Domain name to access the API
      http:
        paths:
          - path: /                 # Match all paths starting with /
            pathType: Prefix        # Type of path matching (Prefix, Exact, or ImplementationSpecific)
            backend:
              service:
                name: flask-api     # Service to route traffic to
                port:
                  number: 9999      # Port on the service to route traffic to
```

### 7. Secrets Management

Securely manage sensitive information such as database credentials and API keys.

```yaml
# secrets.yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: flask-api-secret  # Name referenced by the Flask API deployment
  namespace: endpoint-stats
type: Opaque  # Generic secret type for arbitrary data
data:
  # Base64 encoded credentials - in production, these should be generated securely
  DB_USER: dXNlcg==      # "user" in base64
  DB_PASSWORD: cGFzc3dvcmQ=  # "password" in base64
```

## Basic Security Considerations

- Limit container privileges by setting proper security contexts
- Use network policies to control pod-to-pod communication
- Create separate service accounts with minimum required permissions
- Store sensitive data in Kubernetes secrets
- Regularly update container images to include security patches

## Implementation Checklist

- [x] Create namespace
- [x] Create persistent volume claims
- [x] Deploy PostgreSQL
- [x] Deploy Redis
- [x] Deploy Flask API
- [x] Configure Ingress
- [x] Set up secrets
- [x] Verify connectivity between services
- [x] Test basic API functionality
- [x] Validate resource limits are appropriate

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
