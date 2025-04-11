from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr

class User(UserBase):
    id: str | None = None
    password: str

class UserPublic(UserBase):
    id: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserAuth(UserPublic):
    access_token: str    