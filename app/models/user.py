from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

from schemas.user import ProfessionsEnum

if TYPE_CHECKING:
    from models import EventMember
    from models import RequestToTeam
    from models import Skill


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(60))
    telegram_username: Mapped[str] = mapped_column(String(60))
    fullname: Mapped[str] = mapped_column(String(60))

    bio: Mapped[str | None] = mapped_column(String(250), default=None)
    profession: Mapped[ProfessionsEnum]
    age: Mapped[int]

    password_updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    events: Mapped[list["EventMember"]] = relationship()
    requests: Mapped[list["RequestToTeam"]] = relationship()
    skills: Mapped[list["Skill"]] = relationship(secondary='user_skills', lazy='selectin')
