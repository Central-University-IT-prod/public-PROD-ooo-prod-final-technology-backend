from repositories.base import SQLAlchemyRepository
from models import InvitationToUser


class InvitationToUserRepository(SQLAlchemyRepository):
    model = InvitationToUser
