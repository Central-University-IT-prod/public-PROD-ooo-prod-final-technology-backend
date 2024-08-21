from fastapi import APIRouter
from core.dependencies import UOW, current_admin_or_error
from schemas.token import TokenResponse
from services.admin import AdminService
from schemas.admin import (
    AdminLoginRequest,
    AdminResponse,
    AdminRegisterRequest,
    AdminChangePasswordRequest,
)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.post('', response_model=TokenResponse)
async def create_admin(uow: UOW, schema: AdminRegisterRequest):
    return await AdminService().create(uow, schema)


@router.post('/login', response_model=TokenResponse)
async def login_admin(uow: UOW, schema: AdminLoginRequest):
    return await AdminService().sign_in(uow, schema)


@router.get('/me', response_model=AdminResponse)
async def get_admin_profile(admin: current_admin_or_error):
    return AdminResponse.model_validate(admin, from_attributes=True)


@router.post('/update_password')
async def change_password_admin(
    uow: UOW,
    admin: current_admin_or_error,
    schema: AdminChangePasswordRequest,
):
    return await AdminService().update_password(uow, admin, schema)
