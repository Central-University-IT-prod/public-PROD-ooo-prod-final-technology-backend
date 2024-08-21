from repositories.base import SQLAlchemyRepository
from models import UserSkills


class UserSkillRepository(SQLAlchemyRepository):
    model = UserSkills
