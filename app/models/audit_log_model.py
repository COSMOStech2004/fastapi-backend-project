from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.models.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    admin_id = Column(Integer, nullable=False)

    target_user_id = Column(Integer, nullable=True)

    action = Column(String, nullable=False)

    details = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)