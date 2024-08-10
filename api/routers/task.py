from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.task as task_crud
from api.db import get_db
import api.schemas.task as task_schema

router = APIRouter()

@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    """
    タスクのリストを取得します。

    Args:
        db (AsyncSession): データベースセッション。

    Returns:
        List[task_schema.Task]: タスクのリスト。
    """
    return await task_crud.get_tasks(db=db)

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)):
    """
    新しいタスクを作成します。

    Args:
        task_body (task_schema.TaskCreate): 作成するタスクのデータ。
        db (AsyncSession): データベースセッション。

    Returns:
        task_schema.TaskCreateResponse: 作成されたタスクのレスポンス。
    """
    return await task_crud.create_task(db=db, task_create=task_body)

@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    task_id: int, task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
    """
    既存のタスクを更新します。

    Args:
        task_id (int): 更新するタスクのID。
        task_body (task_schema.TaskCreate): 更新するタスクのデータ。
        db (AsyncSession): データベースセッション。

    Returns:
        task_schema.TaskCreateResponse: 更新されたタスクのレスポンス。

    Raises:
        HTTPException: タスクが存在しない場合は404エラーを返します。
    """
    task = await task_crud.get_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not exist")
    return await task_crud.update_task(db=db, task_create=task_body, original=task)

@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    タスクを削除します。

    Args:
        task_id (int): 削除するタスクのID。
        db (AsyncSession): データベースセッション。

    Raises:
        HTTPException: タスクが存在しない場合は404エラーを返します。
    """
    task = await task_crud.get_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not exist")
    await task_crud.delete_task(db=db, original=task)
    return
