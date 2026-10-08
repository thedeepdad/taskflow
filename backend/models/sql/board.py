from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING
from config import Base

if TYPE_CHECKING:
    from .projects import Project
    from .column import Column

class Board(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(100))


    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete='CASCADE'),
        nullable=False
    )


    project: Mapped["Project"] = relationship(
        back_populates="boards",
        init=False
    )
    columns: Mapped[list["Column"]] = relationship(
        back_populates="board",
        cascade="all, delete-orphan",
        init=False
    )