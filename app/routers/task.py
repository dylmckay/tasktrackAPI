from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db
from ..schemas.task import Task, TaskCreate, TaskUpdate
from ..services.task import add_task, delete_task, load_tasks, update_task

DbSession = Annotated[AsyncSession, Depends(get_db)]

router = APIRouter(tags=["tasks"])


@router.post("/tasks/", status_code=status.HTTP_201_CREATED)
async def task_add(new_task: TaskCreate, db: DbSession) -> Task:
    task = await add_task(new_task, db)
    return task


@router.patch("/tasks/{task_id}")
async def task_update(task_id: int, task_update: TaskUpdate, db: DbSession) -> Task:
    updated_task = await update_task(task_id, task_update, db)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return updated_task


@router.get("/tasks/")
async def tasks_load(db: DbSession) -> list[Task]:
    tasks = await load_tasks(db)
    return tasks


@router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def task_delete(task_id: int, db: DbSession) -> Task:
    deleted_task = await delete_task(task_id, db)
    if deleted_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found."
        )
    return deleted_task
