from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from typing import TYPE_CHECKING
from config import Base, UserRole

if TYPE_CHECKING:
    from .projects import Project
    from .users import User

class ProjectMember(Base):
    __tablename__ = "project_members"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete='CASCADE'),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete='CASCADE'),
        primary_key=True,
    )
    role: Mapped[str] = mapped_column(
        String(50),
        default=UserRole.member
    )


    project: Mapped["Project"] = relationship(
        back_populates="members",
        init=False
    )

    user: Mapped["User"] = relationship(
        back_populates="project_members",
        init=False
    )