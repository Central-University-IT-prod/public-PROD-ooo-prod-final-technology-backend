from sqlalchemy import insert, update, select

from utils.unitofwork import IUnitOfWork
import core.exceptions as _exc
from services.google_sheet import GoogleSheetService
from schemas.upload_members import UploadMembersRequest
from models import EventMember, User


class UploadMembersService:
    @staticmethod
    async def _check_admin_permissions(
        uow: IUnitOfWork,
        admin_id: int,
        event_id: int,
    ) -> None:
        async with uow:
            event = await uow.event.get(id=event_id, creator_id=admin_id)

            if not event:
                raise _exc.ForbiddenError(
                    'Admin have not got permissions to upload members or event with this id does not exist',
                )

    @staticmethod
    async def _check_duplicate_members(
        uow: IUnitOfWork,
        emails: list[str],
        event_id: int, \
    ) -> None:
        async with uow:
            result = await uow.event_members.get_list(user_email=emails, event_id=event_id)

            if len(result['data']):
                raise _exc.ConflictError('Duplicate user email in db')

    async def upload_members(
        self,
        uow: IUnitOfWork,
        schema: UploadMembersRequest,
        admin_id: int,
    ) -> tuple[list[str], str]:
        async with uow:
            await self._check_admin_permissions(uow, admin_id, schema.event_id)

            data = await GoogleSheetService().fetch_by_url(schema.spreadsheet_url)

            emails = [member['email'] for member in data]

            if len(emails) != len(set(emails)):
                raise _exc.ConflictError('Duplicate user email in spreadsheet')

            await self._check_duplicate_members(uow, emails, schema.event_id)

            new_data = [dict()] * len(data)
 
            try:
                for index, member in enumerate(data):
                    new_data[index] = {
                        'user_email': member['email'],
                        'score': int(member['score']),
                        'event_id': schema.event_id,
                    }
            except ValueError:
                raise _exc.BadRequestError('Score is incorrect')

            await uow.session.execute(
                insert(EventMember),
                new_data,
            )

            await uow.commit()

            subquery = select(User.id).where(
                User.email == EventMember.user_email,
                EventMember.event_id == schema.event_id,
            )

            await uow.session.execute(
                update(EventMember)
                .values(user_id=subquery)
                .where(EventMember.event_id == schema.event_id)
            )

            event = await uow.event.get(id=schema.event_id)

            await uow.commit()
            return emails, event.title
