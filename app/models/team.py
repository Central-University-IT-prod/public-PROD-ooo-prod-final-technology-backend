from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from models import User
    from models import RequestToTeam
    from models import InvitationToUser


class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(100))
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id'))
    leader_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    members: Mapped[list["User"]] = relationship(secondary="team_members", lazy='selectin')

    requests: Mapped[list["RequestToTeam"]] = relationship()
    invites: Mapped[list["InvitationToUser"]] = relationship()
