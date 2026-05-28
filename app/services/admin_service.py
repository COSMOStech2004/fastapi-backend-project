
from sqlalchemy.orm import Session
from app.models.audit_log_model import AuditLog
from app.models.uer_models import  User    
from fastapi import HTTPException
from app.logger import logger
from datetime import datetime
from app.services.audit_service import create_audit_log



def get_audit_logs(
    db: Session,
    limit: int = 10,
    offset: int = 0
):
    query = db.query(AuditLog).order_by(
        AuditLog.created_at.desc()
    )

    total_logs = query.count()

    logs = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total_logs,
        "limit": limit,
        "offset": offset,
        "data": logs
    }

def update_user_role(db: Session, user_id: int, role_data,admin_user:User):
    user = db.query(User).filter(
        User.id == user_id,User.is_deleted==False
    ).first()

    if not user:
        logger.warning(f"User not found for role update: {user_id} by admin: {admin_user.id}")
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if role_data.role not in ["user", "admin"]:
        logger.warning(f"Invalid role update attempt for user: {user_id} with role: {role_data.role} by admin: {admin_user.id}")
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )
    old_role=user.role
    user.role = role_data.role
    create_audit_log(
        db=db,
        admin_id=admin_user.id,
        target_user_id=user.id,
        action="update_role",
        details=f"Role updated from {old_role} to {role_data.role}"
    )

    
    db.commit()
    db.refresh(user)
    logger.info(f"User role updated: {user.id} by admin: {admin_user.id}")
    return user



def delete_user(db: Session, user_id: int, admin_user: User):
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    logger.info(f"Attempting to delete user: {user_id}")
    if not user:
        logger.warning(f"User not found for deletion: {user_id} by admin: {admin_user.id}")
        raise HTTPException(status_code=404, detail="User not found")
    user.is_deleted = True
    user.deleted_at = datetime.utcnow()
    create_audit_log(
        db=db,
        admin_id=admin_user.id,
        target_user_id=user.id,
        action="soft_delete",
        details="User soft deleted"
    )
    db.commit()
    logger.info(f"User deleted: {user_id} by admin: {admin_user.id}")
    return {"message": "User deleted successfully"}

def permanently_delete_user(db: Session, user_id: int, admin_user: User):
    user = db.query(User).filter(
        User.id == user_id,
        User.is_deleted == True
    ).first()
    if not user:
        logger.warning(
            f"Permanent delete failed: deleted user not found - user_id={user_id} by admin: {admin_user.id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Deleted user not found"
        )
    
    create_audit_log(
        db=db,
        admin_id=admin_user.id,
        target_user_id=user.id,
        action="soft_delete",
        details="User soft deleted"
    )
    db.delete(user)
    db.commit()
    logger.info(
        f"User permanently deleted: user_id={user_id} by admin: {admin_user.id}"
    )

    return {
        "message": "User permanently deleted successfully"
    }


def restore_user(db: Session, user_id: int, admin_user: User):
    user = db.query(User).filter( User.id == user_id, User.is_deleted == True ).first()
    if not user:
        logger.warning( f"User restore failed: deleted user not found - user_id={user_id} by admin: {admin_user.id}")
        raise HTTPException(status_code=404,detail="Deleted user not found")
    user.is_deleted = False
    user.deleted_at = None
    create_audit_log(
        db=db,
        admin_id=admin_user.id,
        target_user_id=user.id,
        action="soft_delete",
        details="User soft deleted"
    )
    db.commit()
    db.refresh(user)
    logger.info( f"User restored successfully: user_id={user_id} by admin: {admin_user.id}")
    return user

def get_deleted_users(db: Session,limit: int = 10, offset: int = 0):
    query = db.query(User).filter(User.is_deleted == True)
    total_users = query.count()
    users = (query.offset(offset).limit(limit).all())
    logger.info(f"Getting deleted users: total={total_users}")
    return {
        "total": total_users,
        "limit": limit,
        "offset": offset,
        "data": users
       }


def get_all_users(
    db: Session,
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
    role: str | None = None,
    sort_by: str = "created_at",
    sort_order: str="desc"
):
    query = db.query(User).filter(User.is_deleted==False)

    if search:
        search_pattern = f"%{search}%"

        query = query.filter(
            (User.name.ilike(search_pattern))|
            (User.email.ilike(search_pattern))
        )

    if role:
        query = query.filter(
            User.role == role
        )


    allowed_sort_fields = {
        "id": User.id,
        "name": User.name,
        "email": User.email,
        "age": User.age,
        "role": User.role,
        "created_at": User.created_at,
        "updated_at": User.updated_at
    }

    sort_column = allowed_sort_fields.get(sort_by, User.created_at)

    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    
    total_users = query.count()

    users = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total_users,
        "limit": limit,
        "offset": offset,
        "data": users
    }