from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class InvitationToUser(Base):
    __tablename__ = 'invitation_to_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
