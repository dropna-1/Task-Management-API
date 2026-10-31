from app.database.models import Project, User
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import AddProjectRequest
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.core.exceptions import *


async def add_project_service(req: AddProjectRequest, db: AsyncSession, user_id: int):
    user = await db.get(User, user_id)
    if user is None:
        raise UserNotFoundError()
    project = Project(name=req.name, owner=user)
    db.add(project)
    await db.commit()
    return project


async def add_member_service(member_id: int, project_id: int, db: AsyncSession, user_id: int):
    stmt = select(Project).options(selectinload(Project.members)).where(Project.id == project_id)
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    if project is None:
        raise ProjectNotFoundError()
    if project.owner_id != user_id or user_id == member_id:
        raise ForbiddenError()
    member = await db.get(User, member_id)
    if member is None:
        raise UserNotFoundError()
    if member in project.members:
        raise MemberAlreadyExistError()
    project.members.append(member)
    await db.commit()
    return project


async def change_project_name_service(project_id: int, project_name: str,
                                      db: AsyncSession, user_id: int):
    project = await db.get(Project, project_id)
    if project is None:
        raise ProjectNotFoundError()
    if project.owner_id != user_id:
        raise ForbiddenError()
    project.name = project_name
    await db.commit()


async def delete_member_service(user_id: int, member_id: int, project_id: int, db: AsyncSession):
    stmt = select(Project).options(selectinload(Project.members)).where(Project.id == project_id)
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    if project is None:
        raise ProjectNotFoundError()
    if project.owner_id != user_id or user_id == member_id:
        raise ForbiddenError()
    user = await db.get(User, member_id)
    if user is None:
        raise UserNotFoundError()
    if user not in project.members:
        raise MemberNotExistError()
    project.members.remove(user)
    await db.commit()
