
# from redis_om import get_redis_connection
# import os

# redis = get_redis_connection(
#     host=os.getenv("redis-19105.crce263.ap-south-1-1.ec2.cloud.redislabs.com", "localhost:5000"),
#     port=int(os.getenv("11844", 6379)),
#     password=os.getenv("Q4COyJ7Fe1VnGZc9iRnpZrG3pxXInymE", None),
#     decode_responses=True
# )

from redis_om import get_redis_connection

redis = get_redis_connection(
    host="localhost",
    port=6379,
    decode_responses=True
)
