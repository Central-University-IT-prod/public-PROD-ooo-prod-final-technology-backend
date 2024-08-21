from fastapi import APIRouter
from core.dependencies import UOW, current_user_or_error
from services.event import EventService
from schemas.event import EventResponse


router = APIRouter(
    prefix="/user-events",
    tags=["user-events"],
)


@router.get('', response_model=list[EventResponse])
async def get_user_events(uow: UOW, current_user: current_user_or_error):
    return await EventService().get_user_events(uow, current_user.id)
