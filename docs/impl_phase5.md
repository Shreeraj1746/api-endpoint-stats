# Phase 5: Monitoring and Maintenance

## Overview

This phase focuses on implementing comprehensive monitoring and maintenance procedures for the Endpoint Statistics application. We'll set up monitoring dashboards, backup procedures, maintenance protocols, and disaster recovery plans to ensure system reliability and data safety. These measures are crucial for long-term application stability and performance.

## Monitoring Philosophy

Effective monitoring follows these principles:

- **Proactive vs. Reactive**: Detect issues before they affect users
- **Actionable Alerts**: Every alert should be meaningful and require action
- **Comprehensive Coverage**: Monitor all components, dependencies, and user-facing services
- **Performance Insights**: Track trends over time to predict future needs

## Implementation Steps

### 1. Grafana Dashboard Setup

Grafana dashboards provide visual representations of system metrics, making it easy to monitor application health and performance.

```yaml
# grafana-dashboard.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: endpoint-stats-dashboard
  namespace: endpoint-stats
data:
  dashboard.json: |
    {
      "dashboard": {
        "id": null,
        "title": "Endpoint Statistics Dashboard",
        "panels": [
          {
            "title": "API Request Rate",
            "type": "graph",
            "datasource": "Prometheus",
            "targets": [
              {
                "expr": "rate(http_requests_total[5m])",
                "legendFormat": "{{method}} {{path}}"
              }
            ]
          },
          {
            "title": "Error Rate",
            "type": "graph",
            "datasource": "Prometheus",
            "targets": [
              {
                "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
                "legendFormat": "{{method}} {{path}}"
              }
            ]
          }
        ]
      }
    }
```

#### Advanced Grafana Dashboard Configuration

```yaml
# advanced-dashboard-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: advanced-endpoint-stats-dashboard
  namespace: endpoint-stats
data:
  dashboard.json: |
    {
      "dashboard": {
        "id": null,
        "title": "Endpoint Statistics Advanced Dashboard",
        "refresh": "10s",
        "time": {
          "from": "now-6h",
          "to": "now"
        },
        "timepicker": {
          "refresh_intervals": ["5s", "10s", "30s", "1m", "5m", "15m", "30m", "1h", "2h", "1d"],
          "time_options": ["5m", "15m", "1h", "6h", "12h", "24h", "2d", "7d", "30d"]
        },
        "panels": [
          {
            "id": 1,
            "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
            "title": "Request Rate by Endpoint",
            "type": "graph",
            "datasource": "Prometheus",
            "targets": [
              {
                "expr": "sum(rate(http_requests_total[5m])) by (path)",
                "legendFormat": "{{path}}"
              }
            ],
            "tooltip": {
              "shared": true,
              "sort": 0,
              "value_type": "individual"
            },
            "xaxis": {
              "mode": "time",
              "show": true
            },
            "yaxes": [
              {
                "format": "short",
                "label": "Requests/second",
                "logBase": 1,
                "show": true
              },
              {
                "format": "short",
                "logBase": 1,
                "show": true
              }
            ]
          },
          {
            "id": 2,
            "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
            "title": "Response Time by Endpoint",
            "type": "graph",
            "datasource": "Prometheus",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, path))",
                "legendFormat": "{{path}} (p95)"
              },
              {
                "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, path))",
                "legendFormat": "{{path}} (p50)"
              }
            ]
          },
          {
            "id": 3,
            "gridPos": {"h": 8, "w": 8, "x": 0, "y": 8},
            "title": "CPU Usage",
            "type": "graph",
            "datasource": "Prometheus",
            "targets": [
              {
                "expr": "sum(rate(container_cpu_usage_seconds_total{namespace=\"endpoint-stats\"}[5m])) by (pod)",
                "legendFormat": "{{pod}}"
              }
            ]
          },
          {
            "id": 4,
            "gridPos": {"h": 8, "w": 8, "x": 8, "y": 8},
            "title": "Memory Usage",
            "type": "graph",
            "datasource": "Prometheus",
            "targets": [
              {
                "expr": "sum(container_memory_usage_bytes{namespace=\"endpoint-stats\"}) by (pod)",
                "legendFormat": "{{pod}}",
                "format": "bytes"
              }
            ]
          },
          {
            "id": 5,
            "gridPos": {"h": 8, "w": 8, "x": 16, "y": 8},
            "title": "Pod Status",
            "type": "stat",
            "datasource": "Prometheus",
            "targets": [
              {
                "expr": "sum(kube_pod_status_phase{namespace=\"endpoint-stats\", phase=\"Running\"}) by (pod)"
              }
            ],
            "options": {
              "colorMode": "value",
              "graphMode": "area",
              "justifyMode": "auto",
              "orientation": "auto",
              "reduceOptions": {
                "calcs": ["lastNotNull"],
                "fields": "",
                "values": false
              }
            }
          },
          {
            "id": 6,
            "gridPos": {"h": 8, "w": 24, "x": 0, "y": 16},
            "title": "Error Rate by Status Code",
            "type": "graph",
            "datasource": "Prometheus",
            "targets": [
              {
                "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) by (status, path)",
                "legendFormat": "{{status}} - {{path}}"
              }
            ]
          }
        ],
        "templating": {
          "list": [
            {
              "name": "pod",
              "type": "query",
              "datasource": "Prometheus",
              "query": "label_values(kube_pod_info{namespace=\"endpoint-stats\"}, pod)",
              "refresh": 1,
              "regex": "",
              "sort": 0,
              "multi": true
            }
          ]
        },
        "annotations": {
          "list": [
            {
              "name": "Deployments",
              "datasource": "Prometheus",
              "expr": "changes(kube_deployment_status_replicas_updated{namespace=\"endpoint-stats\"}[5m]) > 0",
              "step": "60s",
              "titleFormat": "Deployment",
              "tagKeys": "deployment",
              "textFormat": "Deployment {{deployment}} updated"
            }
          ]
        }
      }
    }
```

### 2. Backup Procedures

Backups are essential for data recovery in case of system failures or data corruption. We'll implement automated backup procedures for both databases and configuration data.

```yaml
# backup-job.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: endpoint-stats
spec:
  schedule: "0 0 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:14
            command: ["/bin/sh", "-c"]
            args:
            - |
              pg_dump -h postgres -U admin -d endpoint_stats > /backup/backup-$(date +%Y%m%d).sql
            volumeMounts:
            - name: backup-volume
              mountPath: /backup
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: password
          volumes:
          - name: backup-volume
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
```

#### Advanced Backup Strategy

```yaml
# tiered-backup-job.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-tiered-backup
  namespace: endpoint-stats
spec:
  schedule: "0 * * * *"  # Hourly backups
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:14
            command: ["/bin/sh", "-c"]
            args:
            - |
              # Get current date info
              DATE=$(date +%Y%m%d)
              HOUR=$(date +%H)
              DOW=$(date +%u)  # day of week (1-7)
              DOM=$(date +%d)   # day of month

              # Determine backup type
              if [ "$HOUR" = "00" ] && [ "$DOW" = "7" ] && [ "$DOM" -le "07" ]; then
                # Monthly backup (first Sunday of month)
                BACKUP_FILE="monthly-$DATE.sql"
                RETENTION=365  # days to keep
              elif [ "$HOUR" = "00" ] && [ "$DOW" = "7" ]; then
                # Weekly backup (every Sunday at midnight)
                BACKUP_FILE="weekly-$DATE.sql"
                RETENTION=30   # days to keep
              elif [ "$HOUR" = "00" ]; then
                # Daily backup (every day at midnight)
                BACKUP_FILE="daily-$DATE.sql"
                RETENTION=7    # days to keep
              else
                # Hourly backup
                BACKUP_FILE="hourly-$DATE-$HOUR.sql"
                RETENTION=1    # days to keep
              fi

              echo "Creating $BACKUP_FILE"
              pg_dump -h postgres -U admin -d endpoint_stats > /backup/$BACKUP_FILE

              # Clean up old backups
              find /backup -name "hourly-*.sql" -mtime +$RETENTION -delete
              find /backup -name "daily-*.sql" -mtime +$RETENTION -delete
              find /backup -name "weekly-*.sql" -mtime +$RETENTION -delete
              find /backup -name "monthly-*.sql" -mtime +$RETENTION -delete
            volumeMounts:
            - name: backup-volume
              mountPath: /backup
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: password
          volumes:
          - name: backup-volume
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
```

#### Backup Verification and Testing

```yaml
# backup-verify-job.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-verification
  namespace: endpoint-stats
spec:
  schedule: "0 4 * * *"  # Run daily at 4 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: verify
            image: postgres:14
            command: ["/bin/sh", "-c"]
            args:
            - |
              # Find the most recent backup
              LATEST_BACKUP=$(find /backup -name "*.sql" -type f -printf "%T@ %p\n" | sort -n | tail -1 | cut -f2- -d" ")

              if [ -z "$LATEST_BACKUP" ]; then
                echo "No backups found!"
                exit 1
              fi

              echo "Verifying backup: $LATEST_BACKUP"

              # Create a temporary database for testing
              export PGPASSWORD="$POSTGRES_PASSWORD"
              psql -h postgres -U admin -d postgres -c "CREATE DATABASE backup_verify;"

              # Restore the backup to the test database
              psql -h postgres -U admin -d backup_verify < $LATEST_BACKUP

              # Run some basic validation queries
              ROW_COUNT=$(psql -h postgres -U admin -d backup_verify -t -c "SELECT count(*) FROM endpoints;")

              echo "Verification complete. Row count: $ROW_COUNT"

              # Clean up
              psql -h postgres -U admin -d postgres -c "DROP DATABASE backup_verify;"

              # Save verification results
              echo "$(date) - Backup $LATEST_BACKUP verified. Row count: $ROW_COUNT" >> /backup/verification.log
            volumeMounts:
            - name: backup-volume
              mountPath: /backup
            env:
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: password
          volumes:
          - name: backup-volume
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
```

### 3. Disaster Recovery Plan

A disaster recovery plan outlines procedures for recovering from various failure scenarios, from service outages to complete data center failures.

```yaml
# disaster-recovery-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: disaster-recovery-plan
  namespace: endpoint-stats
data:
  dr-plan.md: |
    # Disaster Recovery Plan for Endpoint Statistics Application

    ## Recovery Point Objective (RPO)
    The application aims for an RPO of 1 hour, meaning no more than 1 hour of data should be lost in case of a disaster.

    ## Recovery Time Objective (RTO)
    The application aims for an RTO of 4 hours, meaning the application should be back online within 4 hours of a disaster.

    ## Disaster Scenarios and Recovery Procedures

    ### Scenario 1: Database Failure

    1. Identify the failure cause
    2. If it's a pod or node issue, allow Kubernetes to reschedule the pod
    3. If data is corrupted, restore from the most recent backup:
       ```
       kubectl exec -it -n endpoint-stats deployment/postgres -- /bin/bash
       psql -U admin -d postgres -c "DROP DATABASE endpoint_stats;"
       psql -U admin -d postgres -c "CREATE DATABASE endpoint_stats;"
       psql -U admin -d endpoint_stats < /backup/latest_backup.sql
       ```

    ### Scenario 2: Complete Cluster Failure

    1. Provision a new Kubernetes cluster
    2. Apply all manifests from the Infrastructure as Code repository
    3. Restore database from the offsite backup storage
    4. Update DNS records to point to the new cluster

    ### Scenario 3: Application Deployment Failure

    1. Identify the failing deployment
    2. Roll back to the last known good version:
       ```
       kubectl rollout undo deployment/flask-api -n endpoint-stats
       ```
    3. Review logs to determine the root cause

    ## Recovery Testing Schedule
    DR recovery procedures should be tested quarterly to ensure they work as expected.
```

#### Disaster Recovery Scripts

```bash
#!/bin/bash
# dr-restore.sh

set -e

# Parameters
BACKUP_FILE=${1:-$(find /backup -name "*.sql" -type f -printf "%T@ %p\n" | sort -n | tail -1 | cut -f2- -d" ")}
NAMESPACE="endpoint-stats"
DATABASE_POD=$(kubectl get pods -n $NAMESPACE -l app=postgres -o name | head -1)

echo "Starting disaster recovery restore from backup: $BACKUP_FILE"

# 1. Create temporary database dump folder
echo "Creating temporary folder in pod..."
kubectl exec -n $NAMESPACE ${DATABASE_POD} -- mkdir -p /tmp/restore

# 2. Copy backup file to pod
echo "Copying backup file to pod..."
kubectl cp $BACKUP_FILE $NAMESPACE/${DATABASE_POD#*/}:/tmp/restore/backup.sql

# 3. Restore the database
echo "Restoring database..."
kubectl exec -n $NAMESPACE ${DATABASE_POD} -- bash -c "
export PGPASSWORD=\$(cat /etc/postgres-secret/password);
psql -U admin -d postgres -c 'DROP DATABASE IF EXISTS endpoint_stats;'
psql -U admin -d postgres -c 'CREATE DATABASE endpoint_stats;'
psql -U admin -d endpoint_stats < /tmp/restore/backup.sql
"

# 4. Verify restoration
echo "Verifying restoration..."
ROW_COUNT=$(kubectl exec -n $NAMESPACE ${DATABASE_POD} -- bash -c "
export PGPASSWORD=\$(cat /etc/postgres-secret/password);
psql -U admin -d endpoint_stats -t -c 'SELECT count(*) FROM endpoints;'
")

echo "Restoration complete. Row count: $ROW_COUNT"

# 5. Clean up
echo "Cleaning up..."
kubectl exec -n $NAMESPACE ${DATABASE_POD} -- rm -rf /tmp/restore

echo "Disaster recovery completed successfully!"
```

### 4. Maintenance Procedures

Regular system maintenance helps prevent issues and optimize performance. We'll implement scheduled maintenance tasks for database optimization, log rotation, and system updates.

```yaml
# maintenance-script.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: system-maintenance
  namespace: endpoint-stats
spec:
  template:
    spec:
      containers:
      - name: maintenance
        image: busybox
        command: ["/bin/sh", "-c"]
        args:
        - |
          # Clean up old logs
          find /var/log -type f -name "*.log" -mtime +7 -delete

          # Optimize database
          psql -h postgres -U admin -d endpoint_stats -c "VACUUM ANALYZE;"

          # Clean up Redis
          redis-cli -h redis -p 6379 FLUSHDB
      restartPolicy: Never
```

#### Comprehensive Maintenance Task Scheduler

```yaml
# maintenance-cron.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scheduled-maintenance
  namespace: endpoint-stats
spec:
  schedule: "0 2 * * *"  # Run daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: maintenance-sa
          containers:
          - name: maintenance
            image: bitnami/kubectl:latest
            command: ["/bin/bash", "-c"]
            args:
            - |
              # 1. Database maintenance
              echo "Running database maintenance..."
              kubectl exec -n endpoint-stats $(kubectl get pods -n endpoint-stats -l app=postgres -o name | head -1) -- bash -c "
                export PGPASSWORD=\$(cat /etc/postgres-secret/password);
                # Analyze tables to update statistics
                psql -U admin -d endpoint_stats -c 'VACUUM ANALYZE;'
                # Remove dead rows to reclaim space
                psql -U admin -d endpoint_stats -c 'VACUUM FULL;'
                # Rebuild indices
                psql -U admin -d endpoint_stats -c 'REINDEX DATABASE endpoint_stats;'
                # Cleanup temporary objects
                psql -U admin -d endpoint_stats -c 'DROP TABLE IF EXISTS temp_stats;'
              "

              # 2. Redis maintenance
              echo "Running Redis maintenance..."
              kubectl exec -n endpoint-stats $(kubectl get pods -n endpoint-stats -l app=redis -o name | head -1) -- bash -c "
                # Remove old cache entries
                redis-cli --raw -h localhost keys 'cache:*' | xargs -r redis-cli del
                # Run memory optimization
                redis-cli --raw -h localhost MEMORY PURGE
                # Save current dataset
                redis-cli --raw -h localhost SAVE
              "

              # 3. Log rotation and cleanup
              echo "Cleaning old logs..."
              kubectl get pods -n endpoint-stats --no-headers | awk '{print $1}' | xargs -I{} kubectl exec -n endpoint-stats {} -- bash -c "
                if [ -d /var/log ]; then
                  find /var/log -type f -name '*.log' -mtime +7 -delete || true
                fi
              " || true

              # 4. Clear old completed jobs
              echo "Cleaning old jobs..."
              kubectl delete jobs -n endpoint-stats --field-selector status.successful=1 --field-selector status.completionTime\\<$(date -d '7 days ago' -Ins)

              # 5. Check for configuration drifts
              echo "Checking for configuration drifts..."
              kubectl diff -f /manifests/ || true

              # 6. Report maintenance completion
              echo "Maintenance completed at $(date)"
            volumeMounts:
            - name: manifests-volume
              mountPath: /manifests
          volumes:
          - name: manifests-volume
            configMap:
              name: k8s-manifests
          restartPolicy: OnFailure
```

### 5. Health Check Scripts

Health check scripts help monitor the system and quickly identify issues.

```bash
#!/bin/bash
# health-check.sh

# Check API health
curl -s http://flask-api/health | jq .

# Check database connectivity
psql -h postgres -U admin -d endpoint_stats -c "SELECT 1;"

# Check Redis connectivity
redis-cli -h redis -p 6379 PING

# Check pod status
kubectl get pods -n endpoint-stats
```

#### Enhanced System Health Monitoring

```bash
#!/bin/bash
# enhanced-health.sh

OUTPUT_FILE="/tmp/health-report.txt"
NAMESPACE="endpoint-stats"
EMAIL_RECIPIENT="ops@example.com"

# Start fresh report
echo "Endpoint Statistics Health Report - $(date)" > $OUTPUT_FILE
echo "=================================================" >> $OUTPUT_FILE

# 1. Check all pod statuses
echo -e "\n## Pod Status" >> $OUTPUT_FILE
kubectl get pods -n $NAMESPACE -o wide >> $OUTPUT_FILE

# 2. Check recent pod events
echo -e "\n## Recent Pod Events" >> $OUTPUT_FILE
kubectl get events -n $NAMESPACE --sort-by='.lastTimestamp' | tail -10 >> $OUTPUT_FILE

# 3. Check resource usage
echo -e "\n## Resource Usage" >> $OUTPUT_FILE
echo "CPU and Memory:" >> $OUTPUT_FILE
kubectl top pods -n $NAMESPACE >> $OUTPUT_FILE

# 4. Check API health
echo -e "\n## API Health" >> $OUTPUT_FILE
API_POD=$(kubectl get pods -n $NAMESPACE -l app=flask-api -o name | head -1)
if [ -n "$API_POD" ]; then
  kubectl exec -n $NAMESPACE $API_POD -- curl -s http://localhost:5000/health >> $OUTPUT_FILE
else
  echo "No API pod found!" >> $OUTPUT_FILE
fi

# 5. Database checks
echo -e "\n## Database Health" >> $OUTPUT_FILE
DB_POD=$(kubectl get pods -n $NAMESPACE -l app=postgres -o name | head -1)
if [ -n "$DB_POD" ]; then
  echo "Connection test:" >> $OUTPUT_FILE
  kubectl exec -n $NAMESPACE $DB_POD -- bash -c "PGPASSWORD=\$(cat /etc/postgres-secret/password) psql -U admin -d endpoint_stats -c 'SELECT 1;'" >> $OUTPUT_FILE

  echo "Database size:" >> $OUTPUT_FILE
  kubectl exec -n $NAMESPACE $DB_POD -- bash -c "PGPASSWORD=\$(cat /etc/postgres-secret/password) psql -U admin -d endpoint_stats -c 'SELECT pg_size_pretty(pg_database_size(\"endpoint_stats\"));'" >> $OUTPUT_FILE

  echo "Connection count:" >> $OUTPUT_FILE
  kubectl exec -n $NAMESPACE $DB_POD -- bash -c "PGPASSWORD=\$(cat /etc/postgres-secret/password) psql -U admin -d endpoint_stats -c 'SELECT count(*) FROM pg_stat_activity;'" >> $OUTPUT_FILE
else
  echo "No database pod found!" >> $OUTPUT_FILE
fi

# 6. Redis checks
echo -e "\n## Redis Health" >> $OUTPUT_FILE
REDIS_POD=$(kubectl get pods -n $NAMESPACE -l app=redis -o name | head -1)
if [ -n "$REDIS_POD" ]; then
  echo "Connection test:" >> $OUTPUT_FILE
  kubectl exec -n $NAMESPACE $REDIS_POD -- redis-cli PING >> $OUTPUT_FILE

  echo "Memory usage:" >> $OUTPUT_FILE
  kubectl exec -n $NAMESPACE $REDIS_POD -- redis-cli INFO memory | grep used_memory_human >> $OUTPUT_FILE

  echo "Client count:" >> $OUTPUT_FILE
  kubectl exec -n $NAMESPACE $REDIS_POD -- redis-cli INFO clients | grep connected_clients >> $OUTPUT_FILE
else
  echo "No Redis pod found!" >> $OUTPUT_FILE
fi

# 7. Check PVC status
echo -e "\n## Storage Status" >> $OUTPUT_FILE
kubectl get pvc -n $NAMESPACE >> $OUTPUT_FILE

# 8. Check running services
echo -e "\n## Services" >> $OUTPUT_FILE
kubectl get svc -n $NAMESPACE >> $OUTPUT_FILE

# 9. Check ingress
echo -e "\n## Ingress" >> $OUTPUT_FILE
kubectl get ingress -n $NAMESPACE >> $OUTPUT_FILE

# 10. Check recent logs
echo -e "\n## Recent API Logs" >> $OUTPUT_FILE
if [ -n "$API_POD" ]; then
  kubectl logs -n $NAMESPACE $API_POD --tail=20 >> $OUTPUT_FILE
fi

# Display report
cat $OUTPUT_FILE

# Optional: Send report by email
# mail -s "Endpoint Statistics Health Report" $EMAIL_RECIPIENT < $OUTPUT_FILE
```

### 6. Monitoring Alerts

Monitoring alerts notify operators of system issues that require attention.

```yaml
# monitoring-alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: endpoint-stats-alerts
  namespace: endpoint-stats
spec:
  groups:
  - name: endpoint-stats
    rules:
    - alert: HighLatency
      expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: High API latency detected
        description: 95th percentile latency is above 1 second
    - alert: DatabaseConnectionIssues
      expr: up{job="postgres"} == 0
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: Database connection issues
        description: Cannot connect to PostgreSQL database
```

#### Business-Level Alerting

Add alerts focused on business metrics rather than just technical metrics:

```yaml
# business-alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: endpoint-stats-business-alerts
  namespace: endpoint-stats
spec:
  groups:
  - name: business-metrics
    rules:
    - alert: HighErrorRateForKey
      expr: sum(rate(http_errors_total{customer_tier="premium"}[5m])) / sum(rate(http_requests_total{customer_tier="premium"}[5m])) > 0.01
      for: 5m
      labels:
        severity: critical
        team: customer-success
      annotations:
        summary: High error rate for premium customers
        description: Error rate for premium customers is above 1% for 5 minutes
        dashboard: https://grafana.example.com/d/abc123/customer-dashboard
        runbook: https://wiki.example.com/runbooks/high-error-rate

    - alert: APIQuotaAlmostReached
      expr: sum(rate(api_calls_total[1h])) by (customer_id) / on(customer_id) group_left api_quota > 0.9
      for: 15m
      labels:
        severity: warning
        team: sales
      annotations:
        summary: API quota almost reached
        description: Customer {{ $labels.customer_id }} is using >90% of their API quota

    - alert: AbnormalTrafficPattern
      expr: abs(sum(rate(http_requests_total[1h])) - sum(rate(http_requests_total[1h] offset 1d))) / sum(rate(http_requests_total[1h] offset 1d)) > 0.5
      for: 30m
      labels:
        severity: warning
        team: security
      annotations:
        summary: Abnormal traffic pattern detected
        description: Traffic has changed by more than 50% compared to the same time yesterday
```

### 7. Performance Tuning Guidelines

Recommendations for optimizing application performance based on metrics.

```yaml
# performance-tuning-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: performance-tuning-guide
  namespace: endpoint-stats
data:
  tuning-guide.md: |
    # Performance Tuning Guide for Endpoint Statistics

    ## Resource Allocation Guidelines

    ### Flask API
    - Start with 100m CPU, 128Mi memory per pod
    - For every 100 req/s, add approximately 50m CPU
    - For heavy statistical analysis workloads, increase memory to 256Mi per pod

    ### PostgreSQL
    - For databases under 10GB: 500m CPU, 1Gi memory
    - For databases 10-50GB: 1000m CPU, 2Gi memory
    - For databases over 50GB: 2000m CPU, 4Gi memory

    ### Redis
    - For caching only: 100m CPU, 256Mi memory
    - With persistent storage: 200m CPU, 512Mi memory

    ## Query Optimization

    ### Common Slow Queries and Solutions
    1. Endpoint statistics aggregation:
       ```sql
       -- Original slow query
       SELECT endpoint, COUNT(*), AVG(response_time)
       FROM requests
       WHERE timestamp > NOW() - INTERVAL '30 days'
       GROUP BY endpoint;

       -- Optimized query
       SELECT endpoint, COUNT(*), AVG(response_time)
       FROM requests
       WHERE timestamp > NOW() - INTERVAL '30 days'
       GROUP BY endpoint
       ORDER BY COUNT(*) DESC
       LIMIT 10;
       ```

    2. Add appropriate indices:
       ```sql
       CREATE INDEX idx_requests_timestamp ON requests(timestamp);
       CREATE INDEX idx_requests_endpoint ON requests(endpoint);
       ```

    ## Scaling Guidelines

    - Set HPA targets at 70% CPU to allow buffer for traffic spikes
    - Implement PodDisruptionBudgets for critical components
    - Pre-scale before expected high-traffic events

    ## Caching Strategy

    1. Use Redis for API-level caching with appropriate TTLs:
       - High-change data: 1-5 minutes
       - Medium-change data: 30-60 minutes
       - Reference data: 12-24 hours

    2. Implement HTTP caching headers for client-side caching

    ## Connection Pooling

    - Database connections: Min 5, Max 20 per pod
    - Redis connections: Min 2, Max 10 per pod
```

## Capacity Planning

A strategy for planning resource capacity based on growth projections.

```yaml
# capacity-planning-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: capacity-planning
  namespace: endpoint-stats
data:
  capacity-plan.md: |
    # Capacity Planning for Endpoint Statistics

    ## Current Resource Usage (Baseline)

    | Component | Current Pods | CPU/Pod | Memory/Pod | Storage |
    |-----------|--------------|---------|------------|---------|
    | Flask API | 3            | 100m    | 128Mi      | N/A     |
    | PostgreSQL| 1            | 500m    | 1Gi        | 10Gi    |
    | Redis     | 1            | 100m    | 256Mi      | 5Gi     |

    ## Growth Projections

    | Metric             | Current | 3 Months | 6 Months | 12 Months |
    |--------------------|---------|----------|----------|-----------|
    | Requests/second    | 100     | 250      | 500      | 1000      |
    | Database size (GB) | 5       | 8        | 15       | 30        |
    | Cache size (GB)    | 1       | 2        | 3        | 5         |

    ## Resource Scaling Plan

    ### 3 Months
    - Scale Flask API to 5 pods
    - Increase PostgreSQL to 750m CPU, 1.5Gi memory
    - No changes needed for Redis

    ### 6 Months
    - Scale Flask API to 8 pods
    - Increase PostgreSQL to 1000m CPU, 2Gi memory
    - Increase PostgreSQL storage to 20Gi
    - Increase Redis to 200m CPU, 512Mi memory

    ### 12 Months
    - Scale Flask API to 15 pods
    - Consider database sharding or read replicas
    - Increase PostgreSQL to 2000m CPU, 4Gi memory, 50Gi storage
    - Increase Redis to 500m CPU, 1Gi memory, 10Gi storage

    ## Node Capacity Planning

    For 12-month projections, minimum node requirements:
    - Worker nodes: 5 (8 CPU, 32GB RAM each)
    - Consider dedicated nodes for database workloads
```

## Implementation Checklist

- [ ] Set up Grafana dashboards
- [ ] Configure basic and advanced monitoring visualizations
- [ ] Configure backup procedures
- [ ] Set up backup verification and testing
- [ ] Create disaster recovery plan and scripts
- [ ] Implement maintenance automation
- [ ] Create health check scripts
- [ ] Configure monitoring alerts
- [ ] Document performance tuning guidelines
- [ ] Create capacity planning document
- [ ] Test backup and restore
- [ ] Verify monitoring setup
- [ ] Document maintenance procedures

## Log Retention Policy

```yaml
# log-retention-policy-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: log-retention-policy
  namespace: endpoint-stats
data:
  policy.md: |
    # Log Retention Policy

    ## Retention Periods

    | Log Type       | Retention Period | Storage Location |
    |---------------|------------------|------------------|
    | Application   | 30 days          | Elasticsearch    |
    | System        | 14 days          | Elasticsearch    |
    | Security      | 365 days         | Secured storage  |
    | Audit         | 180 days         | Secured storage  |
    | Performance   | 7 days           | Elasticsearch    |

    ## Compliance Requirements

    For regulated industries, adjust retention periods to:
    - Financial services: Minimum 7 years for transaction logs
    - Healthcare: Minimum 6 years for access logs
    - PCI-DSS: Minimum 1 year for authentication logs

    ## Log Rotation Configuration

    Logs will be rotated as follows:
    - Size-based rotation: When log file reaches 100MB
    - Time-based rotation: Daily at midnight

    ## Archival Procedure

    1. Logs older than retention period are compressed
    2. Compressed logs are moved to cold storage
    3. Verification of archived logs is performed monthly
```

## Next Steps

After completing Phase 5, you have successfully implemented all major components of the Endpoint Statistics application. Review the [Implementation Checklist](implementation_checklist.md) to ensure all components are properly configured and tested.
