from fastapi import APIRouter
from core.dependencies import UOW, current_admin_or_error
from schemas.team import TeamResponse
from schemas.user import UserResponse
from services.event import EventService
from schemas.event import EventResponse
from services.team import TeamService


router = APIRouter(
    prefix="/events",
    tags=["events"],
)


@router.get('/free-teams')
async def get_free_teams(
    uow: UOW,
    event_id: int,
) -> list[TeamResponse]:
    return await TeamService().get_free_teams(uow, event_id=event_id)


@router.get('/free-users')
async def get_free_users(
    uow: UOW,
    event_id: int,
) -> list[UserResponse]:
    return await TeamService().get_free_users(uow, event_id=event_id)


@router.get('/event-table')
async def get_event_table(
    uow: UOW,
    event_id: int,
    admin: current_admin_or_error,
):
    return await EventService().get_event_table(uow, admin=admin, event_id=event_id)


@router.get('/{event_id}', response_model=EventResponse)
async def get_event(uow: UOW, event_id: int):
    return await EventService().get(uow, id=event_id)
