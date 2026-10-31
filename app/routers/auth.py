from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.services.auth import authenticate_user, create_access_token, signup_service
from app.schemas import LoginResponse, UserRequest
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from typing import Annotated

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
async def login(db: Annotated[AsyncSession, Depends(get_db)],
                form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form.username, form.password, db)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    token = create_access_token(user.id, user.role, timedelta(minutes=15))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        new_user = await signup_service(user, db)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=409, detail="username already exists")