from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.uer_models import User
from app.security import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token")

    user = db.query(User).filter(
        User.id == user_id,
        User.is_deleted == False
    ).first()

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    return user


def get_current_admin_user(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required")

    return current_user