from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from sqlalchemy import String
from config import Base, UserRole

if TYPE_CHECKING:
    from .projects import Project
    from .projects_member import ProjectMember
    from .tasks import Task
    from .comments import Comment

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(default=UserRole.member)

    projects: Mapped[list["Project"]] = relationship(
        back_populates="owner",
        init=False
    )
    project_members: Mapped[list["ProjectMember"]] = relationship(
        back_populates="user",
        init=False
    )
    created_tasks: Mapped[list["Task"]] = relationship(
        foreign_keys="Task.creator_id",
        back_populates="creator",
        init=False
    )
    assigned_tasks: Mapped[list["Task"]] = relationship(
        foreign_keys="Task.assignee_id",
        back_populates="assignee",
        init=False
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author",
        init=False
    )

