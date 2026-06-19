
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from app.models.email_verification_token_model import EmailVerificationToken
from app.models.uer_models import  User    
from app.models.refresh_token_model import RefreshToken
from fastapi import HTTPException,status
from app.security  import hash_password
import secrets
from datetime import datetime, timedelta
from app.logger import logger
from app.security import verify_password
from app.services.email_service import send_email_verification_email

def read_root():
    logger.info("Reading root endpoint")
    return {"message": "Backend is running successfully!"}


def about():
    logger.info("Reading about endpoint")
    return {"message":"king of the world"}

def create_email_verification_for_user(db, user):
    verification_token = secrets.token_urlsafe(32)

    token_record = EmailVerificationToken(
        token=verification_token,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )

    db.add(token_record)

    try:
        send_email_verification_email(
            email=user.email,
            verification_token=verification_token
        )
    except Exception:
        pass

def create_user(db, user_data):
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        age=user_data.age,
        password=hash_password(user_data.password),
        role="user",
        is_deleted=False,
        is_verified=False,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    verification_token = secrets.token_urlsafe(32)

    token_record = EmailVerificationToken(
        token=verification_token,
        user_id=new_user.id,
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )

    db.add(token_record)
    db.commit()

    try:
        send_email_verification_email(
            email=new_user.email,
            verification_token=verification_token
        )
    except Exception as e:
        logger.error(f"Failed to send verification email to {new_user.email}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to send verification email. Please try again later."
        )
    return new_user


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    logger.info(f"User retrieved: {user_id}")
    return user


def update_user_profile(update_data,current_user,db: Session):
    email_changed=False
    existing_email=db.query(User).filter(
        User.email == update_data.email,
        User.id != current_user.id,
        User.is_deleted == False
    ).first()
    if existing_email:
        logger.warning(f"Attempt to update profile with existing email: {update_data.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    current_user.name = update_data.name
    current_user.age = update_data.age
    current_user.email = update_data.email
    current_user.is_verified=False
    current_user.verified_at=None
    email_changed=True
    if email_changed:
        verification_token = secrets.token_urlsafe(32)

        token_record = EmailVerificationToken(
        token=verification_token,
        user_id=current_user.id,
        expires_at=datetime.utcnow() + timedelta(hours=24))

        db.add(token_record)

        try:
            send_email_verification_email(
            email=current_user.email,
            verification_token=verification_token
        )
        except Exception:
          pass
    
    db.commit()
    db.refresh(current_user)
    message = "Profile updated successfully"

    if email_changed:
        message = "Profile updated successfully. Please verify your new email before next login."

    logger.info(f"User profile updated: {current_user.id}")

    return current_user

def partial_update_user_profile(update_data, current_user, db: Session):
    email_changed = False

    if update_data.email is not None:
        new_email = update_data.email.lower()

        if new_email != current_user.email:
            existing_email = db.query(User).filter(
                User.email == new_email,
                User.id != current_user.id,
                User.is_deleted == False
            ).first()

            if existing_email:
                logger.warning(
                    f"Attempt to update profile with existing email: {new_email}"
                )
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )

            current_user.email = new_email
            current_user.is_verified = False
            current_user.verified_at = None
            email_changed = True

    if update_data.name is not None:
        current_user.name = update_data.name

    if update_data.age is not None:
        current_user.age = update_data.age

    try:
        if email_changed:
            create_email_verification_for_user(
                db,
                current_user
            )

        db.commit()
        db.refresh(current_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    except Exception as error:
        db.rollback()
        logger.error(f"Profile update failed: {repr(error)}")
        raise HTTPException(
            status_code=500,
            detail="Profile update failed"
        )

    message = "Profile updated successfully"

    if email_changed:
        message = "Profile updated successfully. Please verify your new email before next login."

    return current_user



def deactivate_account(db, current_user, password: str):
    if not verify_password(password, current_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    current_user.is_active = False
    current_user.deactivated_at = datetime.utcnow()

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
        "message": "Account deactivated successfully"
    }