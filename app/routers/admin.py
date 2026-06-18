from fastapi import APIRouter, Depends, Query
from typing import Literal
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth_dependencies import get_current_admin_user
from app.models.uer_models import User
from app.shemas.user_schema import (
PaginatedUserResponse,UserResponse)
from app.shemas.admin_schema import RoleUpdate as userRoleUpdate
from app.shemas.auditlog_schema import (PaginatedAuditLogResponse)
from app.services.admin_service import (
    delete_user,
    permanently_delete_user,
    update_user_role,
    get_all_users,
    restore_user,
    get_deleted_users,
    get_audit_logs,
    reactivate_user
)

router = APIRouter()

@router.get("/audit-logs", response_model=PaginatedAuditLogResponse)
def admin_get_audit_logs(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)
):
    return get_audit_logs(db, limit, offset)

@router.get("/users", response_model=PaginatedUserResponse)
def admin_get_all_users(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    search: str | None = Query(default=None),
    role: Literal["user", "admin"] | None = Query(default=None),
    sort_by: Literal["id","name","email","age","role","created_at","updated_at"] = Query(default="created_at"),
    sort_order: Literal["asc", "desc"] = Query(default="desc"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)
):
    return get_all_users(
        db,
        limit,
        offset,
        search,
        role,
        sort_by,
        sort_order
    )

@router.get("/users/deleted", response_model=PaginatedUserResponse)
def admin_get_deleted_users(limit: int = Query(default=10, ge=1, le=100),offset: int = Query(default=0, ge=0),db: Session = Depends(get_db),_: User = Depends(get_current_admin_user)):
    return get_deleted_users(db, limit, offset)

@router.delete("/users/{user_id}/permanent")
def admin_permanently_delete_user(user_id: int,db: Session = Depends(get_db),user: User = Depends(get_current_admin_user)):
    return permanently_delete_user(db, user_id, user)


@router.delete("/users/{user_id}",)
def remove_user(user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_admin_user)):
    return delete_user(db, user_id,user)

@router.patch("/users/{user_id}/restore", response_model=UserResponse)
def admin_restore_user(user_id: int,db: Session = Depends(get_db),user: User = Depends(get_current_admin_user)):
    return restore_user(db, user_id,user)


@router.patch("/admin/users/{user_id}/role", response_model=UserResponse)
def change_user_role(user_id: int,role_data: userRoleUpdate,db: Session = Depends(get_db),user: User = Depends(get_current_admin_user)):
    return update_user_role(db, user_id, role_data,user)

@router.patch("/users/{user_id}/reactivate")
def reactivate_user_account(user_id: int,db: Session = Depends(get_db),admin_user: User = Depends(get_current_admin_user)):
    return reactivate_user(db,user_id,admin_user)