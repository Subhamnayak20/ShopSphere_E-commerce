# Files to Remove - Cleanup List

## Unwanted Files (Safe to Delete)

### Test Files (Not Needed for Production)
- check_redis.py
- quick_test.py
- test_connection.py
- test_db.py
- test_register.py
- test_service.py
- test_startup.py

### Unused Database Files
- database.py (SQLAlchemy - not used, using in-memory)
- deps.py (SQLAlchemy dependencies - not used)
- models.py (SQLAlchemy models - not used)
- schemas.py (SQLAlchemy schemas - not used)

### Redundant Batch Files
- restart_all.bat
- run_app.bat
- start_services.bat
- START.bat

### Unused Frontend (If not needed)
- frontend/ directory (app.js, index.html, styles.css, test.html)
- serve_frontend.py

### Unused GitHub Directory
- .github/ directory

## Files to KEEP (Essential)

### Core Services
✅ product_service.py
✅ user_service.py
✅ order_service.py
✅ in_memory_db.py
✅ redis_db.py

### Configuration
✅ requirements.txt
✅ .dockerignore
✅ .gitignore
✅ nginx.conf

### Docker
✅ docker-compose.yml
✅ docker-compose.lb.yml
✅ Dockerfile.product
✅ Dockerfile.user
✅ Dockerfile.order

### Kubernetes
✅ k8s/ directory (all files)

### Documentation
✅ README.md
✅ FIXES.md
✅ LOAD_BALANCING.md
✅ LB_QUICK_REF.md
✅ LB_SUMMARY.md
✅ VENV_GUIDE.md
✅ VENV_STATUS.md

### Scripts
✅ start_all_services.ps1
✅ test_services.py (validation script - useful)

## Space Savings Estimate

- Test files: ~50 KB
- Unused database files: ~30 KB
- Batch files: ~10 KB
- Frontend: ~20 KB
- .github: ~5 KB

Total: ~115 KB (minimal, but cleaner project)

## Cleanup Commands

### Windows PowerShell
```powershell
# Remove test files
Remove-Item check_redis.py, quick_test.py, test_connection.py, test_db.py, test_register.py, test_service.py, test_startup.py -ErrorAction SilentlyContinue

# Remove unused database files
Remove-Item database.py, deps.py, models.py, schemas.py -ErrorAction SilentlyContinue

# Remove batch files
Remove-Item restart_all.bat, run_app.bat, start_services.bat, START.bat -ErrorAction SilentlyContinue

# Remove frontend (if not needed)
Remove-Item -Recurse -Force frontend, serve_frontend.py -ErrorAction SilentlyContinue

# Remove .github
Remove-Item -Recurse -Force .github -ErrorAction SilentlyContinue
```

### Linux/macOS
```bash
# Remove test files
rm -f check_redis.py quick_test.py test_connection.py test_db.py test_register.py test_service.py test_startup.py

# Remove unused database files
rm -f database.py deps.py models.py schemas.py

# Remove batch files
rm -f restart_all.bat run_app.bat start_services.bat START.bat

# Remove frontend (if not needed)
rm -rf frontend serve_frontend.py

# Remove .github
rm -rf .github
```
