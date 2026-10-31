from alembic.util import status
from fastapi import Depends, HTTPException, status
from app.core.security import oauth2_schema
from app.database.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import setting
from typing import Annotated
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

def get_admin(user: user_dependency):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403)
    return user.get("id")

admin_dependency = Annotated[int, Depends(get_admin)]