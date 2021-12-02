from pydantic import BaseModel, Field
from typing import List
from enum import Enum

from pydantic.networks import EmailStr

class Role(str, Enum):
    admin = "admin"
    user = "user"

class User(BaseModel):
    user: str = Field(...)
    password: str = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    roles: List[Role]

class UpdateUserModel(BaseModel):
    password: str = Field(...)
    name: str = Field(...)
    roles: List[Role]

class UpdateUserPassword(BaseModel):
    password: str = Field(...)

class UpdateUserName(BaseModel):
    name: str = Field(...)

class UpdateUserRoles(BaseModel):
    roles: List[Role]

class AuthUser(BaseModel):
    user: str = Field(...)
    password: str = Field(...)

def ErrorResponse(error, code, message):
    return {'error': error, 'code': code, 'message': message}

def SuccessResponse(data, message):
    return {'data': [data], 'code': 200, 'message': message}
