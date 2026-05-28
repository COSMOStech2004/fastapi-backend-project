from dataclasses import field
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class AuditLogResponse(BaseModel):
    id: int
    admin_id: int
    target_user_id: int | None
    action: str
    details: str | None
    created_at: Optional[datetime]=None

    class Config:
        from_attributes = True

class PaginatedAuditLogResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: list[AuditLogResponse]