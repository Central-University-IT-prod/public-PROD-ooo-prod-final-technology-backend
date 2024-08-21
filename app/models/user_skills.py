from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.skill import Skill


class UserSkills(Base):
    __tablename__ = 'user_skills'

    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id'), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
