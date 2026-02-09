import subprocess
import time
import requests

print("Starting User Service...")
proc = subprocess.Popen(
    ["python", "-m", "uvicorn", "user_service:app", "--host", "0.0.0.0", "--port", "8001"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

time.sleep(5)

try:
    response = requests.get("http://127.0.0.1:8001/")
    print(f"✓ Service is running: {response.json()}")
    
    # Test register
    reg_response = requests.post(
        "http://127.0.0.1:8001/register",
        json={"email": "test@test.com", "password": "test123"}
    )
    print(f"✓ Register endpoint: {reg_response.status_code} - {reg_response.json()}")
    
except Exception as e:
    print(f"✗ Error: {e}")
finally:
    proc.terminate()
    print("\nService stopped.")
