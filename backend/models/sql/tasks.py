from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Text, DateTime, func
from typing import TYPE_CHECKING
from datetime import datetime
from config import Base

if TYPE_CHECKING:
    from .projects import Project
    from .users import User
    from .column import Column
    from .comments import Comment

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        init=False
    )


    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete='CASCADE')
    )
    column_id: Mapped[int] = mapped_column(
        ForeignKey("columns.id", ondelete='CASCADE')
    )
    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete='SET NULL')
    )
    assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete='CASCADE'),
        nullable=True,
        default=None
    )
    position: Mapped[int] = mapped_column(default=0)
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None
    )    


    project: Mapped["Project"] = relationship(
        back_populates="tasks",
        init=False
    )
    column: Mapped["Column"] = relationship(
        back_populates="tasks",
        init=False
    )
    creator: Mapped["User"] = relationship(
        foreign_keys=[creator_id],
        back_populates="created_tasks",
        init=False
    )
    assignee: Mapped["User"] = relationship(
        foreign_keys=[assignee_id],
        back_populates="assigned_tasks",
        init=False
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
        init=False
    )