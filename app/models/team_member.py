from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class TeamMember(Base):
    __tablename__ = 'team_members'

    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'), primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), default=None, primary_key=True)
