from fastapi import APIRouter
from core.dependencies import UOW
from services.skills import SkillService
from schemas.skill import SkillResponse


router = APIRouter(
    prefix="/skills",
    tags=["skills"],
)


@router.get('', response_model=list[SkillResponse])
async def get_event(uow: UOW):
    return await SkillService().get_skills_list(uow)
