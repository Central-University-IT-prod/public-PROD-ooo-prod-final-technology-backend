from datetime import date

from core.exceptions import ValidationError
from utils.time import get_utc


def validate_team_creation_deadline(team_creation_deadline: date) -> date:
    if team_creation_deadline <= get_utc().date():
        raise ValidationError("Date must be in future")

    return team_creation_deadline


def validate_max_member_qty(v: int) -> int:
    if v <= 0:
        raise ValidationError('Minimum 1 member in team')
    
    return v
