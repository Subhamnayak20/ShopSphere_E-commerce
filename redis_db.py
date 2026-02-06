import os

# Only attempt to import redis connection when USE_REDIS is enabled.
USE_REDIS = os.getenv("USE_REDIS", "true").lower() == "true"

if USE_REDIS:
    try:
        from redis_om import get_redis_connection
        redis = get_redis_connection(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            password=os.getenv("REDIS_PASSWORD", None),
            decode_responses=True,
        )
    except Exception:
        # If redis_om or underlying deps fail to import, fall back to None and allow in-memory mode
        redis = None
else:
    redis = None
