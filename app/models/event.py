from datetime import date

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(30), index=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey('admins.id'))
    team_creation_deadline: Mapped[date]
    max_member_qty: Mapped[int] = mapped_column(default=5)
