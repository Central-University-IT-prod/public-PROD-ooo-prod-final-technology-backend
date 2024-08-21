from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from schemas.skill import SkillResponse


class ProfessionsEnum(str, Enum):
    mobile = 'mobile'
    backend = 'backend'
    frontend = 'frontend'


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    fullname: str
    telegram_username: str
    profession: ProfessionsEnum
    skills: list[int]
    age: int = Field(ge=1)
    bio: str = Field(max_length=250)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    fullname: str
    telegram_username: str
    skills: list[SkillResponse]
    age: int
    profession: str
    bio: str


class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    fullname: str
    telegram_username: str
    skills: list[int] = Field(max_length=5)


class IsInTeamResponse(BaseModel):
    team_id: int | None
