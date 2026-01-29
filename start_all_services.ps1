#!/usr/bin/env pwsh
<#
.SYNOPSIS
Starts all ShopSphere E-commerce microservices
.DESCRIPTION
Launches Product Service, User Service, and Order Service on ports 8000, 8001, and 8002 respectively
#>

Write-Host "Starting ShopSphere E-commerce Services..." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if requirements are installed
Write-Host "`nChecking dependencies..." -ForegroundColor Yellow
try {
    python -c "import fastapi, uvicorn, redis_om" -ErrorAction Stop | Out-Null
    Write-Host "All dependencies installed" -ForegroundColor Green
}
catch {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r "$scriptDir\requirements.txt"
}

Write-Host "`nStarting services..." -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Green

# Function to start service
function Start-MyService {
    param(
        [string]$ServiceName,
        [string]$ModuleName,
        [int]$Port
    )
    
    Write-Host "`nStarting $ServiceName on port $Port..." -ForegroundColor Cyan
    $processArgs = @(
        "-m", "uvicorn",
        "$ModuleName`:app",
        "--reload",
        "--host", "127.0.0.1",
        "--port", $Port.ToString()
    )
    
    Start-Process python -ArgumentList $processArgs -NoNewWindow -PassThru
}

# Start all services
$productProcess = Start-MyService "Product Service" "product_service" 8000
$userProcess = Start-MyService "User Service" "user_service" 8001
$orderProcess = Start-MyService "Order Service" "order_service" 8002

Write-Host "`n==========================================" -ForegroundColor Green
Write-Host "All services started successfully!" -ForegroundColor Green
Write-Host "`nAccess your services at:" -ForegroundColor Cyan
Write-Host "  Product Service: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  User Service:    http://localhost:8001/docs" -ForegroundColor White
Write-Host "  Order Service:   http://localhost:8002/docs" -ForegroundColor White
Write-Host "`nPress Ctrl+C to stop all services" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Green

# Wait for processes
$processes = @($productProcess, $userProcess, $orderProcess)
Wait-Process -InputObject $processes -Any

Write-Host "`nShutting down services..." -ForegroundColor Yellow
Stop-Process -InputObject $processes -Force -ErrorAction SilentlyContinue
Write-Host "All services stopped." -ForegroundColor Green
