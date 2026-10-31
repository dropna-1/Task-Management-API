from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models import User
from app.core.security import password_hash
from app.core.config import setting
from datetime import datetime, timedelta, timezone
import jwt

from app.schemas import UserRequest


async def authenticate_user(name: str, password: str, db: AsyncSession):
    stmt = select(User).where(User.username == name)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        return None
    if not password_hash.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(user_id: int, user_role: str, time: timedelta):
    payload = {
        "sub": user_id,
        "role": user_role,
        "exp": datetime.now(timezone.utc) + time
    }
    return jwt.encode(payload, setting.SECRET_KEY, "HS256")


async def signup_service(user: UserRequest, db: AsyncSession):
    db_user = User(username = user.username,
                   hashed_password = password_hash.hash(user.password))
    try:
        db.add(db_user)
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    return db_user