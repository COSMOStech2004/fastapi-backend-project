from sqlalchemy.orm import Session

from app.models.audit_log_model import AuditLog


def create_audit_log(
    db: Session,
    admin_id: int,
    action: str,
    target_user_id: int | None = None,
    details: str | None = None
):
    audit_log = AuditLog(
        admin_id=admin_id,
        target_user_id=target_user_id,
        action=action,
        details=details
    )

    db.add(audit_log)

    return audit_log