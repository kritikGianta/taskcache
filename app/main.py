from fastapi import FastAPI,HTTPException
from app.redis_client import redis_client
from app.schemas import TaskCreate
from app.cache import (
    get_cached_task,
    cache_task,
    delete_cached_task
)
from fastapi import Request
from app.rate_limiter import check_rate_limit
app = FastAPI(title = "TaskCache")

@app.get('/health')
def health():
    try :
        redis_client.ping()
        return {"status":"healthy","redis":"connected"}
    except Exception: 
        return {"status":"unhealthy","redis":"disconnected"}

@app.post("/tasks")
def create_task(task: TaskCreate):

    task_id = redis_client.incr("task:id")

    redis_client.hset(
        f"task:{task_id}",
        mapping={
            "title": task.title,
            "priority": task.priority,
            "status": "pending"
        }
    )

    redis_client.rpush("tasks", task_id)

    return {
        "id": task_id,
        "title": task.title,
        "priority": task.priority,
        "status": "pending"
    }

@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    cached_task = get_cached_task(task_id)

    if cached_task:
        redis_client.incr("stats:cache_hits")

        return {
            **cached_task,
            "source": "cache"
        }

    redis_client.incr("stats:cache_misses")

    task = redis_client.hgetall(f"task:{task_id}")

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task["id"] = task_id

    cache_task(task_id, task)

    return {
        **task,
        "source": "redis"
    }

@app.patch("/tasks/{task_id}/status")
def update_status(task_id: int, status: str):

    key = f"task:{task_id}"

    if not redis_client.exists(key):
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    redis_client.hset(
        key,
        "status",
        status
    )

    delete_cached_task(task_id)

    return {
        "id": task_id,
        "status": status
    }

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    key = f"task:{task_id}"

    if not redis_client.exists(key):
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    redis_client.delete(key)

    delete_cached_task(task_id)

    return {
        "message": "Task deleted"
    }

@app.post("/tasks/{task_id}/expire")
def expire_task(task_id: int, seconds: int = 60):

    key = f"task:{task_id}"

    if not redis_client.exists(key):
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    redis_client.expire(key, seconds)

    return {
        "message": "Task expiration set",
        "expires_in": seconds
    }

@app.get("/stats")
def get_stats():

    hits = int(redis_client.get("stats:cache_hits") or 0)
    misses = int(redis_client.get("stats:cache_misses") or 0)

    total = hits + misses

    hit_rate = 0

    if total > 0:
        hit_rate = round((hits / total) * 100, 2)

    return {
        "cache_hits": hits,
        "cache_misses": misses,
        "total_requests": total,
        "cache_hit_rate": hit_rate
    }

@app.post("/tasks/{task_id}/tags")
def add_tag(task_id: int, tag: str):

    if not redis_client.exists(f"task:{task_id}"):
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    redis_client.sadd(
        f"task:{task_id}:tags",
        tag
    )

    return {
        "task_id": task_id,
        "tag": tag
    }

@app.get("/tasks/{task_id}/tags")
def get_tags(task_id: int):

    if not redis_client.exists(f"task:{task_id}"):
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    tags = redis_client.smembers(
        f"task:{task_id}:tags"
    )

    return {
        "task_id": task_id,
        "tags": list(tags)
    }

@app.delete("/tasks/{task_id}/tags/{tag}")
def delete_tag(task_id: int, tag: str):

    redis_client.srem(
        f"task:{task_id}:tags",
        tag
    )

    return {
        "message": "Tag removed"
    }

@app.get("/activity")
def get_activity():

    activities = redis_client.lrange(
        "activity",
        0,
        9
    )

    return {
        "activities": activities
    }

@app.get("/protected")
def protected_route(request: Request):

    check_rate_limit(request)

    return {
        "message": "Request allowed"
    }