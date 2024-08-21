from repositories.base import SQLAlchemyRepository
from models import Event


class EventRepository(SQLAlchemyRepository):
    model = Event
