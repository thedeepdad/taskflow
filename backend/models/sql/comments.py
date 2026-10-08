from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, Text, DateTime, func
from typing import TYPE_CHECKING
from datetime import datetime
from config import Base

if TYPE_CHECKING:
    from .tasks import Task
    from .users import User

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False
    )


    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id")
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )


    task: Mapped["Task"] = relationship(
        back_populates="comments",
        init=False
    )

    author: Mapped["User"] = relationship(
        back_populates="comments",
        init=False
    )