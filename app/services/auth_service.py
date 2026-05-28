from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from app.models.uer_models import  User    
from fastapi import HTTPException,status
from app.security  import create_access_token, verify_password,hash_password
from app.logger import logger



def change_user_password(password_data,current_user,db:Session):
    if not verify_password(password_data.old_password,current_user.password):
        logger.warning(f"Incorrect old password for user: {current_user.id}")
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    
    current_user.password = hash_password(password_data.new_password)
    db.commit()
    logger.info(f"User password changed: {current_user.id}")
    return {"message": "Password changed successfully"}



def login_user(db: Session,user_data):
    user = db.query(User).filter(User.email == user_data.username, User.is_deleted == False).first()
    if not user:
        logger.warning(f"User not found for login: {user_data.username}")
        raise HTTPException(status_code=404, detail="User not found")
    password_correct = verify_password(user_data.password,user.password)
    if not password_correct:
        logger.warning(f"Invalid email or password for user: {user_data.username}")
        raise HTTPException(status_code=400, detail= "Invalid email or password")
    access_token = create_access_token(data={"sub": str(user.id)})
    logger.info(f"User logged in: {user.id}")
    return {"access_token": access_token,"token_type": "bearer"}
