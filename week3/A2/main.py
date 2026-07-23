from fastapi import FastAPI, HTTPException

from models import Task

from database import (
    initialize_database,
    get_all,
    get_by_id,
    create_task,
    update_task,
    delete_task,
)

app = FastAPI()

initialize_database()


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return get_all()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = get_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found",
        )

    return task


@app.post("/tasks", status_code=201)
def add_task(task: Task):
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty",
        )

    return create_task(task.title, task.done)


@app.put("/tasks/{task_id}")
def edit_task(task_id: int, task: Task):
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty",
        )

    updated = update_task(
        task_id,
        task.title,
        task.done,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found",
        )

    return updated


@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: int):
    deleted = delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found",
        )