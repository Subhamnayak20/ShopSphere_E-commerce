# ShopSphere Cleanup Script
# Removes unwanted files while keeping essential application and documentation files

Write-Host "ShopSphere E-commerce - Cleanup Script" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

$filesToRemove = @(
    # Test files
    "check_redis.py",
    "quick_test.py",
    "test_connection.py",
    "test_db.py",
    "test_register.py",
    "test_service.py",
    "test_startup.py",
    
    # Unused database files
    "database.py",
    "deps.py",
    "models.py",
    "schemas.py",
    
    # Redundant batch files
    "restart_all.bat",
    "run_app.bat",
    "start_services.bat",
    "START.bat",
    
    # Frontend (if not needed)
    "serve_frontend.py"
)

$foldersToRemove = @(
    "frontend",
    ".github"
)

Write-Host "Removing unwanted files..." -ForegroundColor Yellow
$removedCount = 0

foreach ($file in $filesToRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "[REMOVED] $file" -ForegroundColor Green
        $removedCount++
    }
}

foreach ($folder in $foldersToRemove) {
    if (Test-Path $folder) {
        Remove-Item $folder -Recurse -Force
        Write-Host "[REMOVED] $folder/" -ForegroundColor Green
        $removedCount++
    }
}

Write-Host ""
Write-Host "Cleanup complete! Removed $removedCount items." -ForegroundColor Cyan
Write-Host ""
Write-Host "Essential files kept:" -ForegroundColor Green
Write-Host "  - Core services (product_service.py, user_service.py, order_service.py)"
Write-Host "  - Configuration files (requirements.txt, nginx.conf, etc.)"
Write-Host "  - Docker files (Dockerfiles, docker-compose.yml)"
Write-Host "  - Kubernetes manifests (k8s/)"
Write-Host "  - All documentation (*.md files)"
Write-Host "  - Virtual environment (.venv/)"
Write-Host ""
Write-Host "Application is ready to run!" -ForegroundColor Cyan
