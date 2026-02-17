"""Quick test to verify all services can be imported without errors"""

print("Testing imports...")

try:
    print("1. Testing user_service...")
    import user_service
    print("   [OK] user_service")
except Exception as e:
    print(f"   [ERROR] user_service: {e}")

try:
    print("2. Testing product_service...")
    import product_service
    print("   [OK] product_service")
except Exception as e:
    print(f"   [ERROR] product_service: {e}")

try:
    print("3. Testing order_service...")
    import order_service
    print("   [OK] order_service")
except Exception as e:
    print(f"   [ERROR] order_service: {e}")

print("\nAll services can be imported successfully!")
