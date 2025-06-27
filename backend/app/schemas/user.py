from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    full_name: str
    password: str

class UserOut(UserBase):
    id: int
    full_name: str
    is_active: bool