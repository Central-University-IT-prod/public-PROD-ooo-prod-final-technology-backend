from repositories.base import SQLAlchemyRepository
from models import Skill


class SkillRepository(SQLAlchemyRepository):
    model = Skill
