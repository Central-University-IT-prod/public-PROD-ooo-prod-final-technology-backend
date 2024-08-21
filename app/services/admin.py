import core.exceptions as _exc 
from core.security import get_password_hash, verify_password
from models import Admin
import schemas.admin as _admin_schemas
from schemas.token import TokenResponse
from services.jwt import JWTService
from utils.unitofwork import IUnitOfWork
from utils.time import get_utc


class AdminService:
    @staticmethod
    async def _check_email(
        uow: IUnitOfWork,
        email: str,
    ) -> None:
        if (await uow.admin.get(email=email)) is not None:
            raise _exc.ConflictError(detail='Admin with this email already exists.')

    @staticmethod
    async def get(uow: IUnitOfWork, **filters) -> Admin:
        async with uow:
            admin = await uow.admin.get(**filters)

            if not admin:
                raise _exc.NotFoundError('Admin with this id does not exist')
            
            await uow.commit()

            return admin

    async def create(self, uow: IUnitOfWork, schema: _admin_schemas.AdminRegisterRequest) -> TokenResponse:
        async with uow:
            await self._check_email(uow, schema.email)
            schema.password = get_password_hash(schema.password)
            admin = await uow.admin.create(schema.model_dump())
            await uow.commit()
            access_token = JWTService().create_token(admin.id, 'admin')
            return TokenResponse(access_token=access_token)

    @staticmethod
    async def update_password(
        uow: IUnitOfWork,
        admin: Admin,
        schema: _admin_schemas.AdminChangePasswordRequest,
    ) -> TokenResponse:
        async with uow:
            if not verify_password(schema.old_password, admin.password):
                raise _exc.ForbiddenError(detail="Current password not match")

            admin.password = get_password_hash(schema.new_password)
            admin.password_updated_at = get_utc()

            uow.session.add(admin)
            await uow.commit()

            token = JWTService().create_token(admin.id, 'admin')

            return TokenResponse(access_token=token)

    @staticmethod
    async def sign_in(uow: IUnitOfWork, schema: _admin_schemas.AdminLoginRequest) -> TokenResponse:
        async with uow:
            user = await uow.admin.get(email=schema.email)

            if not user or not verify_password(schema.password, user.password):
                raise _exc.AuthError(detail="Invalid login or password.")

            token = JWTService().create_token(user.id, 'admin')
            return TokenResponse(access_token=token)
