@echo off
echo Stopping all existing services...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq User Service*" 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Product Service*" 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Order Service*" 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Frontend*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting services...
echo.

start "User Service" cmd /k "python -m uvicorn user_service:app --host 0.0.0.0 --port 8001"
timeout /t 3 /nobreak >nul

start "Product Service" cmd /k "python -m uvicorn product_service:app --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul

start "Order Service" cmd /k "python -m uvicorn order_service:app --host 0.0.0.0 --port 8002"
timeout /t 3 /nobreak >nul

start "Frontend" cmd /k "python serve_frontend.py"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo All services started!
echo ========================================
echo.
echo Open: http://localhost:5500
echo.
start http://localhost:5500
pause
