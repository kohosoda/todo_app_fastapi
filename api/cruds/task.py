from typing import List, Tuple, Optional

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.task as task_model
import api.schemas.task as task_scheme

async def create_task(
    db: AsyncSession, task_create: task_scheme.TaskCreate
) -> task_model.Task:
    task = task_model.Task(**task_create.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_tasks(db: AsyncSession) -> List[Tuple[int, str, bool]]:
    result: Result = await (
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                task_model.Task.is_done,
            )
        )
    )

    return result.all()

async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
    result: Result = await db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    task: Optional[Tuple[task_model.Task]] = result.first()
    return task[0] if task is not None else None

async def update_task(
    db: AsyncSession, task_update: task_scheme.TaskUpdate, original: task_model.Task
) -> task_model.Task:
    original.title = task_update.title
    original.is_done = task_update.is_done
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_task(
    db: AsyncSession, original: task_model.Task
) -> None:
    await db.delete(original)
    await db.commit()
