from fastapi import Request, HTTPException
from app.redis_client import redis_client


LIMIT = 10
WINDOW = 60


def check_rate_limit(request: Request):

    client_ip = request.client.host

    key = f"rate:{client_ip}"

    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, WINDOW)

    if count > LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )