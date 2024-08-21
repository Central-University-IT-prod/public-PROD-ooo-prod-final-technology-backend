from pydantic import BaseModel, EmailStr, Field, ConfigDict


class AdminRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class AdminResponse(BaseModel):
    model_config = ConfigDict(extra='ignore')

    email: EmailStr


class AdminChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str
