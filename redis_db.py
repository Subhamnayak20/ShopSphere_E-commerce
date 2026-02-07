import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

try:
    redis_client.ping()
    print("✅ Connected to Local Redis")
except redis.ConnectionError:
    print("❌ Redis is not running")


