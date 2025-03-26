from pydantic import BaseModel, ConfigDict
from datetime import datetime


class LoginUserSchema(BaseModel):
    login: str
    password: str


class AddUserSchema(BaseModel):
    full_name: str
    login: str
    hashed_password: str
    phone: str


class RegisterUserSchema(BaseModel):
    full_name: str
    login: str
    password1: str
    password2: str
    phone: str


class ReadUserSchema(BaseModel):
    id: int
    full_name: str
    login: str
    hashed_password: str
    phone: str
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenSchema(BaseModel):
    access_token: str
