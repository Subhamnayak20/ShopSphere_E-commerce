# Kubernetes Deployment Guide

## Prerequisites

- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl CLI installed and configured
- NGINX Ingress Controller installed

## Quick Start

### 1. Build Docker Images

```bash
# Build all service images
docker build -f Dockerfile.product -t shopsphere/product-service:latest .
docker build -f Dockerfile.user -t shopsphere/user-service:latest .
docker build -f Dockerfile.order -t shopsphere/order-service:latest .
```

### 2. Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy configuration and secrets
kubectl apply -f k8s/config.yaml -n shopsphere

# Deploy Redis
kubectl apply -f k8s/redis.yaml -n shopsphere

# Deploy services
kubectl apply -f k8s/product-service.yaml -n shopsphere
kubectl apply -f k8s/user-service.yaml -n shopsphere
kubectl apply -f k8s/order-service.yaml -n shopsphere

# Deploy Ingress
kubectl apply -f k8s/ingress.yaml -n shopsphere

# Deploy HPA (Horizontal Pod Autoscaler)
kubectl apply -f k8s/hpa.yaml -n shopsphere
```

### 3. Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n shopsphere

# Check services
kubectl get svc -n shopsphere

# Check ingress
kubectl get ingress -n shopsphere
```

### 4. Access Services

Add to `/etc/hosts` (Linux/Mac) or `C:\Windows\System32\drivers\etc\hosts` (Windows):
```
127.0.0.1 shopsphere.local
```

Access via:
- Product Service: http://shopsphere.local/api/products
- User Service: http://shopsphere.local/api/users
- Order Service: http://shopsphere.local/api/orders

## Deploy All at Once

```bash
kubectl apply -f k8s/ -n shopsphere
```

## Scaling

```bash
# Manual scaling
kubectl scale deployment product-service --replicas=3 -n shopsphere
kubectl scale deployment user-service --replicas=3 -n shopsphere
kubectl scale deployment order-service --replicas=3 -n shopsphere

# Check HPA status
kubectl get hpa -n shopsphere

# Watch auto-scaling in action
kubectl get hpa -n shopsphere --watch
```

## Load Balancing

Kubernetes provides built-in load balancing:
- **Service Load Balancing**: Round-robin across pod replicas
- **Ingress Load Balancing**: NGINX ingress controller distributes external traffic
- **Auto-scaling**: HPA scales pods based on CPU (70%) and Memory (80%) utilization

### HPA Configuration
- Min replicas: 2
- Max replicas: 10
- CPU threshold: 70%
- Memory threshold: 80%

## Monitoring

```bash
# View logs
kubectl logs -f deployment/product-service -n shopsphere
kubectl logs -f deployment/user-service -n shopsphere
kubectl logs -f deployment/order-service -n shopsphere

# Describe pod
kubectl describe pod <pod-name> -n shopsphere

# Get pod metrics
kubectl top pods -n shopsphere
```

## Cleanup

```bash
# Delete all resources
kubectl delete -f k8s/ -n shopsphere

# Delete namespace
kubectl delete namespace shopsphere
```

## Architecture

```
                    ┌─────────────────┐
                    │     Ingress     │
                    │  (nginx-ingress)│
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │   Product    │ │     User     │ │    Order     │
    │   Service    │ │   Service    │ │   Service    │
    │  (2 replicas)│ │ (2 replicas) │ │ (2 replicas) │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           └────────────────┼────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │    Redis     │
                    │  (1 replica) │
                    └──────────────┘
```

## Resource Allocation

| Service | Replicas | CPU Request | Memory Request | CPU Limit | Memory Limit |
|---------|----------|-------------|----------------|-----------|--------------|
| Product | 2 | 200m | 256Mi | 500m | 512Mi |
| User | 2 | 200m | 256Mi | 500m | 512Mi |
| Order | 2 | 200m | 256Mi | 500m | 512Mi |
| Redis | 1 | 100m | 128Mi | 200m | 256Mi |

## Notes

- All services use ClusterIP for internal communication
- Ingress handles external routing
- Redis data persists using PersistentVolumeClaim
- Health checks ensure pod readiness
- Secrets manage sensitive configuration
