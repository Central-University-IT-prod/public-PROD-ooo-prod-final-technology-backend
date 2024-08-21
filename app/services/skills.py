from sqlalchemy import delete

from utils.unitofwork import IUnitOfWork
from schemas.skill import SkillResponse
from models.user_skills import UserSkills
import core.exceptions as _exc
from models.user import User


class SkillService:
    @staticmethod
    async def _check_skill_qty(
        uow: IUnitOfWork,
        user: User,
    ) -> None:
        if len(user.skills) + 1 > 5:
            raise _exc.ConflictError('You reach user skills quantity limit (5)')

    @staticmethod
    async def _check_skill_unique(
        uow: IUnitOfWork,
        user_id: int,
        skill_id: int,
    ) -> None:
        async with uow:
            user_skill = await uow.user_skills.get(user_id=user_id, skill_id=skill_id)

            if user_skill:
                raise _exc.ConflictError('User already have this skill.')

    @staticmethod
    async def get_skills_list(uow: IUnitOfWork) -> list[SkillResponse]:
        async with uow:
            skills_list = await uow.skill.get_list()
            skills_list = skills_list['data']

            skills_list = [SkillResponse.model_validate(
                skill,
                from_attributes=True
            ) for skill in skills_list]

            await uow.commit()

            return skills_list

    async def add_user_skill(self, uow: IUnitOfWork, user: User, skill_id: int) -> None:
        async with uow:
            await self._check_skill_qty(uow, user)
            await self._check_skill_unique(uow, user.id, skill_id)
            await uow.user_skills.create(dict(user_id=user.id, skill_id=skill_id))
            await uow.commit()

    @staticmethod
    async def remove_user_skill(uow: IUnitOfWork, user_id: int, skill_id: int) -> None:
        async with uow:
            await uow.session.execute(
                delete(UserSkills)
                .where(
                    UserSkills.user_id == user_id,
                    UserSkills.skill_id == skill_id,
                ),
            )
            await uow.commit()
