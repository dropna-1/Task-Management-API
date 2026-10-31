from sqlalchemy import ForeignKey, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base


project_members = Table(
    "project_members",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, default="user")
    owner_projects: Mapped[list["Project"]] = relationship(back_populates="owner")
    member_projects: Mapped[list["Project"]] = relationship(secondary=project_members,
                                                            back_populates="members")
    user_tasks: Mapped[list["Task"]] = relationship(back_populates="doer")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    owner: Mapped["User"] = relationship(back_populates="owner_projects")
    project_tasks: Mapped[list["Task"]] = relationship(back_populates="project")
    members: Mapped[list["User"]] = relationship(secondary=project_members,
                                                 back_populates="member_projects")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    title: Mapped[str] = mapped_column(nullable=True)
    project: Mapped["Project"] = relationship(back_populates="project_tasks")
    doer_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    doer: Mapped["User | None"] = relationship(back_populates="user_tasks")