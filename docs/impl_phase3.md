# Phase 3: Security Implementation

## Overview
This phase focuses on implementing comprehensive security measures for the Endpoint Statistics application. We'll set up network policies, RBAC, and security contexts to ensure the application is properly secured against common threats and follows Kubernetes security best practices.

## Security Principles
The implementation follows key security principles:
- **Defense in depth**: Multiple layers of security controls
- **Least privilege**: Granting only the access necessary for each component
- **Secure by default**: Starting with restricted access and adding permissions as needed
- **Isolation**: Separating application components to limit the impact of compromises

## Implementation Steps

### 1. Network Policies
Network policies act as a firewall within Kubernetes, controlling which pods can communicate with each other. They help prevent lateral movement if an attacker gains access to one pod.

```yaml
# network-policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: endpoint-stats
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

This policy denies all traffic (ingress and egress) to all pods in the namespace by default, creating a zero-trust starting point.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-access
  namespace: endpoint-stats
spec:
  podSelector:
    matchLabels:
      app: flask-api
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: endpoint-stats
    ports:
    - protocol: TCP
      port: 5000
```

This policy allows traffic to the Flask API from pods within the same namespace.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: postgres-policy
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
    ports:
    - protocol: TCP
      port: 5432
```

This policy restricts database access to only the Flask API pods, protecting database data from unauthorized access.

### 2. RBAC Configuration
Role-Based Access Control (RBAC) limits what actions different users and service accounts can perform within the cluster.

```yaml
# rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: endpoint-stats-sa
  namespace: endpoint-stats
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: endpoint-stats-reader
  namespace: endpoint-stats
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get"]
  resourceNames: ["api-config"]
```

This role grants minimal read-only permissions to view pods and services, plus access to specific ConfigMaps.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: endpoint-stats-reader-binding
  namespace: endpoint-stats
subjects:
- kind: ServiceAccount
  name: endpoint-stats-sa
  namespace: endpoint-stats
roleRef:
  kind: Role
  name: endpoint-stats-reader
  apiGroup: rbac.authorization.k8s.io
```

This binding assigns the role to the service account used by the application.

### 3. Security Contexts
Security contexts define privilege and access control settings for pods and containers, implementing the principle of least privilege.

```yaml
# security-contexts.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-api
  namespace: endpoint-stats
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: flask-api
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
          seccompProfile:
            type: RuntimeDefault
        volumeMounts:
        - name: tmp-volume
          mountPath: /tmp
        - name: api-config
          mountPath: /app/config
          readOnly: true
      volumes:
      - name: tmp-volume
        emptyDir: {}
      - name: api-config
        configMap:
          name: api-config
```

This security context configuration:
- Forces the container to run as a non-root user
- Prevents privilege escalation
- Makes the root filesystem read-only (with a writable volume mounted at /tmp)
- Drops all Linux capabilities
- Uses the default seccomp profile to restrict system calls

### 4. Pod Security Policies
Pod Security Policies (PSP) enforce security settings across multiple pods to maintain consistent security standards.

```yaml
# pod-security-policy.yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: endpoint-stats-psp
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
  - 'configMap'
  - 'emptyDir'
  - 'projected'
  - 'secret'
  - 'downwardAPI'
  - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  supplementalGroups:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
  fsGroup:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
  readOnlyRootFilesystem: true
```

This Pod Security Policy prevents privileged pods, requires non-root users, and limits the types of volumes that can be mounted.

### 5. Secret Management
Secrets management involves securely storing and accessing sensitive information like API keys and passwords.

```yaml
# secret-management.yaml
apiVersion: v1
kind: Secret
metadata:
  name: api-keys
  namespace: endpoint-stats
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: ""
type: Opaque
data:
  API_KEY: <base64-encoded-key>
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
  namespace: endpoint-stats
data:
  ALLOWED_ORIGINS: "https://app.endpoint-stats.com"
  RATE_LIMIT: "100"
```

For accessing secrets, configure the application to use the Kubernetes API securely:

```yaml
# api-deployment-with-secrets.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-api
  namespace: endpoint-stats
spec:
  template:
    spec:
      containers:
      - name: flask-api
        env:
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: API_KEY
        envFrom:
        - configMapRef:
            name: api-config
```

### 6. TLS Configuration
Secure communication requires TLS certificates for encryption in transit.

```yaml
# tls-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
  namespace: endpoint-stats
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-certificate>
  tls.key: <base64-encoded-private-key>
```

```yaml
# ingress-with-tls.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: endpoint-stats-ingress
  namespace: endpoint-stats
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - api.endpoint-stats.com
    secretName: tls-secret
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

### 7. Image Security
Container image security helps prevent malicious code from being deployed.

```yaml
# deployment-with-image-security.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-api
  namespace: endpoint-stats
spec:
  template:
    spec:
      containers:
      - name: flask-api
        image: your-registry/flask-api:latest@sha256:abc123...  # Use digest instead of tag
        imagePullPolicy: Always
```

## Security Best Practices
1. **Regular Updates**: Keep all components patched and updated regularly
2. **Image Scanning**: Use tools like Trivy, Clair, or Anchore to scan for vulnerabilities
3. **Audit Logging**: Enable audit logging for all cluster operations
4. **Secret Rotation**: Regularly rotate credentials and secrets
5. **Network Segmentation**: Implement strict network policies
6. **Penetration Testing**: Regularly test security controls
7. **Cluster Hardening**: Follow CIS Kubernetes Benchmarks

## Implementation Checklist
- [ ] Apply network policies
- [ ] Configure RBAC roles and bindings
- [ ] Set up security contexts
- [ ] Implement pod security policies
- [ ] Configure secret management
- [ ] Set up TLS for ingress
- [ ] Implement image security controls
- [ ] Test security configurations
- [ ] Verify access controls
- [ ] Document security procedures

## Common Vulnerabilities Prevented

| Vulnerability | Prevention Mechanism |
|---------------|----------------------|
| Container escape | Security contexts, PSPs, drop capabilities |
| Privilege escalation | `allowPrivilegeEscalation: false`, non-root users |
| Credential exposure | Kubernetes Secrets, proper env var usage |
| Network attacks | Network Policies, TLS encryption |
| Data exfiltration | Egress network policies |
| Supply chain attacks | Image digest pinning, scanning |
| Unauthorized access | RBAC, network policies |

## Troubleshooting Security Issues

1. **Permission Issues**:
   ```bash
   # Check if service account has proper RBAC
   kubectl auth can-i --as=system:serviceaccount:endpoint-stats:endpoint-stats-sa get pods -n endpoint-stats
   ```

2. **Network Policy Issues**:
   ```bash
   # Install a temporary debug pod
   kubectl run -n endpoint-stats debug --image=busybox --rm -it -- /bin/sh

   # Test connectivity from inside the pod
   wget -O- --timeout=2 http://flask-api
   ```

3. **Security Context Issues**:
   ```bash
   # Check container processes and users
   kubectl exec -it -n endpoint-stats <pod-name> -- ps aux
   ```

## Next Steps
After completing Phase 3, proceed to [Phase 4: Deployment Strategy](impl_phase4.md) to implement deployment strategies and rolling updates.
