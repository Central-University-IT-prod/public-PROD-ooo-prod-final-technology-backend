from datetime import date
from typing import Annotated

from pydantic import BaseModel, AfterValidator

from utils.validators import validate_team_creation_deadline, validate_max_member_qty


TeamCreationDeadline = Annotated[date, AfterValidator(validate_team_creation_deadline)]
MaxMembetQty = Annotated[int, AfterValidator(validate_max_member_qty)]


class EventCreateRequest(BaseModel):
    title: str
    max_member_qty: MaxMembetQty
    team_creation_deadline: TeamCreationDeadline


class EventResponse(BaseModel):
    id: int
    title: str
    max_member_qty: int
    team_creation_deadline: date


class EventUpdateRequest(BaseModel):
    title: str
    max_member_qty: int


class EventStatsResponse(BaseModel):
    users_qty: int
    teams_qty: int
    backend_qty: int
    frontend_qty: int
    mobile_qty: int


class EventTableResponse(BaseModel):
    table_url: str
