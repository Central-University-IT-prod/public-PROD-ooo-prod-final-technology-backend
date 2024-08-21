from sqlalchemy import delete, insert, update, select
import core.exceptions as _exc
from core.security import get_password_hash, verify_password
from models import User, EventMember, UserSkills, User, Team, TeamMember
from schemas.user import UserRegisterRequest, IsInTeamResponse, UserChangePasswordRequest, UserLoginRequest, UserUpdateRequest
from services.jwt import JWTService
from utils.unitofwork import IUnitOfWork
from schemas.token import TokenResponse
from utils.time import get_utc


class UserService:
    @staticmethod
    async def _check_email(uow: IUnitOfWork, email: str) -> None:
        if (await uow.user.get(email=email)) is not None:
            raise _exc.ConflictError(detail='User with this email already exists.')

    @staticmethod
    async def _check_skills(uow: IUnitOfWork, skills_ids: list[int]) -> None:
        skills_from_db = await uow.skill.get_list(id=skills_ids)

        if len(skills_from_db['data']) < len(skills_ids):
            raise _exc.BadRequestError('Skill with this id does not exist')

    @staticmethod
    async def get(uow: IUnitOfWork, **filters) -> User | None:
        async with uow:
            user = await uow.user.get(**filters)

            if not user:
                raise _exc.NotFoundError('User with this attributes does not exist.')

            await uow.session.commit()

            return user

    async def create(self, uow: IUnitOfWork, schema: UserRegisterRequest) -> TokenResponse:
        async with uow:
            await self._check_email(uow, schema.email)
            await self._check_skills(uow, schema.skills)

            schema.password = get_password_hash(schema.password)

            user = await uow.user.create(schema.model_dump(exclude={'skills'}))

            await uow.session.refresh(user)

            await uow.session.execute(
                update(EventMember)
                .values(user_id=user.id)
                .where(EventMember.user_email == schema.email),
            )

            new_skills = [dict()] * len(schema.skills)

            for index, skill in enumerate(schema.skills):
                new_skills[index] = {'user_id': user.id, 'skill_id': skill}

            await uow.session.execute(
                insert(UserSkills),
                new_skills,
            )

            access_token = JWTService().create_token(user.id, 'user')

            await uow.commit()

            return TokenResponse(access_token=access_token)

    @staticmethod
    async def update_password(
        uow: IUnitOfWork,
        user: User,
        schema: UserChangePasswordRequest,
    ) -> TokenResponse:
        async with uow:
            if not verify_password(schema.old_password, user.password):
                raise _exc.ForbiddenError(detail="Current password not match")

            user.password = get_password_hash(schema.new_password)
            user.password_updated_at = get_utc()

            uow.session.add(user)
            await uow.commit()

            token = JWTService().create_token(user.id, 'user')

            return TokenResponse(access_token=token)

    @staticmethod
    async def sign_in(uow: IUnitOfWork, schema: UserLoginRequest):
        async with uow:
            find_user = await uow.user.get(email=schema.email)
            if find_user is not None and verify_password(schema.password, find_user.password):
                token = JWTService().create_token(find_user.id, 'user')
                await uow.commit()
                return token
            raise _exc.AuthError(detail="Invalid login or password.")

    async def update(
        self,
        uow: IUnitOfWork,
        user: User,
        schema: UserUpdateRequest
    ) -> User:
        async with uow:
            await self._check_skills(uow, schema.skills)

            user = await uow.user.update(user.id, schema.model_dump(exclude_none=True, exclude={'skills'}))

            await uow.session.execute(
                delete(UserSkills)
                .where(UserSkills.user_id == user.id)
            )

            new_skills = [dict()] * len(schema.skills)

            for index, skill in enumerate(schema.skills):
                new_skills[index] = {'user_id': user.id, 'skill_id': skill}

            await uow.session.execute(
                insert(UserSkills),
                new_skills,
            )

            await uow.commit()
            return user

    async def is_in_team(self, uow: IUnitOfWork, user: User, event_id: int):
        async with uow:
            result = await uow.session.execute(
                select(TeamMember.team_id)
                .join(Team, Team.id == TeamMember.team_id)
                .where(
                    Team.event_id == event_id,
                    TeamMember.user_id == user.id,
                )
            )

            return IsInTeamResponse(team_id=result.scalar())
