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
  name: endpoint-stats
  labels:
    name: endpoint-stats
```

### 2. Storage Configuration

Before deploying stateful applications, we need to configure persistent storage to ensure data isn't lost when pods restart.

```yaml
# persistent-volumes.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgres-pv
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 100Mi
  hostPath:
    path: /data/postgres-pv
  storageClassName: standard

---
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
      storage: 100Mi
  storageClassName: standard

---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: redis-pv
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 100Mi
  hostPath:
    path: /data/redis-pv
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
      storage: 100Mi
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
          env:
            - name: POSTGRES_PASSWORD
              value: postgres
          resources:
            requests:
              cpu: 100m
              memory: 100Mi
            limits:
              cpu: 100m
              memory: 100Mi
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql/data
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: endpoint-stats
spec:
  selector:
    app: postgres
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
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
          image: redis:latest
          ports:
            - containerPort: 6379
          resources:
            requests:
              cpu: 100m
              memory: 100Mi
            limits:
              cpu: 100m
              memory: 100Mi
          args: ["--appendonly", "yes"]  # Enable persistence
          volumeMounts:
            - name: redis-storage
              mountPath: /data
      volumes:
        - name: redis-storage
          persistentVolumeClaim:
            claimName: redis-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: endpoint-stats
spec:
  selector:
    app: redis
  ports:
    - protocol: TCP
      port: 6379
      targetPort: 6379
```

### 5. Flask API Setup

The Flask API serves as the application backend, processing and storing endpoint statistics while providing a REST API for data access.

```yaml
# flask-api-deployment.yaml
---
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
          image: shreeraj1746/endpoint-stats:latest
          ports:
            - containerPort: 9999
          resources:
            requests:
              cpu: 100m
              memory: 100Mi
            limits:
              cpu: 100m
              memory: 100Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 9999
            initialDelaySeconds: 5
            periodSeconds: 10
          env:
            - name: DATABASE_URL
              value: postgresql://postgres:postgres@postgres:5432/postgres
            - name: REDIS_URL
              value: redis://redis:6379/0
          envFrom:
            - secretRef:
                name: flask-api-secret
---
apiVersion: v1
kind: Service
metadata:
  name: flask-api
  namespace: endpoint-stats
spec:
  selector:
    app: flask-api
  ports:
    - protocol: TCP
      port: 9999
      targetPort: 9999
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
    - host: api.endpoint-stats.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: flask-api
                port:
                  number: 9999
```

### 7. Secrets Management

Securely manage sensitive information such as database credentials and API keys.

```yaml
# secrets.yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: flask-api-secret
  namespace: endpoint-stats
type: Opaque
data:
  DB_USER: dXNlcg==
  DB_PASSWORD: cGFzc3dvcmQ=
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
