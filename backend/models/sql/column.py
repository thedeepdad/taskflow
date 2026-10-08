from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING
from config import Base

if TYPE_CHECKING:
    from .board import Board
    from .tasks import Task


class Column(Base):
    __tablename__ = "columns"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    title: Mapped[str] = mapped_column(String(50))

    board_id: Mapped[int] = mapped_column(
        ForeignKey("boards.id", ondelete='CASCADE')
    )
    position: Mapped[int] = mapped_column(default=0)

    

    board: Mapped["Board"] = relationship(
        back_populates="columns",
        init=False
    )
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="column",
        init=False
    )