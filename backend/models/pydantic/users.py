from config import UserRole
from pydantic import BaseModel, EmailStr
from typing import Literal

class UserSchema(BaseModel): 
    id: int
    username: str
    email: str

class UpdateSchema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class ResponseMe(BaseModel):
    username: str
    email: EmailStr

class UpdateUser(UpdateSchema):
    role: Literal["member", "manager", "admin"] | None = None

class UpdateMe(UpdateSchema): pass