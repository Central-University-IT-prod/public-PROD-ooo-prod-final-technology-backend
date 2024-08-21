from fastapi import APIRouter, status
from core.dependencies import UOW
from services.skills import SkillService
from schemas.skill import AddSkillToUser, RemoveSkillFromUser
from core.dependencies import current_user_or_error


router = APIRouter(
    prefix="/user-skills",
    tags=["user-skills"],
)


@router.post('', status_code=status.HTTP_202_ACCEPTED)
async def add_skill_to_user(
    uow: UOW,
    user: current_user_or_error,
    schema: AddSkillToUser,
):
    return await SkillService().add_user_skill(uow, user=user, skill_id=schema.skill_id)


@router.delete('', status_code=status.HTTP_202_ACCEPTED)
async def remove_skill_from_user(
    uow: UOW,
    user: current_user_or_error,
    schema: RemoveSkillFromUser,
):
    return await SkillService().remove_user_skill(uow, user_id=user.id, skill_id=schema.skill_id)
