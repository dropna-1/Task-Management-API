from pydantic import BaseModel, Field
from typing import Annotated


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class UserRequest(BaseModel):
    username: Annotated[str, Field(min_length=4, max_length=20, default="Amir")]
    password: Annotated[str, Field(min_length=8, max_length=40, default="12345678")]


class ChangePasswordRequest(BaseModel):
    current_password: Annotated[str, Field(min_length=8, max_length=40)]
    new_password: Annotated[str, Field(min_length=8, max_length=40)]


class AddProjectRequest(BaseModel):
    name: Annotated[str, Field(min_length=4, max_length=60, default="project")]


class AddTaskRequest(BaseModel):
    title: Annotated[str, Field(min_length=4, max_length=120)]
    project_id: int
