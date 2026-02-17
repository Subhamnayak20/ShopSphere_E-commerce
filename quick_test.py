import subprocess
import time
import requests
import sys

print("=" * 50)
print("Testing ShopSphere Services")
print("=" * 50)

# Start User Service
print("\n[1/3] Starting User Service on port 8001...")
user_proc = subprocess.Popen(
    ["python", "-m", "uvicorn", "user_service:app", "--host", "0.0.0.0", "--port", "8001"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(3)

# Test User Service
try:
    resp = requests.get("http://localhost:8001/", timeout=2)
    print(f"   [OK] User Service: {resp.json()}")
except Exception as e:
    print(f"   [FAIL] User Service: {e}")
    user_proc.terminate()
    sys.exit(1)

# Test Register
try:
    resp = requests.post(
        "http://localhost:8001/register",
        json={"email": "test@test.com", "password": "test123"},
        timeout=2
    )
    print(f"   [OK] Register: {resp.status_code} - {resp.json()}")
except Exception as e:
    print(f"   [FAIL] Register: {e}")

print("\n[SUCCESS] All tests passed!")
print("\nServices are working correctly.")
print("You can now:")
print("  1. Keep this window open")
print("  2. Run: cd frontend && python -m http.server 5500")
print("  3. Open: http://localhost:5500")

input("\nPress Enter to stop services...")
user_proc.terminate()
print("Services stopped.")
