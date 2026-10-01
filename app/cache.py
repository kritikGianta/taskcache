import json
from app.redis_client import redis_client


CACHE_TTL = 60


def get_cached_task(task_id: int):
    key = f"cache:task:{task_id}"

    data = redis_client.get(key)

    if data:
        return json.loads(data)

    return None


def cache_task(task_id: int, task: dict):
    key = f"cache:task:{task_id}"

    redis_client.setex(
        key,
        CACHE_TTL,
        json.dumps(task)
    )


def delete_cached_task(task_id: int):
    key = f"cache:task:{task_id}"

    redis_client.delete(key)