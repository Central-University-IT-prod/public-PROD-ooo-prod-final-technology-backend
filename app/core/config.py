import os
from datetime import timedelta
from dataclasses import dataclass
from dotenv import load_dotenv
import json


load_dotenv()


@dataclass(frozen=True)
class Config:
    # base
    PROJECT_NAME: str = "TEAM MATCHING API"
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # database
    DB_USER = os.getenv("POSTGRES_USERNAME")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_HOST = os.getenv("POSTGRES_HOST")
    DB_PORT = os.getenv("POSTGRES_PORT")
    DB_NAME = os.getenv("POSTGRES_DATABASE")

    # email
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT"))

    APP_URL = os.getenv("APP_URL")

    GOOGLE_SHEETS_DATA = json.loads(os.getenv("GOOGLE_SHEETS_DATA"))  # type: ignore

    DATABASE_URI = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # DATABASE_URI = f"sqlite+aiosqlite:///{PROJECT_ROOT}/db.db"
    TEST_DATABASE_URI = f"sqlite+aiosqlite:///{PROJECT_ROOT}/test_db.db"

    # auth
    JWT_SECRET = os.getenv("RANDOM_SECRET")
    JWT_EXPIRE: timedelta = timedelta(days=180)


config = Config()
