from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from sqlalchemy.orm import Session
from app.shemas.auth_schema import (
ChangePassword,RefreshTokenRequest,LogoutRequest
)
from app.dependencies.auth_dependencies import (get_current_user)

from app.models.uer_models import User

from app.services.auth_service import (
    login_user,
    change_user_password,
    refresh_access_token,
    logout_user
)

router = APIRouter()

@router.put("/cpassword")
def change_password(password_data: ChangePassword, db:Session=Depends(get_db),current_user: User=Depends(get_current_user) ):
    return change_user_password(password_data,current_user,db)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_user(db, form_data) 

@router.post("/refresh")
def refresh_token(refresh_token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    return refresh_access_token(db, refresh_token_data.refresh_token)

@router.post("/logout")
def logout(logout_data: LogoutRequest, db: Session = Depends(get_db)):
    return logout_user(db, logout_data.refresh_token)
