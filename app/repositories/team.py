from repositories.base import SQLAlchemyRepository
from models import Team


class TeamRepository(SQLAlchemyRepository):
    model = Team
