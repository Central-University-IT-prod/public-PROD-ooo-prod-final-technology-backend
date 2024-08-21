from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Skill(Base):
    __tablename__ = 'skills'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(30), unique=True)
