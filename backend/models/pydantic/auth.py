from pydantic import BaseModel, EmailStr

class Login(BaseModel): 
    username: str
    password: str

class Register(Login): 
    email: EmailStr

class ResponseAuthMe(BaseModel):
    id: int
    username: str
    email: str

