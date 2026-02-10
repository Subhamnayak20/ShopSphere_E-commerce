# Load Balancing Configuration

## Overview

ShopSphere implements load balancing at multiple levels to ensure high availability, scalability, and optimal performance.

## Architecture

```
                    ┌─────────────────┐
                    │     Clients     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  NGINX Load     │
                    │    Balancer     │
                    │   (Port 80)     │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │   Product    │ │     User     │ │    Order     │
    │   Service    │ │   Service    │ │   Service    │
    │              │ │              │ │              │
    │ Instance 1   │ │ Instance 1   │ │ Instance 1   │
    │ Instance 2   │ │ Instance 2   │ │ Instance 2   │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           └────────────────┼────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │    Redis     │
                    └──────────────┘
```

## Load Balancing Strategies

### 1. Docker Compose with NGINX

**Algorithm**: Least Connections
- Distributes requests to the server with the fewest active connections
- Optimal for applications with varying request processing times

**Configuration**: `docker-compose.lb.yml`

**Features**:
- 2 instances per service (6 total service instances)
- NGINX as reverse proxy and load balancer
- Health checks for all services
- Automatic failover

**Start**:
```bash
docker-compose -f docker-compose.lb.yml up -d
```

**Access**:
- All services: http://localhost/api/
- Product Service: http://localhost/api/products
- User Service: http://localhost/api/users
- Order Service: http://localhost/api/orders

### 2. Kubernetes with HPA

**Algorithm**: Round Robin (default) + Auto-scaling
- Kubernetes Service provides built-in load balancing
- HorizontalPodAutoscaler (HPA) scales based on metrics

**Configuration**: `k8s/hpa.yaml`

**Features**:
- Auto-scaling: 2-10 replicas per service
- CPU threshold: 70%
- Memory threshold: 80%
- Ingress controller for external load balancing

**Deploy**:
```bash
kubectl apply -f k8s/hpa.yaml -n shopsphere
```

**Monitor**:
```bash
kubectl get hpa -n shopsphere
```

## Load Balancing Algorithms

### NGINX (Docker Compose)

**Least Connections** (`least_conn`):
- Best for: Variable request processing times
- Ensures even distribution of load
- Prevents overloading slower instances

**Configuration**:
```nginx
upstream product_service {
    least_conn;
    server product-service-1:8000 max_fails=3 fail_timeout=30s;
    server product-service-2:8000 max_fails=3 fail_timeout=30s;
}
```

### Kubernetes

**Round Robin** (default):
- Distributes requests sequentially
- Simple and effective for similar workloads

**Session Affinity** (optional):
```yaml
service:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
```

## Health Checks

### NGINX Health Checks
- Max failures: 3
- Fail timeout: 30s
- Automatic removal of unhealthy instances

### Kubernetes Health Checks
- Liveness probes: Restart unhealthy pods
- Readiness probes: Remove from load balancer
- Startup probes: Allow initialization time

## Scaling

### Manual Scaling (Docker Compose)
```bash
docker-compose -f docker-compose.lb.yml up -d --scale product-service-1=3
```

### Manual Scaling (Kubernetes)
```bash
kubectl scale deployment product-service --replicas=5 -n shopsphere
```

### Auto-scaling (Kubernetes)
HPA automatically scales based on:
- CPU utilization (70% threshold)
- Memory utilization (80% threshold)
- Custom metrics (optional)

## Performance Optimization

### Connection Pooling
- Reuse connections between NGINX and services
- Reduces connection overhead

### Timeouts
- Connect timeout: 30s
- Send timeout: 30s
- Read timeout: 30s

### Caching (Future Enhancement)
- NGINX caching for static content
- Redis caching for database queries

## Monitoring

### Check Service Health
```bash
# Docker Compose
curl http://localhost/health

# Kubernetes
kubectl get pods -n shopsphere
kubectl top pods -n shopsphere
```

### View Load Distribution
```bash
# Docker logs
docker logs shopsphere-nginx -f

# Kubernetes
kubectl logs -f deployment/product-service -n shopsphere
```

## Failover

### Automatic Failover
- NGINX detects failed instances (3 failures in 30s)
- Removes unhealthy instances from pool
- Redistributes traffic to healthy instances

### Recovery
- Failed instances automatically rejoin pool after recovery
- Health checks verify instance readiness

## Testing Load Balancing

### Simple Test
```bash
# Send multiple requests
for i in {1..10}; do
  curl http://localhost/api/products
done
```

### Load Testing (Apache Bench)
```bash
ab -n 1000 -c 10 http://localhost/api/products
```

### Load Testing (wrk)
```bash
wrk -t4 -c100 -d30s http://localhost/api/products
```

## Configuration Files

| File | Purpose |
|------|---------|
| `nginx.conf` | NGINX load balancer configuration |
| `docker-compose.lb.yml` | Docker Compose with load balancing |
| `k8s/hpa.yaml` | Kubernetes auto-scaling configuration |
| `k8s/ingress.yaml` | Kubernetes ingress load balancing |

## Best Practices

1. **Always run multiple instances** (minimum 2 per service)
2. **Configure health checks** for automatic failover
3. **Set appropriate timeouts** to prevent hanging requests
4. **Monitor resource usage** and adjust scaling thresholds
5. **Use connection pooling** to reduce overhead
6. **Implement circuit breakers** for cascading failure prevention
7. **Enable access logs** for debugging and monitoring

## Troubleshooting

### Issue: Uneven load distribution
**Solution**: Check if instances have similar resources and performance

### Issue: Requests timing out
**Solution**: Increase timeout values in NGINX configuration

### Issue: Services not scaling
**Solution**: Verify metrics-server is installed in Kubernetes

### Issue: High latency
**Solution**: Add more replicas or optimize service code

## Future Enhancements

- [ ] Implement API Gateway (Kong/Traefik)
- [ ] Add rate limiting per client
- [ ] Implement circuit breaker pattern
- [ ] Add distributed tracing (Jaeger)
- [ ] Implement service mesh (Istio)
- [ ] Add geo-based load balancing
