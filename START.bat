@echo off
cls
echo ========================================
echo ShopSphere E-commerce Platform
echo ========================================
echo.

REM Kill all existing Python processes on these ports
echo Cleaning up old services...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8001 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8002 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5500 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
timeout /t 2 /nobreak >nul

echo Starting services...
echo.

echo [1/4] User Service (Port 8001)...
start "User Service" cmd /k "python -m uvicorn user_service:app --reload --host 0.0.0.0 --port 8001"
timeout /t 4 /nobreak >nul

echo [2/4] Product Service (Port 8000)...
start "Product Service" cmd /k "python -m uvicorn product_service:app --reload --host 0.0.0.0 --port 8000"
timeout /t 4 /nobreak >nul

echo [3/4] Order Service (Port 8002)...
start "Order Service" cmd /k "python -m uvicorn order_service:app --reload --host 0.0.0.0 --port 8002"
timeout /t 4 /nobreak >nul

echo [4/4] Frontend Server (Port 5500)...
start "Frontend" cmd /k "cd frontend && python -m http.server 5500"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo SUCCESS! All services are running
echo ========================================
echo.
echo Open in browser: http://localhost:5500
echo.
echo API Documentation:
echo   http://localhost:8001/docs (User)
echo   http://localhost:8000/docs (Product)
echo   http://localhost:8002/docs (Order)
echo.

start http://localhost:5500

echo Press any key to exit...
pause >nul
