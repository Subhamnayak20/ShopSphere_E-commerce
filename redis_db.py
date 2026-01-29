
from redis_om import get_redis_connection
import os

redis = get_redis_connection(
    host=os.getenv("redis-10956.c10.us-east-1-3.ec2.cloud.redislabs.com", "localhost:10956"),
    port=int(os.getenv("10956", 6379)),
    password=os.getenv("Q4COyJ7Fe1VnGZc9iRnpZrG3pxXInymE", None),
    decode_responses=True
)