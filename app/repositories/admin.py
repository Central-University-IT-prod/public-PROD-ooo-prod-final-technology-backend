from repositories.base import SQLAlchemyRepository
from models import Admin


class AdminRepository(SQLAlchemyRepository):
    model = Admin
