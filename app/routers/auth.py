from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from sqlalchemy.orm import Session
from app.shemas.auth_schema import (
ChangePassword,RefreshTokenRequest,LogoutRequest,ForgotPasswordRequest,ResetPasswordRequest,VerifyEmailRequest,ResendVerificationEmailRequest
)
from app.dependencies.auth_dependencies import (get_current_user)
from app.models.uer_models import User
from app.dependencies.rate_limit_dependency import (login_rate_limit,forgot_password_rate_limit,resend_verification_rate_limit)
from app.services.auth_service import (login_user,change_password,refresh_access_token,logout_user,logout_all_devices,forgot_password,reset_password,verify_email,resend_verification_email,get_active_sessions,revoke_session
)

router = APIRouter()

@router.put("/cpassword")
def change_password(password_data: ChangePassword, db:Session=Depends(get_db),current_user: User=Depends(get_current_user) ):
    return change_password(password_data,current_user,db)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db),  _: None = Depends(login_rate_limit)):
    return login_user(db, form_data) 

@router.post("/refresh")
def refresh_token(refresh_token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    return refresh_access_token(db, refresh_token_data.refresh_token)

@router.post("/logout")
def logout(logout_data: LogoutRequest, db: Session = Depends(get_db)):
    return logout_user(db, logout_data.refresh_token)

@router.post("/logout-all")
def logout_all(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return logout_all_devices(db,current_user)

@router.post("/forgot-password")
def forgot_user_password(forgot_data: ForgotPasswordRequest, db: Session = Depends(get_db), _: None = Depends(forgot_password_rate_limit)):
    return forgot_password(db, forgot_data.email)

@router.post("/reset-password")
def reset_user_password(reset_data: ResetPasswordRequest, db: Session = Depends(get_db)):
    return reset_password(db, reset_data.token, reset_data.new_password)

@router.post("/verify-email")
def verify_user_email(verification_data: VerifyEmailRequest,db: Session = Depends(get_db)):
    return verify_email(db,verification_data.token)

@router.post("/resend-verification-email")
def resend_user_verification_email(verification_data: ResendVerificationEmailRequest,db: Session = Depends(get_db),_: None = Depends(resend_verification_rate_limit)):
    return resend_verification_email(db,verification_data.email)

@router.get("/sessions")
def list_active_sessions(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return get_active_sessions(db,current_user)


@router.delete("/sessions/{session_id}")
def revoke_user_session(session_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return revoke_session(db,current_user,session_id)