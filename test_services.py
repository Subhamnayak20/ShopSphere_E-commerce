#!/usr/bin/env python3
"""
Test script to verify all services can start without errors
"""

def test_imports():
    print("Testing service imports...")
    
    try:
        from product_service import app as product_app
        print("[OK] Product Service")
    except Exception as e:
        print(f"[FAILED] Product Service - {e}")
        return False
    
    try:
        from order_service import app as order_app
        print("[OK] Order Service")
    except Exception as e:
        print(f"[FAILED] Order Service - {e}")
        return False
    
    try:
        from user_service import app as user_app
        print("[OK] User Service")
    except Exception as e:
        print(f"[FAILED] User Service - {e}")
        return False
    
    print("\nAll services imported successfully!")
    return True

if __name__ == "__main__":
    success = test_imports()
    exit(0 if success else 1)
