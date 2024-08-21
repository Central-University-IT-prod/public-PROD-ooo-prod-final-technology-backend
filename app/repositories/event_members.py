from repositories.base import SQLAlchemyRepository
from models import EventMember


class EventMemberRepository(SQLAlchemyRepository):
    model = EventMember
