from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import async_session_maker
from repositories.user import UserRepository
from repositories.admin import AdminRepository
from repositories.event import EventRepository
from repositories.skill import SkillRepository
from repositories.user_skills import UserSkillRepository
from repositories.event_members import EventMemberRepository
from repositories.team import TeamRepository
from repositories.team_members import TeamMemberRepository
from repositories.invitation_to_user import InvitationToUserRepository
from repositories.request_to_team import RequestToTeamRepository


class IUnitOfWork(ABC):
    session: AsyncSession
    user: UserRepository
    admin: AdminRepository
    event: EventRepository
    skill: SkillRepository
    user_skills: UserSkillRepository
    event_members: EventMemberRepository
    teams: TeamRepository
    team_members: TeamMemberRepository
    invitation_to_team: InvitationToUserRepository
    request_to_team: RequestToTeamRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.admin = AdminRepository(self.session)
        self.user = UserRepository(self.session)
        self.event = EventRepository(self.session)
        self.skill = SkillRepository(self.session)
        self.user_skills = UserSkillRepository(self.session)
        self.event_members = EventMemberRepository(self.session)
        self.teams = TeamRepository(self.session)
        self.team_members = TeamMemberRepository(self.session)
        self.invitation_to_team = InvitationToUserRepository(self.session)
        self.request_to_team = RequestToTeamRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
