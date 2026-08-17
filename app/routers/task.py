from fastapi import APIRouter, HTTPException, status

from ..schemas.task import Task, TaskCreate, TaskUpdate
from ..services.task import (
    DATA_FILE,
    add_task,
    delete_task,
    load_tasks,
    update_task,
)

router = APIRouter(tags=["tasks"])


@router.post("/tasks/", status_code=status.HTTP_201_CREATED)
def task_add(new_task: TaskCreate) -> Task:
    task = add_task(new_task)
    return task


@router.patch("/tasks/{task_id}")
def task_update(task_id: int, task_update: TaskUpdate) -> Task:
    updated_task = update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return updated_task


@router.get("/tasks/")
def tasks_load() -> list[Task]:
    tasks = load_tasks(str(DATA_FILE))
    return tasks


@router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def task_delete(task_id: int) -> Task:
    deleted_task = delete_task(task_id)
    if deleted_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return deleted_task
