import sys
sys.path.insert(0, '.')

from user_service import register, UserSchema

try:
    user = UserSchema(email="test@test.com", password="test123")
    result = register(user)
    print("Success:", result)
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
