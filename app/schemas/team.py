from pydantic import BaseModel, Field
from schemas.user import UserResponse


class TeamCreateRequest(BaseModel):
    title: str = Field(min_length=3, max_length=30)
    description: str = Field(min_length=3, max_length=100)
    event_id: int


class TeamResponse(BaseModel):
    id: int
    members: list[UserResponse]
    title: str
    description: str


class RequestResponse(BaseModel):
    id: int
    user: UserResponse


class RequestToTeamResponse(BaseModel):
    requests: list[RequestResponse]


class AcceptRequestRequest(BaseModel):
    request_id: int


class SendInviteRequest(BaseModel):
    user_id: int
    event_id: int


class UserInviteReponse(BaseModel):
    id: int
    team: TeamResponse


class AcceptInviteRequest(BaseModel):
    invite_id: int


class TeamForTable(BaseModel):
    title: str
    members: list[UserResponse]
