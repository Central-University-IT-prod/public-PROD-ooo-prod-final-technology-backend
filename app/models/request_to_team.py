from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class RequestToTeam(Base):
    __tablename__ = 'request_to_team'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
