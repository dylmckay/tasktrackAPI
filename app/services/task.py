import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.task import Task as TaskModel
from ..schemas.task import Task, TaskCreate, TaskUpdate

logger = logging.getLogger(__name__)


async def load_tasks(db: AsyncSession) -> list[Task]:
    tasks = await db.execute(select(TaskModel))
    tasks_sequence = tasks.scalars().all()
    return [Task.model_validate(task) for task in tasks_sequence]


async def add_task(new_task: TaskCreate, db: AsyncSession) -> Task:
    task_model = TaskModel(description=new_task.description)
    db.add(task_model)
    await db.commit()
    await db.refresh(task_model)
    return Task.model_validate(task_model)


async def update_task(
    task_id: int, task_update: TaskUpdate, db: AsyncSession
) -> Task | None:
    task_model = await db.get(TaskModel, task_id)

    if task_model is not None:
        if task_update.description is not None:
            task_model.description = task_update.description
        if task_update.done is not None:
            task_model.done = task_update.done

        await db.commit()
        await db.refresh(task_model)
        return Task.model_validate(task_model)


async def delete_task(task_id: int, db: AsyncSession) -> Task | None:
    task_model = await db.get(TaskModel, task_id)
    if task_model is not None:
        task_schema = Task.model_validate(task_model)
        await db.delete(task_model)
        await db.commit()
        return task_schema
