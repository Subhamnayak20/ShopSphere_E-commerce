# Load Balancing Quick Reference

## Docker Compose with NGINX Load Balancer

### Start
```bash
docker-compose -f docker-compose.lb.yml up -d
```

### Access
- Product Service: http://localhost/api/products
- User Service: http://localhost/api/users
- Order Service: http://localhost/api/orders
- Health Check: http://localhost/health

### Architecture
```
Client → NGINX (Port 80) → 2x Product Service (8000)
                         → 2x User Service (8001)
                         → 2x Order Service (8002)
                         → Redis (6379)
```

### Check Status
```bash
# View all containers
docker-compose -f docker-compose.lb.yml ps

# View NGINX logs
docker logs shopsphere-nginx -f

# View service logs
docker logs shopsphere-product-1 -f
docker logs shopsphere-product-2 -f
```

### Stop
```bash
docker-compose -f docker-compose.lb.yml down
```

---

## Kubernetes with HPA

### Deploy
```bash
kubectl apply -f k8s/ -n shopsphere
```

### Access
http://shopsphere.local/api/

### Architecture
```
Ingress → Service (Load Balancer) → 2-10 Pods (Auto-scaled)
```

### Check Status
```bash
# View pods
kubectl get pods -n shopsphere

# View HPA status
kubectl get hpa -n shopsphere

# Watch auto-scaling
kubectl get hpa -n shopsphere --watch

# View pod metrics
kubectl top pods -n shopsphere
```

### Manual Scale
```bash
kubectl scale deployment product-service --replicas=5 -n shopsphere
```

### Delete
```bash
kubectl delete -f k8s/ -n shopsphere
```

---

## Load Balancing Algorithms

### NGINX (Docker Compose)
- **Algorithm**: Least Connections
- **Health Checks**: 3 failures in 30s
- **Failover**: Automatic

### Kubernetes
- **Algorithm**: Round Robin (default)
- **Auto-scaling**: CPU 70%, Memory 80%
- **Min/Max Replicas**: 2-10

---

## Testing Load Distribution

### Simple Test
```bash
for i in {1..10}; do curl http://localhost/api/products; done
```

### Load Test (Apache Bench)
```bash
ab -n 1000 -c 10 http://localhost/api/products
```

### Load Test (wrk)
```bash
wrk -t4 -c100 -d30s http://localhost/api/products
```

---

## Troubleshooting

### Docker Compose
```bash
# Check NGINX config
docker exec shopsphere-nginx nginx -t

# Reload NGINX
docker exec shopsphere-nginx nginx -s reload

# View upstream status
docker logs shopsphere-nginx | grep upstream
```

### Kubernetes
```bash
# Check service endpoints
kubectl get endpoints -n shopsphere

# Describe HPA
kubectl describe hpa product-service-hpa -n shopsphere

# Check metrics server
kubectl top nodes
```

---

## Key Files

| File | Purpose |
|------|---------|
| `nginx.conf` | NGINX load balancer config |
| `docker-compose.lb.yml` | Docker Compose with LB |
| `k8s/hpa.yaml` | Kubernetes auto-scaling |
| `k8s/ingress.yaml` | Kubernetes ingress LB |
| `LOAD_BALANCING.md` | Full documentation |
