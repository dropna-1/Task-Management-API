from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Project
from app.core.exceptions import *
from sqlalchemy.orm import selectinload
from app.database.models import Task
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def add_task_service(title: str, project_id: int, user_id: int, db: AsyncSession):
    stmt = select(Project).options(selectinload(Project.project_tasks)).where(Project.id == project_id)
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    if project is None:
        raise ProjectNotFoundError()
    if project.owner_id != user_id:
        raise ForbiddenError()
    task = Task(title=title, project_id=project_id)
    if task in project.project_tasks:
        raise TaskAlreadyExistError()
    task.project = project
    db.add(task)
    await db.commit()
    return task


async def complete_task_service(task_id: int, user_id: int, db: AsyncSession):
    task = await db.get(Task, task_id)
    if task is None:
        raise TaskNotFoundError()
    if task.doer_id != user_id:
        raise ForbiddenError()
    await db.delete(task)


async def delete_task_service(task_id: int, user_id: int, db: AsyncSession):
    stmt = select(Task).options(selectinload(Task.project)).where(Task.id == task_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if task is None:
        raise TaskNotFoundError()
    if task.project.owner_id != user_id:
        raise ForbiddenError()
    await db.delete(task)