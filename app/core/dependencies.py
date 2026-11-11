from alembic.util import status
from fastapi import Depends, HTTPException, status
from app.core.security import oauth2_schema, password_hash
from app.database.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import setting
from typing import Annotated
from app.database.models import User
import jwt

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_access(token: Annotated[str, Depends(oauth2_schema)]):
    payload = jwt.decode(token, setting.SECRET_KEY, "HS256")
    user_id = payload.get("sub")
    user_role = payload.get("role")
    if user_id is None or user_role is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return {"id": user_id, "role": user_role}

user_dependency = Annotated[dict, Depends(get_current_access)]
db_dependency = Annotated[AsyncSession, Depends(get_db)]

async def get_admin(user: user_dependency):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403)
    return user.get("id")

admin_dependency = Annotated[int, Depends(get_admin)]

async def get_main_admin(admin: admin_dependency, db: db_dependency) -> int:
    userdb = await db.get(User, admin)
    if (userdb.username != setting.ADMIN_USERNAME or
            not password_hash.verify(setting.ADMIN_PASSWORD, userdb.hashed_password)):
        raise HTTPException(status_code=403)
    return admin

main_admin_dependency = Annotated[int, Depends(get_main_admin)]