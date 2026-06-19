from os import error

from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from app.models.uer_models import  User 
from app.models.refresh_token_model import RefreshToken
from datetime import datetime, timedelta
from app.config import REFRESH_TOKEN_EXPIRE_DAYS, MAX_FAILED_LOGIN_ATTEMPTS, ACCOUNT_LOCKOUT_MINUTES
from fastapi import HTTPException,status
from app.security  import create_access_token, verify_password,hash_password,create_refresh_token,verify_refresh_token
from app.logger import logger
import secrets
from app.models.password_reset_model_token import PasswordResetToken
from app.models.refresh_token_model import RefreshToken
from app.services.email_service import send_password_reset_email
from app.models.email_verification_token_model import EmailVerificationToken
from app.services.email_service import send_email_verification_email



def change_password(db, current_user, password_data):
    if not verify_password(password_data.old_password,current_user.password):
        raise HTTPException(
            status_code=401,
            detail="Old password is incorrect"
        )
    current_user.password = hash_password(
        password_data.new_password
    )

    db.query(RefreshToken).filter(
        RefreshToken.user_id == current_user.id,
        RefreshToken.is_revoked == False
    ).update(
        {
            "is_revoked": True
        },
        synchronize_session=False
    )

    db.commit()

    return {
        "message": "Password changed successfully. Please login again."
    }



def login_user(db, form_data):
    user = db.query(User).filter(User.email == form_data.username,User.is_deleted == False,User.is_active == True).first()

    if user is None:
        raise HTTPException(status_code=401,detail="Invalid email or password")

    now = datetime.utcnow()
    if user.locked_until and user.locked_until > now:
        raise HTTPException(status_code=403,detail="Account is temporarily locked. Please try again later.")

    if user.locked_until and user.locked_until <= now:
        user.locked_until = None
        user.failed_login_attempts = 0
        db.commit()
        db.refresh(user)

    if not verify_password(form_data.password, user.password):
        user.failed_login_attempts += 1

        if user.failed_login_attempts >= int(MAX_FAILED_LOGIN_ATTEMPTS):
            user.locked_until = now + timedelta(minutes=int(ACCOUNT_LOCKOUT_MINUTES))
        db.commit()
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email before login"
        )

    user.failed_login_attempts = 0
    user.locked_until = None

    access_token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )

    refresh_token = create_refresh_token(
        data={
            "sub": str(user.id)
        }
    )

    refresh_token_record = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(
            days=int(REFRESH_TOKEN_EXPIRE_DAYS)
        )
    )

    db.add(refresh_token_record)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def refresh_access_token(db: Session, refresh_token: str):
    user_id = verify_refresh_token(refresh_token)
    if not user_id:
        logger.warning(f"Invalid refresh token")
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    token_record = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.is_revoked == False
    ).first()
    
    if token_record is None:
        raise HTTPException(
            status_code=401,
            detail="Refresh token revoked or not found"
        )

    if token_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=401,
            detail="Refresh token expired"
        )
    
    user = db.query(User).filter(User.id == token_record.user_id, User.is_deleted == False, User.is_active == True).first()
    if not user:
        logger.warning(f"User not found for refresh token: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    token_record.is_revoked = True
    new_access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
    new_refresh_token_record = RefreshToken(
        token=new_refresh_token,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(
            days=int(REFRESH_TOKEN_EXPIRE_DAYS)
        )
    )

    db.add(new_refresh_token_record)
    db.commit()

    logger.info(f"Access token refreshed for user: {user.id}")
    return {"access_token": new_access_token, "token_type": "bearer"}


def logout_user(db:Session,refresh_token:str):
    token_record = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.is_revoked == False
    ).first()
    
    if token_record is None:
        raise HTTPException(
            status_code=401,
            detail="Refresh token revoked or not found"
        )
    
    token_record.is_revoked = True
    db.commit()
    logger.info(f"User logged out, refresh token revoked: {token_record.user_id}")
    return {"message": "Logged out successfully"}

def logout_all_devices(db, current_user):
    active_tokens = db.query(RefreshToken).filter(
        RefreshToken.user_id == current_user.id,
        RefreshToken.is_revoked == False
    ).all()

    if not active_tokens:
        return {
            "message": "No active sessions found"
        }

    for token in active_tokens:
        token.is_revoked = True

    db.commit()

    return {
        "message": "Logged out from all devices successfully",
        "revoked_sessions": len(active_tokens)
    }

def get_active_sessions(db, current_user):
    sessions = db.query(RefreshToken).filter(
        RefreshToken.user_id == current_user.id,
        RefreshToken.is_revoked == False,
        RefreshToken.expires_at > datetime.utcnow()
    ).order_by(
        RefreshToken.created_at.desc()
    ).all()

    return {
        "total": len(sessions),
        "data": [
            {
                "id": session.id,
                "created_at": session.created_at,
                "expires_at": session.expires_at,
                "is_revoked": session.is_revoked
            }
            for session in sessions
        ]
    }


def revoke_session(db, current_user, session_id: int):
    session = db.query(RefreshToken).filter(
        RefreshToken.id == session_id,
        RefreshToken.user_id == current_user.id,
        RefreshToken.is_revoked == False
    ).first()

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Active session not found"
        )

    session.is_revoked = True

    db.commit()

    return {
        "message": "Session revoked successfully"
    }


def forgot_password(db, email: str):
    user = db.query(User).filter(
        User.email == email,
        User.is_deleted == False
    ).first()

    if user is None:
        return {
            "message": "If this email exists, a password reset link has been sent."
        }

    reset_token = secrets.token_urlsafe(32)

    reset_token_record = PasswordResetToken(
        token=reset_token,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(minutes=15)
    )

    db.add(reset_token_record)
    db.commit()

    try:
        send_password_reset_email(
            email=user.email,
            reset_token=reset_token
        )

    except Exception:
        return {
            "message": "Password reset token was created, but email could not be sent."
        }

    return {
        "message": "If this email exists, a password reset link has been sent."
    }


def reset_password(db, token: str, new_password: str):
    token_record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token,
        PasswordResetToken.is_used == False
    ).first()

    if token_record is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or already used reset token"
        )

    if token_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Reset token expired"
        )

    user = db.query(User).filter(
        User.id == token_record.user_id,
        User.is_deleted == False
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found or inactive"
        )

    user.password = hash_password(new_password)

    token_record.is_used = True

    db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id,
        RefreshToken.is_revoked == False
    ).update(
        {
            "is_revoked": True
        },
        synchronize_session=False
    )

    db.commit()

    return {
        "message": "Password reset successfully. Please login again."
    }


def verify_email(db, token: str):
    token_record = db.query(EmailVerificationToken).filter(
        EmailVerificationToken.token == token,
        EmailVerificationToken.is_used == False
    ).first()

    if token_record is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or already used verification token"
        )

    if token_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Verification token expired"
        )

    user = db.query(User).filter(
        User.id == token_record.user_id,
        User.is_deleted == False
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found or inactive"
        )

    user.is_verified = True
    user.verified_at = datetime.utcnow()
    token_record.is_used = True

    db.commit()

    return {
        "message": "Email verified successfully. You can now login."
    }


def resend_verification_email(db, email: str):
    user = db.query(User).filter(
        User.email == email,
        User.is_deleted == False
    ).first()

    if user is None:
        return {
            "message": "If this email exists, a verification link has been sent."
        }
    if user.is_verified:
        return {
            "message": "Email is already verified."
        }

    verification_token = secrets.token_urlsafe(32)

    token_record = EmailVerificationToken(
        token=verification_token,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )

    db.add(token_record)
    db.commit()

    try:
        print("Trying to send verification email to:", user.email)

        send_email_verification_email(
            email=user.email,
            verification_token=verification_token
        )
        print("Verification email sent successfully.")
    except Exception as error:
        print("EMAIL VERIFICATION SEND ERROR:", repr(error))
        return {
            "message": "Verification token was created, but email could not be sent."
        }

    return {
        "message": "If this email exists, a verification link has been sent."
    }