from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User
from sqlalchemy import select

async def get_all_users_service(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users