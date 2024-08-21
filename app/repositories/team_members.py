from repositories.base import SQLAlchemyRepository
from models import TeamMember


class TeamMemberRepository(SQLAlchemyRepository):
    model = TeamMember
