from fastapi import APIRouter
from core.dependencies import UOW, current_user_or_error
from schemas.token import TokenResponse
from services.user import UserService
from schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    UserUpdateRequest,
    UserChangePasswordRequest,
    IsInTeamResponse,
)


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post('', response_model=TokenResponse)
async def user_register(uow: UOW, schema: UserRegisterRequest):
    return await UserService().create(uow, schema)


@router.post('/login', response_model=TokenResponse)
async def user_login(uow: UOW, schema: UserLoginRequest):
    access_token = await UserService().sign_in(uow, schema)
    return TokenResponse(access_token=access_token)


@router.get('/me', response_model=UserResponse)
async def me(user: current_user_or_error):
    return UserResponse.model_validate(user, from_attributes=True)


@router.put('/update')
async def update(uow: UOW, user: current_user_or_error, schema: UserUpdateRequest):
    return await UserService().update(uow, user, schema)


@router.post('/update_password')
async def update_password(
    uow: UOW,
    user: current_user_or_error,
    schema: UserChangePasswordRequest,
):
    return await UserService().update_password(uow, user, schema)


@router.get('/is_in_team', response_model=IsInTeamResponse)
async def is_me_in_team(
    uow: UOW,
    user: current_user_or_error,
    event_id: int,
):
    return await UserService().is_in_team(uow, user=user, event_id=event_id)
