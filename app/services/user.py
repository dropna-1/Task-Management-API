from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User, Project, Task, project_members
from app.schemas import ChangePasswordRequest
from app.core.security import password_hash
from app.core.exceptions import *
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select, exists


async def change_password_service(db: AsyncSession, user_id: int, form: ChangePasswordRequest):
    user = await db.get(User, user_id)
    if not password_hash.verify(user.hashed_password, form.current_password):
        raise PasswordWrongError()
    user.hashed_password = password_hash.hash(form.new_password)
    await db.commit()


async def get_my_project_service(user_id: int, db: AsyncSession):
    stmt = select(Project).where(Project.owner_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def accept_task_service(task_id: int, user_id: int, db: AsyncSession):
    stmt = select(Task).options(joinedload(Task.project)).where(Task.id == task_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if task is None:
        raise TaskNotExistError()
    if task.doer_id is not None:
        raise TaskAlreadySelectedError()
    stmt = select(exists().where(project_members.c.project_id == task.project_id,
                                 project_members.c.user_id == user_id))
    is_member = await db.scalar(stmt)
    if task.project.owner_id != user_id and not is_member:
        raise ForbiddenError()
    user = await db.get(User, user_id)
    task.doer = user
    await db.commit()
    return task