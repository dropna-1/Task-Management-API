from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import *
from app.database.models import User, Project
from sqlalchemy import select

async def get_all_users_service(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

async def get_all_projects_service(db: AsyncSession):
    result = await db.execute(select(Project))
    projects = result.scalars().all()
    return projects

async def promote_service(db: AsyncSession, user_id: int):
    user = await db.get(User, user_id)
    if user is None:
        raise UserNotFoundError()
    user.role = "admin"
    await db.commit()
    return user

async def demote_service(db: AsyncSession, user_id: int):
    user = await db.get(User, user_id)
    if user is None:
        raise UserNotFoundError()
    user.role = "user"
    await db.commit()
    return user