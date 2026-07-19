import redis 
from app.config import Redis_host,Redis_username,Redis_password

r = redis.Redis(
    host=Redis_host,
    port=19484,
    decode_responses=True,
    username=Redis_username,
    password=Redis_password,
)

r.ping()

