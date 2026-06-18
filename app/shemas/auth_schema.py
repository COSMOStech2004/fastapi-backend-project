
from pydantic import BaseModel, EmailStr, Field

class ChangePassword(BaseModel):
    old_password: str
    new_password: str=Field(min_length=0, description="New password must be at least 6 characters long")

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class LogoutRequest(BaseModel):
    refresh_token: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=1, max_length=100)

class VerifyEmailRequest(BaseModel):
    token: str


class ResendVerificationEmailRequest(BaseModel):
    email: EmailStr