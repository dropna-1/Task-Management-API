from fastapi import APIRouter, status, Query
from app.core.dependencies import user_dependency, db_dependency
from app.services.project import *
from typing import Annotated

router = APIRouter(prefix="/project", tags=["Project"])


@router.post("/add-project", status_code=status.HTTP_201_CREATED)
async def add_project(req: AddProjectRequest, user: user_dependency, db: db_dependency):
    return await add_project_service(req, db, user.get("id"))


@router.patch("/{project_id}/project/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def add_member(project_id: int, member_id: int,
                     db: db_dependency, user: user_dependency):
    return await add_member_service(member_id, project_id, db, user.get("id"))


@router.patch("/change-name/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def change_project_name(new_name: Annotated[str, Query(min_length=4, max_length=30)],
                      project_id: int, user: user_dependency, db: db_dependency):
    return await change_project_name_service(project_id, new_name, db, user.get("id"))


@router.delete("/{project_id}/delete/{member_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(member_id: int, project_id: int,
                        user: user_dependency, db: db_dependency):
    return await delete_member_service(user.get("id"), member_id, project_id, db)