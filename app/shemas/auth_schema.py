
from pydantic import BaseModel, EmailStr, Field

class ChangePassword(BaseModel):
    old_password: str
    new_password: str=Field(min_length=0, description="New password must be at least 6 characters long")