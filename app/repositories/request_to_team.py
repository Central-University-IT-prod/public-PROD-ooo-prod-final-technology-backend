from repositories.base import SQLAlchemyRepository
from models import RequestToTeam


class RequestToTeamRepository(SQLAlchemyRepository):
    model = RequestToTeam
