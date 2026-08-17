import json
import logging
import os
from pathlib import Path

from schemas.task import Task, TaskCreate, TaskUpdate

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "entries.json"


logger = logging.getLogger(__name__)


def _check_dir(filename: str) -> None:
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)


def _save_tasks(filename: str, tasks: list[Task]) -> None:
    dumped_tasks = [task.model_dump() for task in tasks]
    try:
        with open(filename, "w") as f:
            json.dump(dumped_tasks, f, indent=4)
    except FileNotFoundError:
        _check_dir(filename)
        _save_tasks(filename, tasks)
    except PermissionError:
        logger.exception("No write permission for this file.")
        raise
    except OSError:
        logger.exception("An I/O error occurred.")
        raise


def load_tasks(filename: str) -> list[Task]:
    try:
        with open(filename, "r") as f:
            tasks_json = json.load(f)
            return [Task.model_validate(task) for task in tasks_json]
    except FileNotFoundError:
        _check_dir(filename)
        _save_tasks(filename, [])
        return []
    except json.JSONDecodeError:
        return []


def add_task(new_task: TaskCreate) -> Task:
    tasks = load_tasks(str(DATA_FILE))
    task = Task(
        id=max((task.id for task in tasks), default=0) + 1,
        description=new_task.description,
        done=False,
    )
    tasks.append(task)
    _save_tasks(str(DATA_FILE), tasks)
    return task


def delete_task(task_id: int) -> Task | None:
    tasks = load_tasks(str(DATA_FILE))
    if not tasks:
        return None
    removed_task: Task | None = None
    updated_tasks: list[Task] = []
    for task in tasks:
        if task.id == task_id:
            removed_task = task
        else:
            updated_tasks.append(task)

    if removed_task is not None:
        _save_tasks(str(DATA_FILE), updated_tasks)
        return removed_task
    else:
        return None


def update_task(task_id: int, task_update: TaskUpdate) -> Task | None:
    tasks = load_tasks(str(DATA_FILE))

    for task in tasks:
        if task.id == task_id:
            if task_update.description is not None:
                task.description = task_update.description
            if task_update.done is not None:
                task.done = task_update.done

            _save_tasks(str(DATA_FILE), tasks)
            return task

    return None
