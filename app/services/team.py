from sqlalchemy import select, not_

from schemas.team import TeamCreateRequest

from utils.unitofwork import IUnitOfWork
import core.exceptions as _exc
from models import Team, TeamMember, RequestToTeam, User, InvitationToUser, EventMember
from schemas.team import *


class TeamService:
    @staticmethod
    async def _check_title(uow: IUnitOfWork, title: str, event_id: int) -> None:
        if (await uow.teams.get(title=title, event_id=event_id)) is not None:
            raise _exc.ConflictError(detail='Team with this title already exists.')

    @staticmethod
    async def _check_is_user_in_team(
        uow: IUnitOfWork,
        creator_id: int,
        event_id: int,
    ) -> None:
        creator_teams = await uow.session.execute(
            select(TeamMember)
            .join(
                Team,
                Team.id == TeamMember.team_id,
            ).where(
                Team.event_id == event_id,
                TeamMember.user_id == creator_id,
            )
        )

        if len(creator_teams.all()):
            raise _exc.ConflictError('User cannot create team if it is in team')

    @staticmethod
    async def _send_invite(uow: IUnitOfWork, user_id: int, team_id: int):
        await uow.invitation_to_team.create({'user_id': user_id, 'team_id': team_id})
        await uow.commit()

    async def create_team(
        self,
        uow: IUnitOfWork,
        schema: TeamCreateRequest,
        user_id: int,
    ) -> dict:
        async with uow:
            await self._check_title(uow, schema.title, schema.event_id)
            await self._check_is_user_in_team(uow, creator_id=user_id, event_id=schema.event_id)

            team = await uow.teams.create({**schema.model_dump(), 'leader_id': user_id})

            await uow.session.refresh(team)

            await uow.team_members.create({'user_id': user_id, 'team_id': team.id})

            await uow.commit()

            return {'id': team.id}

    async def send_team_request(
        self,
        uow: IUnitOfWork,
        user_id: int,
        team_id: int,
    ) -> dict:
        async with uow:
            res = await uow.session.execute(
                select(Team.event_id)
                .join(
                    TeamMember,
                    TeamMember.team_id == Team.id,
                )
                .where(
                    Team.id == team_id,
                )
            )

            event_id = res.scalar()

            if not event_id:
                raise _exc.NotFoundError('Team with this id does not exist')

            await self._check_is_user_in_team(uow, user_id, event_id=event_id)

            request_to_team = await uow.request_to_team.create({'user_id': user_id, 'team_id': team_id})
            await uow.commit()
            return {'id': request_to_team.id}

    @staticmethod
    async def get_team_requests(
        uow: IUnitOfWork,
        leader_id: int,
        event_id: int,
    ) -> RequestToTeamResponse:
        async with uow:
            result = await uow.session.execute(
                select(RequestToTeam.id, User)
                .join(RequestToTeam, RequestToTeam.user_id == User.id)
                .join(Team, Team.id == RequestToTeam.team_id)
                .where(
                    Team.leader_id == leader_id,
                    Team.event_id == event_id,
                )
            )

            requests = [RequestResponse(
                id=request[0],
                user=UserResponse.model_validate(request[1], from_attributes=True),
            ) for request in result.all()]

            return RequestToTeamResponse(requests=requests)

    async def accept_user_request(
        self,
        uow: IUnitOfWork,
        schema: AcceptRequestRequest,
        user: User,
    ):
        async with uow:
            request = await uow.request_to_team.get(id=schema.request_id)

            if not request:
                raise _exc.BadRequestError('No request with this id')

            await uow.request_to_team.delete(schema.request_id)

            await self._send_invite(
                uow,
                user_id=request.user_id,
                team_id=request.team_id,
            )

    async def send_invite(
        self,
        uow: IUnitOfWork,
        schema: SendInviteRequest,
        leader_id: int,
    ):
        async with uow:
            team = await uow.teams.get(leader_id=leader_id, event_id=schema.event_id)

            await self._send_invite(
                uow,
                user_id=schema.user_id,
                team_id=team.id,
            )

    @staticmethod
    async def get_user_invites(
        uow: IUnitOfWork,
        user_id: int,
        event_id: int,
    ) -> list[UserInviteReponse]:
        async with uow:
            result = await uow.session.execute(
                select(
                    InvitationToUser.id,
                    Team,
                )
                .join(
                    Team,
                    Team.id == InvitationToUser.team_id,
                )
                .where(
                    InvitationToUser.user_id == user_id,
                    Team.event_id == event_id,
                )
            )

            invites = [UserInviteReponse(
                id=invite[0],
                team=TeamResponse.model_validate(invite[1], from_attributes=True),
            ) for invite in result.all()]

            return invites

    async def accept_invite(
        self,
        uow: IUnitOfWork,
        user: User,
        schema: AcceptInviteRequest,
    ):
        async with uow:
            invite = await uow.invitation_to_team.get(id=schema.invite_id)

            if invite is None:
                raise _exc.NotFoundError('Invitation with this id does not found')

            if invite.user_id != user.id:
                raise _exc.ForbiddenError('You cannot accept this invitation')

            await uow.invitation_to_team.delete(schema.invite_id)

            team = await uow.teams.get(id=invite.team_id)

            members_qty = len(team.members)

            event = await uow.event.get(id=team.event_id)

            await self._check_is_user_in_team(uow, user.id, event.id)

            if members_qty + 1 > event.max_member_qty:
                raise _exc.ConflictError('Max member qty reach')

            await uow.team_members.create({'user_id': user.id, 'team_id': team.id})

            await uow.commit()

    @staticmethod
    async def get_free_teams(
        uow: IUnitOfWork,
        event_id: int,
    ) -> list[TeamResponse]:
        async with uow:
            free_teams = (await uow.teams.get_list(event_id=event_id))['data']

            free_teams = sorted(free_teams, key=lambda x: len(x.members))

            teams = [TeamResponse.model_validate(
                team,
                from_attributes=True,
            ) for team in free_teams]

            return teams

    @staticmethod
    async def get_free_users(
        uow: IUnitOfWork,
        event_id: int,
    ) -> list[UserResponse]:
        async with uow:
            busy_users_subquery = select(TeamMember.user_id)\
                .join(Team, Team.id == TeamMember.team_id)\
                .where(Team.event_id == event_id)

            free_event_users = (await uow.session.execute(
                select(User)
                .join(
                    EventMember,
                    EventMember.user_id == User.id
                )
                .where(
                    EventMember.event_id == event_id,
                    not_(EventMember.user_id.in_(busy_users_subquery)),
                ),
            )).scalars().all()

            free_event_users = [UserResponse.model_validate(
                user,
                from_attributes=True,
            ) for user in free_event_users]

            return free_event_users

    @staticmethod
    async def get_team(
            uow: IUnitOfWork,
            **filters,
    ) -> TeamResponse:
        async with uow:
            team = await uow.teams.get(**filters)
            return TeamResponse.model_validate(team, from_attributes=True)

    @staticmethod
    async def get_team_list(
            uow: IUnitOfWork,
            **filters,
    ) -> list[TeamResponse]:
        async with uow:
            teams = (await uow.teams.get_list(**filters))['data']
            return [TeamResponse.model_validate(team, from_attributes=True) for team in teams]
