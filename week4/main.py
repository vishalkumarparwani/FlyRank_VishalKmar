from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from auth import router as auth_router
from protected import router as protected_router
import postgres_repository as repo
import redis

app = FastAPI()
app.include_router(auth_router)
app.include_router(protected_router)

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True    
)

class Task(BaseModel):
    title: str
    done: bool = False


@app.get("/redis")
def redis_test():
    try:
        redis_client.ping()
        return {"status": "Redis Connected"}
    except Exception as e:
        return {
            "status": "Redis Not Connected",
            "error": str(e)
        }


@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }

@app.get("/health")
def health() :
    return { "message": "Health" }


@app.get("/tasks")
def get_tasks():
    return repo.get_all()

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = repo.get_by_id(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task

@app.post("/tasks", status_code = 201)
def create_task(task: Task):
    task = repo.create_task(task.title, task.done)

    if task is None:
        raise HTTPException(status_code=400, detail=f"Title cannot be empty")
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    task = repo.update_task(task_id, task.title, task.done)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code = 204)
def delete_task(task_id: int):
    task = repo.delete_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail=f"Task not found")