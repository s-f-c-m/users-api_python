from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"

class User(BaseModel):
    user: str = Field(...)
    password: str = Field(...)
    name: str = Field(...)
    roles: List[Role]

class UpdateUserModel(BaseModel):
    password: str = Field(...)
    name: str = Field(...)
    roles: List[Role]

class AuthUser(BaseModel):
    user: str = Field(...)
    password: str = Field(...)
