from fastapi import APIRouter, status
from core.dependencies import UOW, current_user_or_error
from services.team import TeamService
from schemas.team import TeamCreateRequest, AcceptRequestRequest, SendInviteRequest, AcceptInviteRequest, TeamResponse
from schemas.user import UserResponse

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
)
async def create_team(
        uow: UOW,
        user: current_user_or_error,
        schema: TeamCreateRequest,
):
    return await TeamService().create_team(uow, schema=schema, user_id=user.id)


@router.post(
    '/req/{team_id}',
    status_code=status.HTTP_201_CREATED,
)
async def send_request_to_team(
        uow: UOW,
        team_id: int,
        user: current_user_or_error,
):
    return await TeamService().send_team_request(uow, user_id=user.id, team_id=team_id)


@router.get('/requests')
async def get_team_request(
        uow: UOW,
        user: current_user_or_error,
        event_id: int,
):
    return await TeamService().get_team_requests(uow, leader_id=user.id, event_id=event_id)


@router.post('/req-accept')
async def accept_user_request(
        uow: UOW,
        user: current_user_or_error,
        schema: AcceptRequestRequest,
):
    return await TeamService().accept_user_request(uow, schema=schema, user=user)


@router.post('/invite')
async def invite_user(
        uow: UOW,
        user: current_user_or_error,
        schema: SendInviteRequest,
):
    return await TeamService().send_invite(uow, schema=schema, leader_id=user.id)


@router.get('/invites')
async def get_user_invites(
        uow: UOW,
        user: current_user_or_error,
        event_id: int,
):
    return await TeamService().get_user_invites(uow, user_id=user.id, event_id=event_id)


@router.post('/accept')
async def accept_invite(
        uow: UOW,
        user: current_user_or_error,
        schema: AcceptInviteRequest,
):
    return await TeamService().accept_invite(uow, user=user, schema=schema)


@router.get('/{team_id}')
async def get_team_by_id(uow: UOW, team_id: int) -> TeamResponse:
    return await TeamService().get_team(uow, id=team_id)


@router.get('')
async def get_teams_by_event_id(uow: UOW, event_id: int) -> list[TeamResponse]:
    return await TeamService().get_team_list(uow, event_id=event_id)
