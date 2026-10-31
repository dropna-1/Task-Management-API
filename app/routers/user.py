from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Path
from app.core.dependencies import user_dependency, db_dependency
from app.schemas import ChangePasswordRequest
from app.services.user import *

router = APIRouter(tags=["User"])

@router.patch("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(form: ChangePasswordRequest,
                          db: db_dependency, user: user_dependency):
    if form.current_password == form.new_password:
        raise HTTPException(status_code=400, detail="new password cannot be current password")
    return await change_password_service(db, user.get("id"), form)


@router.get("/my_projects", status_code=status.HTTP_200_OK)
async def get_my_projects(user: user_dependency, db: db_dependency):
    return await get_my_project_service(user.get("id"), db)


@router.patch("/task/{task_id}/accept", status_code=status.HTTP_200_OK)
async def accept_task(task_id: Annotated[int, Path(gt=0)],
                      user: user_dependency, db: db_dependency):
    return accept_task_service(task_id, user.get("id"), db)

