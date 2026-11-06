from pydantic import BaseModel
from typing import Literal


class SchemaMember(BaseModel):
    username: str
    email: str
    role: str


class ResponseMembers(SchemaMember):
    pass


class CreateMember(BaseModel):
    username: str
    role: Literal["admin", "member", "manager"] | None = None


class UpdateMember(BaseModel):
    role: Literal["admin", "member", "manager"] | None = None


class ResponseUpdateMember(BaseModel):
    project_id: int
    user_id: int
    role: str
