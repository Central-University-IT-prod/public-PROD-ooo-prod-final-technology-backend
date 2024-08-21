from typing import Annotated

from fastapi import Depends

from core.exceptions import AuthError
from core.security import JWTBearer
from models.user import User
from models.admin import Admin
from services.admin import AdminService
from services.jwt import JWTService
from services.user import UserService
from utils.unitofwork import IUnitOfWork, UnitOfWork


UOW = Annotated[IUnitOfWork, Depends(UnitOfWork)]


async def get_current_user(
    uow: UOW,
    token: str = Depends(JWTBearer()),
) -> User:
    if not token:
        raise AuthError(detail='Invalid authorization token.')

    token_data = JWTService().get_token_data(token)

    if not token_data or token_data.get('type') != 'user':
        raise AuthError(detail='Invalid authorization token.')
    
    user = await UserService().get(uow, id=token_data['id'])

    if not user:
        raise AuthError(detail='Invalid authorization token.')

    if int(user.password_updated_at.timestamp()) > token_data['iat']:
        raise AuthError(detail='Invalid authorization token.')

    return user


current_user_or_error = Annotated[User, Depends(get_current_user)]


async def get_current_admin(
    uow: UOW,
    token: str = Depends(JWTBearer())
) -> Admin:
    if not token:
        raise AuthError(detail='Invalid authorization token.')

    token_data = JWTService().get_token_data(token)

    if not token_data or token_data.get('type') != 'admin':
        raise AuthError(detail='Invalid authorization token.')
    
    admin = await AdminService().get(uow, id=token_data['id'])

    if not admin:
        raise AuthError(detail='Invalid authorization token.')

    if int(admin.password_updated_at.timestamp()) > token_data['iat']:
        raise AuthError(detail='Invalid authorization token.')

    return admin


current_admin_or_error = Annotated[User, Depends(get_current_admin)]
