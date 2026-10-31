from fastapi import APIRouter, status
from app.schemas import AddTaskRequest
from app.core.dependencies import user_dependency, db_dependency
from app.services.task import *

router = APIRouter(prefix="/task", tags=["Task"])

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_task(task: AddTaskRequest, user: user_dependency, db: db_dependency):
    return await add_task_service(task.title, task.project_id, user.get("id"), db)

@router.delete("/complete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def complete_task(task_id: int, user: user_dependency, db: db_dependency):
    return await complete_task_service(task_id, user.get("id"), db)

@router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, user: user_dependency, db: db_dependency):
    return await delete_task_service(task_id, user.get("id"), db)