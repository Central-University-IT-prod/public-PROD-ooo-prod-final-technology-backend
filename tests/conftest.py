import datetime as dt
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from core.database import Base
from core.config import config
from schemas.admin import AdminRegisterRequest
from schemas.event import EventCreateRequest
from schemas.team import TeamCreateRequest
from schemas.user import UserRegisterRequest
from services.user import UserService
from services.admin import AdminService
from main import app
from utils.unitofwork import UnitOfWork
from services.team import TeamService
from services.jwt import JWTService
from services.event import EventService
from utils.time import get_utc

# DATABASE
DATABASE_URL_TEST = config.TEST_DATABASE_URI

engine_test = create_async_engine(DATABASE_URL_TEST)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)
Base.metadata.bind = engine_test


@pytest.fixture(autouse=True, scope='function')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        from sqlalchemy import text
        with open("database-init.sql") as file:
            try:
                query = text(file.read())
                await conn.execute(query)
                await conn.commit()
            except:
                print('Skills table already filled')
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session", autouse=False)
async def async_client():
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.fixture(scope="function")
async def async_session(prepare_database) -> AsyncSession:
    session = async_session_maker()
    yield session


@pytest.fixture(scope='function')
async def uow():
    uow = UnitOfWork()
    yield uow


@pytest.fixture(scope="function")
async def user_token(uow):
    user_schema = UserRegisterRequest(email='testemail@mail.ru',
                                      fullname='test_test',
                                      password='test_password',
                                      telegram_username='test_telegram_user',
                                      age=1,
                                      profession='backend',
                                      bio='backend',
                                      skills=[1, 2, 3])
    token = await UserService().create(uow, user_schema)
    yield token.access_token


@pytest.fixture(scope="function")
async def user_token2(uow):
    user_schema = UserRegisterRequest(email='testemail1@mail.ru',
                                      fullname='test_test',
                                      password='test_password',
                                      telegram_username='test_telegram_user',
                                      age=1,
                                      profession='backend',
                                      bio='backend',
                                      skills=[1, 2, 3])
    token = await UserService().create(uow, user_schema)
    yield token.access_token


@pytest.fixture(scope="function")
async def admin_token(uow):
    admin_schema = AdminRegisterRequest(email='testemail@mail.ru',
                                        password='test_password')
    token = await AdminService().create(uow, admin_schema)
    yield token.access_token


@pytest.fixture(scope='function')
async def event_id(uow, admin_token):
    token_data = JWTService().get_token_data(admin_token)
    schema = EventCreateRequest(
        title='Title',
        max_member_qty=3,
        team_creation_deadline=(get_utc() + dt.timedelta(days=3)).date()
    )
    event = await EventService().create(uow, schema, token_data['id'])

    return event['id']


@pytest.fixture(scope='function')
async def team_id(uow, event_id, user_token):
    schema = TeamCreateRequest(
        title='Title',
        description='Description',
        event_id=event_id
    )
    token_data = JWTService().get_token_data(user_token)
    team = await TeamService().create_team(uow, schema, token_data['id'])

    return team['id']
