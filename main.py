from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database.database import AsyncSessionLocal
from app.core.config import setting
from app.database.models import User
from app.core.security import password_hash
from app.routers.auth import  router as auth_router
from app.routers.user import router as user_router
from app.routers.project import router as project_router
from app.routers.task import router as task_router
from contextlib import asynccontextmanager
from app.core.exceptions import *
from sqlalchemy import select

@asynccontextmanager
async def lifespan(api: FastAPI):
    async with AsyncSessionLocal() as db:
        stmt = select(User).where(User.role == "admin")
        result = await db.execute(stmt)
        admin = result.scalar_one_or_none()
        if admin is None:
            admin = User(username = setting.ADMIN_USERNAME,
                         hashed_password = password_hash.hash(setting.ADMIN_PASSWORD),
                         role = "admin")
            db.add(admin)
            await db.commit()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)

@app.exception_handler(ProjectNotFoundError)
async def project_not_found(request: Request, exc: ProjectNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "project not found"})

@app.exception_handler(ForbiddenError)
async def forbidden(request: Request, exc: ForbiddenError):
    return JSONResponse(status_code=403, content={"detail": "forbidden"})

@app.exception_handler(UserNotFoundError)
async def user_not_found(request: Request, exc: UserNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "user not found"})

@app.exception_handler(MemberAlreadyExistError)
async def member_already_exist(request: Request, exc: MemberAlreadyExistError):
    return JSONResponse(status_code=409, content={"detail": "user already a member"})

@app.exception_handler(PasswordWrongError)
async def password_wrong(request: Request, exc: PasswordWrongError):
    return JSONResponse(status_code=401, content={"detail": "password is wrong"})

@app.exception_handler(MemberNotExistError)
async def member_already_not_exist(request: Request, exc: MemberNotExistError):
    return JSONResponse(status_code=404, content={"detail": "user not exist"})

@app.exception_handler(TaskAlreadyExistError)
async def task_already_exist(request: Request, exc: TaskAlreadyExistError):
    return JSONResponse(status_code=409,
                        content={"detail": "this task already exist in project"})

@app.exception_handler(TaskAlreadySelectedError)
async def task_already_selected(request: Request, exc: TaskAlreadySelectedError):
    return JSONResponse(status_code=409,
                        content={"detail": "task already selected by someone else"})

@app.exception_handler(TaskNotExistError)
async def task_already_not_exist(request: Request, exc: TaskNotExistError):
    return JSONResponse(status_code=404, content={"detail": "task not exist"})

@app.exception_handler(TaskNotFoundError)
async def task_not_found(request: Request, exc: TaskNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "task not found"})

@app.exception_handler(PromotedError)
async def promoted(request: Request, exc: PromotedError):
    return JSONResponse(status_code=400, content={"detail": "user already promoted"})

@app.exception_handler(DemotedError)
async def demoted(request: Request, exc: DemotedError):
    return JSONResponse(status_code=400, content={"detail": "user already demoted"})