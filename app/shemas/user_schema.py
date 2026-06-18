from dataclasses import field
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, List


class UserCreate(BaseModel):
    name: str=Field(min_length=1, max_length=50)
    age: int=Field(ge=18, le=120)
    email: EmailStr
    password: str=Field(min_length=1, description="Password must be at least 6 characters long")

    
class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr
    role: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PaginatedUserResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: List[UserResponse]

class UserLogin(BaseModel):
    email: EmailStr
    password: str=Field(min_length=1, description="Password must be at least 6 characters long")

class UpdateUser(BaseModel):
    name: str=Field(min_length=1, max_length=50)
    age: int =Field(ge=18, le=120)
    email: EmailStr

class PartialUpdateUser(BaseModel):
     name: str | None = Field(default=None, min_length=1, max_length=50)
     age: int | None = Field(default=None, ge=18, le=120)
     email: EmailStr | None = Field(default=None)


class DeactivateAccountRequest(BaseModel):
    password: str = Field(min_length=1, max_length=100)
    