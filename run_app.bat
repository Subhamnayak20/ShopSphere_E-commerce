@echo off
echo ========================================
echo Starting ShopSphere E-commerce Platform
echo ========================================
echo.

echo [1/4] Starting User Service...
start "User Service - Port 8001" cmd /k "python -m uvicorn user_service:app --host 0.0.0.0 --port 8001"
timeout /t 2 /nobreak >nul

echo [2/4] Starting Product Service...
start "Product Service - Port 8000" cmd /k "python -m uvicorn product_service:app --host 0.0.0.0 --port 8000"
timeout /t 2 /nobreak >nul

echo [3/4] Starting Order Service...
start "Order Service - Port 8002" cmd /k "python -m uvicorn order_service:app --host 0.0.0.0 --port 8002"
timeout /t 2 /nobreak >nul

echo [4/4] Starting Frontend Server...
start "Frontend - Port 5500" cmd /k "python serve_frontend.py"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo All services started successfully!
echo ========================================
echo.
echo Backend Services:
echo   User Service:    http://localhost:8001/docs
echo   Product Service: http://localhost:8000/docs
echo   Order Service:   http://localhost:8002/docs
echo.
echo Frontend:
echo   Website: http://localhost:5500
echo.
echo Opening website in browser...
timeout /t 2 /nobreak >nul
start http://localhost:5500
echo.
echo Press any key to stop all services...
pause >nul

echo Stopping all services...
taskkill /F /FI "WindowTitle eq User Service*" >nul 2>&1
taskkill /F /FI "WindowTitle eq Product Service*" >nul 2>&1
taskkill /F /FI "WindowTitle eq Order Service*" >nul 2>&1
taskkill /F /FI "WindowTitle eq Frontend*" >nul 2>&1
echo All services stopped.
