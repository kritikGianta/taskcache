from fastapi import FastAPI,HTTPException
from app.redis_client import redis_client
from app.schemas import TaskCreate

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

    task = redis_client.hgetall(f"task:{task_id}")

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "id": task_id,
        **task
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