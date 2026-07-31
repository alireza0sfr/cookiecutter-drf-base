# Kubernetes Deployment Guide

Complete guide to deploying Aghamohandes Backend on Kubernetes (K8s) clusters.

## Overview

Deploy the backend on Kubernetes for:
- **High availability**: Multiple replicas with load balancing
- **Auto-scaling**: HPA (Horizontal Pod Autoscaler) scales based on metrics
- **Self-healing**: Failed pods are automatically restarted
- **Rolling updates**: Zero-downtime deployments
- **Resource management**: CPU and memory limits
- **Service discovery**: Internal DNS resolution

## Prerequisites

- Kubernetes cluster (v1.20+)
- kubectl CLI
- Docker images pushed to registry
- Persistent storage (PVC) for databases
- Ingress controller (Nginx recommended)
- Optional: Kustomize, Helm, cert-manager

### Install Tools

```bash
# macOS
brew install kubectl kustomize kubernetes-cli

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Install Kustomize
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
sudo mv kustomize /usr/local/bin/
```

## Directory Structure

```
deployment/kubernetes/
├── deployment.yaml       # Web, Celery, Celery Beat deployments
├── service.yaml         # ClusterIP, LoadBalancer services
├── ingress.yaml         # Nginx Ingress, TLS certificates
├── configmap.yaml       # ConfigMaps and environment config
├── secret-example.yaml  # Secrets template (DO NOT COMMIT!)
├── rbac.yaml           # Service accounts, roles, bindings
├── kustomization.yaml  # Kustomize configuration
└── overlays/           # Environment-specific overrides
    ├── development/
    ├── staging/
    └── production/
```

## Quick Start

### 1. Setup Cluster

```bash
# Create namespace
kubectl create namespace aghamohandes

# Create secrets (DO NOT commit to git!)
kubectl create secret generic aghamohandes-secrets \
  --from-literal=database-url="postgresql://user:pass@postgres:5432/aghamohandes" \
  --from-literal=secret-key="YOUR_SECRET_KEY" \
  --from-literal=redis-password="REDIS_PASSWORD" \
  -n aghamohandes

# Verify secret created
kubectl get secrets -n aghamohandes
```

### 2. Deploy Services

```bash
# Deploy using kubectl
kubectl apply -f deployment/kubernetes/ -n aghamohandes

# Or using Kustomize
kubectl apply -k deployment/kubernetes/ -n aghamohandes

# Verify deployment
kubectl get all -n aghamohandes

# Watch rollout
kubectl rollout status deployment/aghamohandes-web -n aghamohandes
```

### 3. Verify Deployment

```bash
# Check pod status
kubectl get pods -n aghamohandes

# Check services
kubectl get svc -n aghamohandes

# Check ingress
kubectl get ingress -n aghamohandes

# View logs
kubectl logs -f deployment/aghamohandes-web -n aghamohandes

# Port forward for testing
kubectl port-forward svc/aghamohandes-web 8000:8000 -n aghamohandes
```

### 4. Access Application

```bash
# Get ingress IP
kubectl get ingress -n aghamohandes

# Access via IP
curl http://<INGRESS_IP>

# Or if DNS configured
curl https://api.example.com/health/
```

## Configuration Management

### ConfigMaps

```bash
# Create ConfigMap from file
kubectl create configmap aghamohandes-config \
  --from-file=deployment/kubernetes/configmap.yaml \
  -n aghamohandes

# View ConfigMap
kubectl get configmap aghamohandes-config -o yaml -n aghamohandes

# Update ConfigMap
kubectl edit configmap aghamohandes-config -n aghamohandes

# ConfigMaps automatically reload (except ENV vars)
```

### Secrets

```bash
# Create secret from file
kubectl create secret generic aghamohandes-secrets \
  --from-file=.env.prod \
  -n aghamohandes

# View secret (encrypted)
kubectl get secret aghamohandes-secrets -o yaml -n aghamohandes

# Update secret
kubectl patch secret aghamohandes-secrets \
  -p '{"data":{"database-url":"base64-encoded-value"}}' \
  -n aghamohandes

# For sensitive secrets, use Sealed Secrets or External Secrets
```

## Deployment Strategies

### Rolling Update (Default)

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1          # 1 extra pod during update
    maxUnavailable: 0    # Never take down pods
```

### Recreate (Downtime)

```yaml
strategy:
  type: Recreate  # Stops all pods, then starts new ones
```

### Blue-Green Deployment

```bash
# Deploy new version alongside old
kubectl apply -f deployment-v2.yaml

# Test new version
kubectl port-forward svc/aghamohandes-web-v2 8000:8000

# Switch service selector
kubectl patch service aghamohandes-web -p '{"spec":{"selector":{"version":"v2"}}}'

# Remove old deployment
kubectl delete deployment aghamohandes-web-v1
```

### Canary Deployment

```bash
# Deploy new version with 1 replica
kubectl set image deployment/aghamohandes-web web=aghamohandes:v2 --record

# Monitor metrics
kubectl get deployment aghamohandes-web -w

# Scale if stable
kubectl scale deployment aghamohandes-web --replicas=3
```

## Scaling

### Manual Scaling

```bash
# Scale deployment
kubectl scale deployment aghamohandes-web --replicas=5

# Scale Celery workers
kubectl scale deployment aghamohandes-celery --replicas=10
```

### Horizontal Pod Autoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: aghamohandes-web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: aghamohandes-web
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 2
        periodSeconds: 30
      selectPolicy: Max
```

Deploy HPA:

```bash
kubectl apply -f deployment/kubernetes/hpa.yaml

# Monitor HPA status
kubectl get hpa -w

# Check scaling events
kubectl describe hpa aghamohandes-web-hpa
```

## Updates & Rollbacks

### Update Image

```bash
# Update image
kubectl set image deployment/aghamohandes-web \
  web=aghamohandes:1.1.0 \
  --record

# Watch rollout progress
kubectl rollout status deployment/aghamohandes-web

# View history
kubectl rollout history deployment/aghamohandes-web

# Rollback to previous version
kubectl rollout undo deployment/aghamohandes-web

# Rollback to specific revision
kubectl rollout undo deployment/aghamohandes-web --to-revision=2
```

### Update Environment Variables

```bash
# Edit ConfigMap
kubectl edit configmap aghamohandes-config

# Force pod restart to reload
kubectl rollout restart deployment/aghamohandes-web
```

### Upgrade with Helm

```bash
helm upgrade aghamohandes ./helm-chart \
  -f values-prod.yaml \
  --namespace aghamohandes
```

## Monitoring & Logging

### View Logs

```bash
# Logs from current pod
kubectl logs deployment/aghamohandes-web -n aghamohandes

# Follow logs
kubectl logs -f deployment/aghamohandes-web -n aghamohandes

# Logs from specific pod
kubectl logs pod/aghamohandes-web-7d8f8f7f -n aghamohandes

# Logs from all containers
kubectl logs -f deployment/aghamohandes-web --all-containers=true

# Previous logs (for crashed pods)
kubectl logs pod/aghamohandes-web-7d8f8f7f --previous
```

### Interactive Shell

```bash
# Execute command in pod
kubectl exec -it deployment/aghamohandes-web -- bash

# Run Django management command
kubectl exec deployment/aghamohandes-web -- python manage.py migrate

# Run tests
kubectl exec deployment/aghamohandes-web -- pytest
```

### Port Forwarding

```bash
# Forward pod port to localhost
kubectl port-forward pod/aghamohandes-web-7d8f8f7f 8000:8000

# Forward service
kubectl port-forward svc/aghamohandes-web 8000:8000

# Forward to different local port
kubectl port-forward svc/aghamohandes-web 9000:8000
```

### Monitoring Tools

#### Prometheus + Grafana

```bash
# Install Prometheus Operator
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack

# Create ServiceMonitor
kubectl apply -f kubernetes/servicemonitor.yaml
```

#### Elasticsearch + Kibana

```bash
# Install ELK stack
helm repo add elastic https://Helm.elastic.co
helm install elasticsearch elastic/elasticsearch
helm install kibana elastic/kibana
```

## Security

### RBAC (Role-Based Access Control)

Defined in `rbac.yaml`:
- Service accounts for each component
- Roles with minimal permissions
- RoleBindings to apply roles

```bash
# Verify RBAC
kubectl auth can-i get pods --as=system:serviceaccount:aghamohandes:aghamohandes

# Check permissions
kubectl get rolebindings -n aghamohandes
```

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: aghamohandes-network-policy
spec:
  podSelector:
    matchLabels:
      app: aghamohandes
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: nginx-ingress
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
```

### Pod Security Policies

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
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
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'MustRunAs'
  fsGroup:
    rule: 'MustRunAs'
```

## Persistent Storage

### PostgreSQL with PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
  storageClassName: fast-ssd
```

### Redis with PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast-ssd
```

### Media & Static Files

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: media-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 100Gi
  storageClassName: shared-storage
```

## Kustomize Overlays

### Development Overlay

```
overlays/development/
├── kustomization.yaml
├── config.yaml
└── secrets.yaml
```

Usage:

```bash
kubectl apply -k overlays/development
```

### Staging Overlay

```bash
kubectl apply -k overlays/staging
```

### Production Overlay

```bash
kubectl apply -k overlays/production
```

## Troubleshooting

### Pod Won't Start

```bash
# Describe pod
kubectl describe pod aghamohandes-web-7d8f8f7f -n aghamohandes

# Check events
kubectl get events -n aghamohandes --sort-by='.lastTimestamp'

# Check resource availability
kubectl top nodes
kubectl describe node <node-name>

# Check resource requests
kubectl get pods -o json | jq '.items[] | {name: .metadata.name, cpu: .spec.containers[].resources.requests.cpu}'
```

### ImagePullBackOff

```bash
# Verify image exists in registry
docker pull aghamohandes:1.0.0

# Check image pull secrets
kubectl get secrets -n aghamohandes

# Update image pull secret
kubectl create secret docker-registry regcred \
  --docker-server=myregistry.azurecr.io \
  --docker-username=<username> \
  --docker-password=<password>
```

### CrashLoopBackOff

```bash
# Check pod logs
kubectl logs pod/aghamohandes-web-7d8f8f7f -n aghamohandes

# Check previous logs (for crashed pod)
kubectl logs pod/aghamohandes-web-7d8f8f7f --previous -n aghamohandes

# Connect to pod and debug
kubectl exec -it pod/aghamohandes-web-7d8f8f7f bash -n aghamohandes
```

### Database Connection Failed

```bash
# Test database connectivity
kubectl run -it --rm debug --image=postgres:14 -- \
  psql -h postgres -U postgres -d aghamohandes -c "SELECT 1"

# Check ConfigMap
kubectl get configmap aghamohandes-config -o yaml

# Check Secrets
kubectl get secret aghamohandes-secrets -o yaml

# Verify pods can reach database
kubectl exec deployment/aghamohandes-web -- \
  python -c "import psycopg2; conn = psycopg2.connect(os.environ['DATABASE_URL'])"
```

### OOMKilled

```bash
# Check memory usage
kubectl top pods -n aghamohandes

# Increase memory limit
kubectl set resources deployment aghamohandes-web \
  --limits=memory=2Gi \
  --requests=memory=1Gi
```

## Production Checklist

- [ ] Cluster is running with HA (3+ nodes)
- [ ] Persistent storage configured and backed up
- [ ] Secrets stored securely (not in git)
- [ ] Ingress with HTTPS/TLS configured
- [ ] Resource requests and limits set
- [ ] Health checks configured
- [ ] Monitoring and logging setup
- [ ] RBAC policies enforced
- [ ] Network policies configured
- [ ] Pod Security Policies enforced
- [ ] Regular backup schedule established
- [ ] Disaster recovery plan documented
- [ ] Load testing completed
- [ ] Autoscaling policies tested

## Useful Commands

```bash
# Get all resources
kubectl get all -n aghamohandes

# Describe resource
kubectl describe pod <pod-name> -n aghamohandes

# Edit resource
kubectl edit deployment aghamohandes-web -n aghamohandes

# Delete resource
kubectl delete pod <pod-name> -n aghamohandes

# Apply changes
kubectl apply -f kubernetes/ -n aghamohandes

# Dry run
kubectl apply -f kubernetes/ --dry-run=client -n aghamohandes

# Watch resources
kubectl get deployment -w -n aghamohandes

# Resource usage
kubectl top pods -n aghamohandes

# Stream logs
kubectl logs -f deployment/aghamohandes-web -n aghamohandes

# Port forward
kubectl port-forward svc/aghamohandes-web 8000:8000 -n aghamohandes
```

## Migration from Docker Compose

```bash
# 1. Build and push image
docker build -f deployment/docker/Dockerfile --target production -t aghamohandes:1.0.0 .
docker push myregistry.azurecr.io/aghamohandes:1.0.0

# 2. Update image in deployment/kubernetes/deployment.yaml
# 3. Create namespace and secrets
kubectl create namespace aghamohandes
kubectl create secret generic aghamohandes-secrets --from-env-file=.env.prod

# 4. Deploy to Kubernetes
kubectl apply -f deployment/kubernetes/ -n aghamohandes

# 5. Verify deployment
kubectl get all -n aghamohandes

# 6. Monitor logs
kubectl logs -f deployment/aghamohandes-web -n aghamohandes

# 7. Test application
kubectl port-forward svc/aghamohandes-web 8000:8000
# Visit http://localhost:8000/health/

# 8. Setup ingress and DNS
kubectl get ingress -n aghamohandes
# Point DNS to ingress IP
```

---

See also:
- [DOCKER.md](DOCKER.md) - Docker containerization
- [DEPLOYMENT.md](DEPLOYMENT.md) - General deployment guide
- Kubernetes configs in `deployment/kubernetes/`
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
