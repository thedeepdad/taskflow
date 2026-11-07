from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime, func, Identity
from typing import TYPE_CHECKING
from datetime import datetime
from config import Base

if TYPE_CHECKING:
    from .users import User


class RegistrationCode(Base):
    __tablename__ = "registration_code"

    id: Mapped[int] = mapped_column(
        Identity(),
        primary_key=True,
        init=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    hash_code: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        init=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    attempts: Mapped[int] = mapped_column(
        default=0,
        server_default="0",
        nullable=False
    )
    user: Mapped["User"] = relationship(
        back_populates="registration_code",
        init=False
    )
