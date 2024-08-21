from sqlalchemy import select, func

from core.exceptions import ConflictError
from models import Event, EventMember, User, Team, Admin
from schemas.event import EventCreateRequest, EventTableResponse, EventUpdateRequest, EventResponse, EventStatsResponse
from schemas.user import UserResponse
from schemas.team import TeamForTable
from utils.unitofwork import IUnitOfWork
import core.exceptions as _exc
from services.google_sheet import GoogleSheetService


class EventService:
    @staticmethod
    async def _check_title(uow: IUnitOfWork, title: str, creator_id: int) -> None:
        if (await uow.event.get(title=title, creator_id=creator_id)) is not None:
            raise ConflictError(detail='Event with this title already exists.')

    @staticmethod
    async def get(uow: IUnitOfWork, **filters) -> EventResponse:
        async with uow:
            event = await uow.event.get(**filters)

            if not event:
                raise _exc.NotFoundError('Event with this attributes does not exist.')

            await uow.commit()

            return EventResponse.model_validate(event, from_attributes=True)

    async def create(self, uow: IUnitOfWork, schema: EventCreateRequest, admin_id: int) -> dict:
        async with uow:
            await self._check_title(uow, schema.title, admin_id)
            result = await uow.event.create({**schema.model_dump(), 'creator_id': admin_id})
            await uow.commit()
            return {'id': result.id}

    @staticmethod
    async def delete(uow: IUnitOfWork, event_id: int):
        async with uow:
            await uow.event.delete(event_id)
            await uow.commit()

    async def update(
            self,
            uow: IUnitOfWork,
            event_id: int,
            schema: EventUpdateRequest,
            admin_id: int,
    ):
        async with uow:
            event = await uow.event.get(id=event_id)

            if event.title != schema.title:
                await self._check_title(uow, schema.title, admin_id)

            await uow.event.update(event_id, schema.model_dump())
            await uow.commit()

    @staticmethod
    async def get_admin_events(uow: IUnitOfWork, admin_id: int) -> list[EventResponse]:
        async with uow:
            result = await uow.event.get_list(creator_id=admin_id)
            events = result['data']

            pydantic_events = [EventResponse.model_validate(
                event,
                from_attributes=True,
            ) for event in events]

            return pydantic_events

    @staticmethod
    async def get_user_events(uow: IUnitOfWork, user_id: int) -> list[EventResponse]:
        async with uow:
            result = (await uow.session.execute(select(Event)
                                                .join(EventMember, EventMember.event_id == Event.id)
                                                .where(EventMember.user_id == user_id))).scalars().all()
            pydantic_events = [EventResponse.model_validate(
                event,
                from_attributes=True,
            ) for event in result]

            return pydantic_events

    @staticmethod
    async def get_event_users(uow: IUnitOfWork, event_id: int) -> list[UserResponse]:
        async with uow:
            result = await uow.session.execute(
                select(User)
                .join(EventMember, EventMember.user_id == User.id)
                .where(EventMember.event_id == event_id),
            )

            event_users = [UserResponse.model_validate(
                user,
                from_attributes=True,
            ) for user in result.scalars().all()]

            return event_users

    async def get_event_stats(self, uow: IUnitOfWork, event_id: int) -> EventStatsResponse:
        async with uow:
            stats = await uow.session.execute(
                select(
                    select(func.count())
                    .select_from(User)
                    .join(
                        EventMember,
                        EventMember.user_id == User.id
                    ).where(
                        EventMember.event_id == event_id
                    ).label('users_qty'),

                    select(func.count())
                    .select_from(Team)
                    .where(
                        Team.event_id == event_id
                    ).label('team_qty'),

                    select(func.count())
                    .select_from(User)
                    .join(
                        EventMember,
                        EventMember.user_id == User.id
                    ).where(
                        EventMember.event_id == event_id,
                        User.profession == 'backend'
                    ).label('backend_qty'),

                    select(func.count())
                    .select_from(User)
                    .join(
                        EventMember,
                        EventMember.user_id == User.id
                    ).where(
                        EventMember.event_id == event_id,
                        User.profession == 'frontend'
                    ).label('frontend_qty'),

                    select(func.count())
                    .select_from(User)
                    .join(
                        EventMember,
                        EventMember.user_id == User.id
                    ).where(
                        EventMember.event_id == event_id,
                        User.profession == 'mobile'
                    ).label('mobile_qty'),
                )
            )

            res = stats.one()

            stats = EventStatsResponse(
                users_qty=res[0],
                teams_qty=res[1],
                backend_qty=res[2],
                frontend_qty=res[3],
                mobile_qty=res[4],
            )

            return stats

    async def get_event_table(self, uow: IUnitOfWork, event_id: int, admin: Admin):
        async with uow:
            event = await uow.event.get(id=event_id)
            stmt = (select(Team)
            .join(Event, Event.id == Team.event_id)
            .where(
                Team.event_id == event_id,
                Event.creator_id == admin.id,
            ))
            print(stmt)
            result = await uow.session.execute(
                stmt
            )

            teams = [TeamForTable.model_validate(
                team,
                from_attributes=True
            ).model_dump() for team in result.scalars().all()]

            event_table = await GoogleSheetService().create_table(olymp_title=event.title, teams=teams)
            return EventTableResponse(table_url=event_table)
