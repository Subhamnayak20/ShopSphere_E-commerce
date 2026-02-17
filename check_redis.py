from redis_db import redis, USE_REDIS

print(f"USE_REDIS: {USE_REDIS}")

if redis:
    try:
        redis.ping()
        print("[OK] Redis connected successfully!")
        print(f"Host: {redis.connection_pool.connection_kwargs.get('host')}")
        print(f"Port: {redis.connection_pool.connection_kwargs.get('port')}")
    except Exception as e:
        print(f"[ERROR] Redis connection failed: {e}")
else:
    print("[WARNING] Using in-memory mode (Redis disabled)")
