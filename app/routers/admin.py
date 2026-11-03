from fastapi import APIRouter
from app.core.dependencies import *
from app.services.admin import *

router = APIRouter(prefix="/ad", tags=["Admin"])

@router.get("/all/users", status_code=status.HTTP_200_OK)
async def get_all_users(admin: admin_dependency, db: db_dependency):
    return await get_all_users_service(db)

@router.get("/all/projects", status_code=status.HTTP_200_OK)
async def get_all_projects(admin: admin_dependency, db: db_dependency):
    return await get_all_projects_service(db)

@router.patch("/promote/{user_id}", status_code=status.HTTP_200_OK)
async def promote(admin: admin_dependency, db: db_dependency, user_id: int):
    return await promote_service(db, user_id)

@router.patch("/demote/{user_id}", status_code=status.HTTP_200_OK)
async def demote(admin: admin_dependency, db: db_dependency, user_id: int):
    return await demote_service(db, user_id)