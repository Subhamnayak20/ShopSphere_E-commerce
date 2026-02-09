@echo off
echo Starting ShopSphere Services...
echo.

start "User Service" cmd /k "python -m uvicorn user_service:app --reload --host 127.0.0.1 --port 8001"
timeout /t 3 /nobreak >nul

start "Product Service" cmd /k "python -m uvicorn product_service:app --reload --host 127.0.0.1 --port 8000"
timeout /t 3 /nobreak >nul

start "Order Service" cmd /k "python -m uvicorn order_service:app --reload --host 127.0.0.1 --port 8002"

echo.
echo All services started!
echo User Service: http://127.0.0.1:8001/docs
echo Product Service: http://127.0.0.1:8000/docs
echo Order Service: http://127.0.0.1:8002/docs
echo.
echo Open frontend/index.html in your browser
pause
