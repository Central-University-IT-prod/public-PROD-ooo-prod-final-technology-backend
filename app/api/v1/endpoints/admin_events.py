from fastapi import APIRouter, status
from core.dependencies import UOW, current_admin_or_error
from services.event import EventService
from schemas.event import EventCreateRequest, EventResponse, EventUpdateRequest
from schemas.user import UserResponse


router = APIRouter(
    prefix="/admin-events",
    tags=["admin-events"],
)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_event(uow: UOW, schema: EventCreateRequest, admin: current_admin_or_error):
    return await EventService().create(uow, schema, admin.id)


@router.delete('/{event_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(uow: UOW, event_id: int, _: current_admin_or_error):
    await EventService().delete(uow, event_id)


@router.patch('/{event_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_event(uow: UOW, event_id: int, schema: EventUpdateRequest, admin: current_admin_or_error):
    await EventService().update(
        uow,
        event_id,
        schema,
        admin_id=admin.id,
    )


@router.get('', response_model=list[EventResponse])
async def get_admin_events(uow: UOW, admin: current_admin_or_error):
    return await EventService().get_admin_events(uow, admin.id)


@router.get('/event-users', response_model=list[UserResponse])
async def get_event_users(uow: UOW, event_id: int):
    return await EventService().get_event_users(uow, event_id=event_id)


@router.get('/stats')
async def get_event_stats(uow: UOW, event_id: int):
    return await EventService().get_event_stats(uow, event_id=event_id)
