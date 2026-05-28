
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from app.models.uer_models import  User    
from fastapi import HTTPException,status
from app.security  import hash_password
from app.logger import logger

def read_root():
    logger.info("Reading root endpoint")
    return {"message": "Backend is running successfully!"}


def about():
    logger.info("Reading about endpoint")
    return {"message":"king of the world"}

def create_user(db: Session, user_data):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        logger.warning(f"Attempt to create user with existing email: {user_data.email}")
        raise HTTPException(
            status_code=400,
            detail="Email already registered")

    hashed_password = hash_password(
        user_data.password
    )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        age=user_data.age,
        password=hashed_password,
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User created: {new_user.id}")
    return new_user

def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    logger.info(f"User retrieved: {user_id}")
    return user


def update_user_profile(update_data,current_user,db: Session):
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
    
    db.commit()
    db.refresh(current_user)
    logger.info(f"User profile updated: {current_user.id}")
    return current_user 

def partial_update_user_profile(update_data,current_user,db: Session):
    if update_data.email is not None:
        existing_email=db.query(User).filter(
            User.email == update_data.email,
            User.id != current_user.id,
            User.is_deleted == False
        ).first()
        if existing_email:
            logger.warning(f"Attempt to update profile with existing email: {update_data.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        current_user.email = update_data.email
    
    if update_data.name is not None:
        current_user.name = update_data.name
    
    if update_data.age is not None:
        current_user.age = update_data.age

        
    try:
        db.commit()
        db.refresh(current_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered")
    return current_user

