from sqlalchemy import Column, Integer, String,DateTime,Boolean
from datetime import datetime
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False,unique=True)
    role = Column(String, default="user")
    phone_number=Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted=Column(Boolean,default=False)
    deleted_at=Column(DateTime, nullable=True)
    is_verified = Column(Boolean,default=False,server_default="false",nullable=False)
    verified_at = Column(DateTime, nullable=True)
    failed_login_attempts = Column(Integer,default=0,server_default="0",nullable=False)
    locked_until = Column(DateTime,nullable=True)
    is_active = Column(Boolean,default=True,server_default="true",nullable=False)
    deactivated_at = Column(DateTime,nullable=True)

