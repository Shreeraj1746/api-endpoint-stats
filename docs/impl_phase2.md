# Phase 2: Monitoring and Observability

## Overview

This phase focuses on setting up comprehensive monitoring and observability for the Endpoint Statistics application. We'll implement Prometheus, Grafana, and logging solutions to ensure we can effectively monitor and debug the application. A robust monitoring stack is critical for maintaining service reliability and quickly identifying issues before they impact users.

## Key Metrics to Monitor

For the Endpoint Statistics application, these metrics are particularly important:

1. **Request-specific metrics**:
   - Request count by endpoint
   - Request latency (p50, p90, p99)
   - Error rates by status code
   - Active concurrent connections

2. **Resource utilization**:
   - CPU and memory usage per pod
   - Disk I/O for database pods
   - Network traffic

3. **Database metrics**:
   - Query performance
   - Connection pool utilization
   - Transaction rates
   - Cache hit/miss ratios

4. **Redis metrics**:
   - Key operation rates
   - Memory utilization
   - Eviction counts
   - Command latency

## Component Interaction

The monitoring stack components interact as follows:

- **Application Pods**: Expose metrics endpoints that are scraped by Prometheus
- **Prometheus**: Collects and stores metrics from all components
- **Grafana**: Visualizes metrics from Prometheus data sources
- **Fluentd**: Collects logs from pods and forwards them to storage
- **AlertManager**: Receives alert notifications from Prometheus and routes them to receivers

## Implementation Steps

### 1. Prometheus Setup

Prometheus is a time-series database that scrapes and stores metrics, enabling powerful monitoring and alerting capabilities.

```yaml
# prometheus-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: endpoint-stats
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s

    rule_files:
      - /etc/prometheus/rules/*.yml

    alerting:
      alertmanagers:
      - static_configs:
        - targets:
          - 'alertmanager:9093'

    scrape_configs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)
          - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            regex: ([^:]+)(?::\d+)?;(\d+)
            replacement: $1:$2
            target_label: __address__
          - action: labelmap
            regex: __meta_kubernetes_pod_label_(.+)
          - source_labels: [__meta_kubernetes_namespace]
            action: replace
            target_label: kubernetes_namespace
          - source_labels: [__meta_kubernetes_pod_name]
            action: replace
            target_label: kubernetes_pod_name

      - job_name: 'flask-api'
        static_configs:
          - targets: ['flask-api:9999']
        metrics_path: /metrics
```

```yaml
# prometheus-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  namespace: endpoint-stats
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      serviceAccountName: prometheus
      initContainers:
      - name: init-chmod-data
        image: busybox:1.35.0
        command: ["sh", "-c", "chmod -R 777 /prometheus"]
        volumeMounts:
        - name: prometheus-storage
          mountPath: /prometheus
      containers:
      - name: prometheus
        image: prom/prometheus:v2.45.0
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: prometheus-config
          mountPath: /etc/prometheus
        - name: prometheus-rules
          mountPath: /etc/prometheus/rules
        - name: prometheus-storage
          mountPath: /prometheus
        resources:
          requests:
            memory: "512Mi"
            cpu: "200m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        args:
          - "--config.file=/etc/prometheus/prometheus.yml"
          - "--storage.tsdb.path=/prometheus"
          - "--storage.tsdb.retention.time=15d"
          - "--web.enable-lifecycle"
      volumes:
      - name: prometheus-config
        configMap:
          name: prometheus-config
      - name: prometheus-rules
        configMap:
          name: prometheus-rules
      - name: prometheus-storage
        persistentVolumeClaim:
          claimName: prometheus-pvc
```

```yaml
# prometheus-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: prometheus-pvc
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: standard
```

```yaml
# prometheus-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: prometheus
  namespace: endpoint-stats
spec:
  selector:
    app: prometheus
  ports:
  - port: 9090
    targetPort: 9090
  type: ClusterIP
```

### 2. Grafana Setup

Grafana provides visualization capabilities for metrics stored in Prometheus, helping to interpret and analyze the data.

```yaml
# grafana-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-datasources
  namespace: endpoint-stats
data:
  datasources.yaml: |
    apiVersion: 1
    datasources:
      - name: Prometheus
        type: prometheus
        url: http://prometheus:9090
        access: proxy
        isDefault: true
        editable: true
        jsonData:
          timeInterval: "5s"
          queryTimeout: "30s"
        version: 1
```

```yaml
# grafana-deployment.yaml
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
      initContainers:
      - name: init-chmod-data
        image: busybox:1.35.0
        command: ["sh", "-c", "mkdir -p /var/lib/grafana/plugins && chmod -R 777 /var/lib/grafana"]
        volumeMounts:
        - name: grafana-storage
          mountPath: /var/lib/grafana
      containers:
      - name: grafana
        image: grafana/grafana:9.5.5
        ports:
        - containerPort: 3000
        env:
        - name: GF_SECURITY_ADMIN_PASSWORD
          valueFrom:
            secretKeyRef:
              name: grafana-secrets
              key: admin-password
        - name: GF_SECURITY_ADMIN_USER
          value: "admin"
        - name: GF_INSTALL_PLUGINS
          value: "grafana-piechart-panel"
        - name: GF_DASHBOARDS_MIN_REFRESH_INTERVAL
          value: "5s"
        - name: GF_PATHS_PROVISIONING
          value: "/etc/grafana/provisioning"
        volumeMounts:
        - name: grafana-storage
          mountPath: /var/lib/grafana
        - name: grafana-datasources
          mountPath: /etc/grafana/provisioning/datasources
        - name: grafana-dashboards-config
          mountPath: /etc/grafana/provisioning/dashboards
        - name: grafana-dashboards
          mountPath: /var/lib/grafana/dashboards
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "200m"
      volumes:
      - name: grafana-storage
        persistentVolumeClaim:
          claimName: grafana-pvc
      - name: grafana-datasources
        configMap:
          name: grafana-datasources
      - name: grafana-dashboards-config
        configMap:
          name: grafana-dashboards
          items:
          - key: dashboards.yaml
            path: dashboards.yaml
      - name: grafana-dashboards
        configMap:
          name: grafana-dashboards
          items:
          - key: endpoint-stats-dashboard.json
            path: endpoint-stats-dashboard.json
```

```yaml
# grafana-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: grafana
  namespace: endpoint-stats
spec:
  selector:
    app: grafana
  ports:
  - port: 3000
    targetPort: 3000
  type: ClusterIP
```

```yaml
# grafana-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: grafana-secrets
  namespace: endpoint-stats
type: Opaque
data:
  admin-password: YWRtaW4=
```

```yaml
# grafana-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: grafana-pvc
  namespace: endpoint-stats
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

#### Sample Grafana Dashboard

Here's a sample dashboard configuration for the Endpoint Statistics application:

```json
{
  "dashboard": {
    "id": null,
    "title": "Endpoint Statistics Overview",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate by Endpoint",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (path)",
            "legendFormat": "{{path}}"
          }
        ]
      },
      {
        "id": 2,
        "title": "Response Time (P95) by Endpoint",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, path))",
            "legendFormat": "{{path}}"
          }
        ]
      },
      {
        "id": 3,
        "title": "Error Rate by Status Code",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) by (status, path)",
            "legendFormat": "{{status}} - {{path}}"
          }
        ]
      },
      {
        "id": 4,
        "title": "Database Query Time",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
        "targets": [
          {
            "expr": "rate(database_query_duration_seconds_sum[5m]) / rate(database_query_duration_seconds_count[5m])",
            "legendFormat": "Avg Query Time"
          }
        ]
      }
    ]
  }
}
```

### 3. Service Monitors

Service monitors define which services should be scraped for metrics and how Prometheus should gather them.

```yaml
# service-monitors.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: flask-api
  namespace: endpoint-stats
spec:
  selector:
    matchLabels:
      app: flask-api
  endpoints:
  - port: http
    interval: 15s
    path: /metrics
    metricRelabelings:
    - sourceLabels: [__name__]
      regex: 'http_requests_total|http_request_duration_seconds.*|process_.*'
      action: keep
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: postgres
  namespace: endpoint-stats
spec:
  selector:
    matchLabels:
      app: postgres
  endpoints:
  - port: metrics
    interval: 30s
    relabelings:
    - sourceLabels: [__meta_kubernetes_pod_container_port_number]
      regex: "9187"
      action: keep
```

### 4. Logging Setup

Fluentd collects logs from containers and forwards them to a centralized location for analysis and storage.

```yaml
# fluentd-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: endpoint-stats
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      <parse>
        @type json
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>

    <filter kubernetes.**>
      @type kubernetes_metadata
    </filter>

    <match kubernetes.var.log.containers.**fluentd**.log>
      @type null
    </match>

    <match kubernetes.var.log.containers.**>
      @type elasticsearch
      host elasticsearch
      port 9200
      logstash_format true
      <buffer>
        @type file
        path /var/log/fluentd-buffers/kubernetes.system.buffer
        flush_mode interval
        retry_type exponential_backoff
        flush_thread_count 2
        flush_interval 5s
      </buffer>
    </match>
```

```yaml
# fluentd-rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: fluentd
  namespace: endpoint-stats
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: fluentd
rules:
- apiGroups:
  - ""
  resources:
  - pods
  - namespaces
  verbs:
  - get
  - list
  - watch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: fluentd
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: fluentd
subjects:
- kind: ServiceAccount
  name: fluentd
  namespace: endpoint-stats
```

```yaml
# fluentd-daemonset.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: endpoint-stats
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      serviceAccount: fluentd
      serviceAccountName: fluentd
      containers:
      - name: fluentd
        image: fluent/fluentd:v1.14-1
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
        - name: fluentd-config
          mountPath: /fluentd/etc
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
      - name: fluentd-config
        configMap:
          name: fluentd-config
```

### 5. Alert Rules

Alert rules define conditions that trigger notifications when metrics indicate potential issues.

```yaml
# prometheus-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: endpoint-stats-alerts
  namespace: endpoint-stats
spec:
  groups:
  - name: endpoint-stats
    rules:
    - alert: HighErrorRate
      expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.1
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: High error rate detected
        description: Error rate is above 10% for the last 5 minutes

    - alert: SlowResponseTime
      expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 2
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: Slow response times detected
        description: 95th percentile of response time is above 2 seconds for the last 10 minutes

    - alert: HighCPUUsage
      expr: sum(rate(container_cpu_usage_seconds_total{namespace="endpoint-stats"}[5m])) by (pod) / sum(kube_pod_container_resource_limits_cpu_cores{namespace="endpoint-stats"}) by (pod) > 0.8
      for: 15m
      labels:
        severity: warning
      annotations:
        summary: High CPU usage detected
        description: Pod {{ $labels.pod }} has been using more than 80% of its CPU limit for 15 minutes
```

### 6. AlertManager Setup

AlertManager handles alerts sent by Prometheus and routes them to appropriate receivers like email, Slack, or PagerDuty.

```yaml
# alertmanager-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: alertmanager-config
  namespace: endpoint-stats
data:
  alertmanager.yml: |
    global:
      slack_api_url: 'https://hooks.slack.com/services/YOUR_SLACK_WEBHOOK'
      resolve_timeout: 5m

    route:
      group_by: ['alertname', 'severity']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 4h
      receiver: 'slack-notifications'
      routes:
      - match:
          severity: critical
        receiver: 'slack-critical'
        continue: true

    receivers:
    - name: 'slack-notifications'
      slack_configs:
      - channel: '#monitoring'
        send_resolved: true
        title: '[{{ .Status | toUpper }}] {{ .GroupLabels.alertname }}'
        text: >-
          {{ range .Alerts }}
            *Alert:* {{ .Annotations.summary }}
            *Description:* {{ .Annotations.description }}
            *Severity:* {{ .Labels.severity }}
          {{ end }}

    - name: 'slack-critical'
      slack_configs:
      - channel: '#incidents'
        send_resolved: true
        title: '[CRITICAL] {{ .GroupLabels.alertname }}'
        text: >-
          {{ range .Alerts }}
            *Alert:* {{ .Annotations.summary }}
            *Description:* {{ .Annotations.description }}
          {{ end }}
```

```yaml
# alertmanager-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alertmanager
  namespace: endpoint-stats
spec:
  replicas: 1
  selector:
    matchLabels:
      app: alertmanager
  template:
    metadata:
      labels:
        app: alertmanager
    spec:
      containers:
      - name: alertmanager
        image: prom/alertmanager:v0.23.0
        args:
        - "--config.file=/etc/alertmanager/alertmanager.yml"
        - "--storage.path=/alertmanager"
        ports:
        - containerPort: 9093
        volumeMounts:
        - name: alertmanager-config
          mountPath: /etc/alertmanager
        - name: alertmanager-storage
          mountPath: /alertmanager
      volumes:
      - name: alertmanager-config
        configMap:
          name: alertmanager-config
      - name: alertmanager-storage
        emptyDir: {}
```

```yaml
# alertmanager-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: alertmanager
  namespace: endpoint-stats
spec:
  selector:
    app: alertmanager
  ports:
  - port: 9093
    targetPort: 9093
  type: ClusterIP
```

## Log Analysis

To make the most of collected logs:

1. **Structured Logging**: Ensure application logs are in JSON format with consistent fields
2. **Log Levels**: Use appropriate log levels (DEBUG, INFO, WARN, ERROR)
3. **Context Information**: Include request IDs, user IDs, and other context in logs
4. **Search Queries**: Common Elasticsearch queries to identify issues:

```
# Find all errors for a specific endpoint
kubernetes.labels.app:flask-api AND level:ERROR AND path:"/api/stats"

# Track requests for a specific user
kubernetes.labels.app:flask-api AND user_id:"12345"

# Find slow database queries
kubernetes.labels.app:flask-api AND message:*query* AND duration:>1000
```

## Implementation Checklist

- [x] Deploy Prometheus
- [x] Configure Prometheus scraping
- [x] Deploy Grafana
- [x] Configure Grafana data sources
- [x] Create initial dashboards
- [x] Configure Service Monitors
- [x] Set up logging with Fluentd
- [x] Configure alert rules
- [x] Deploy AlertManager
- [x] Test monitoring endpoints
- [x] Verify alert notifications
- [x] Validate log collection and analysis

## Troubleshooting

1. **Prometheus scraping issues**:

   ```bash
   # Check scrape targets
   curl -s prometheus:9090/api/v1/targets | jq .

   # Check target labels
   kubectl get pods -n endpoint-stats --show-labels
   ```

2. **Grafana connection issues**:

   ```bash
   # Check data source status
   kubectl exec -it $(kubectl get pods -n endpoint-stats -l app=grafana -o name) -n endpoint-stats -- \
     curl -s http://admin:${GF_SECURITY_ADMIN_PASSWORD}@localhost:3000/api/datasources
   ```

3. **Log collection issues**:

   ```bash
   # Check fluentd status
   kubectl logs -n endpoint-stats -l app=fluentd

   # Verify log file permissions
   kubectl exec -it $(kubectl get pods -n endpoint-stats -l app=fluentd -o name) -n endpoint-stats -- \
     ls -la /var/log/containers/
   ```

## Next Steps

After completing Phase 2, proceed to [Phase 3: Security Implementation](impl_phase3.md) to implement security measures and access controls.
