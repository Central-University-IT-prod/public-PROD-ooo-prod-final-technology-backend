from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class EventMember(Base):
    __tablename__ = 'event_members'

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id'))
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    user_email: Mapped[str] = mapped_column(String(50))
