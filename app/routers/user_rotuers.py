from fastapi import APIRouter,Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.shemas.user_schema import (
UserCreate ,UserResponse,UpdateUser,PartialUpdateUser,DeactivateAccountRequest
)
from app.dependencies.auth_dependencies import (get_current_user)

from app.models.uer_models import User

from app.services.user_service import (
    get_user,
    partial_update_user_profile,
    update_user_profile,
    create_user,
    deactivate_account
)


router = APIRouter()


@router.post("/users", response_model=UserResponse)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/users/{user_id}", response_model=UserResponse)
def fetch_user(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)
    
@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "age": current_user.age
    }

@router.put("/profile", response_model=UserResponse)
def update_profile(update_data: UpdateUser, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_user_profile(update_data, current_user, db)

@router.patch("/profile", response_model=UserResponse)
def partial_update_profile(update_data: PartialUpdateUser, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return partial_update_user_profile(update_data, current_user, db)

@router.patch("/deactivate")
def deactivate_my_account(account_data: DeactivateAccountRequest,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return deactivate_account(db,current_user,account_data.password)

