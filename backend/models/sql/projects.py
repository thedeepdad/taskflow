from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text
from typing import TYPE_CHECKING
from config import Base

if TYPE_CHECKING:
    from .users import User
    from .projects_member import ProjectMember
    from .board import Board
    from .tasks import Task

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)


    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete='CASCADE')
    )


    owner: Mapped["User"] = relationship(
        back_populates="projects",
        init=False
    )
    members: Mapped[list["ProjectMember"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        init=False
    )
    boards: Mapped[list["Board"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        init=False
    )
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project",
        init=False
    )