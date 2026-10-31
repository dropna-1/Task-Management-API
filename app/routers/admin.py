from fastapi import APIRouter, status
from app.core.dependencies import *
from app.services.admin import *

router = APIRouter(prefix="/ad", tags=["Admin"])

@router.get("/all/users", status_code=status.HTTP_200_OK)
async def get_all_users(admin: admin_dependency, db: db_dependency):
    return await get_all_users_service(db)