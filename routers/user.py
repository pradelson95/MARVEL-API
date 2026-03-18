from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from models.user import User
from schemas.user_schema import UserCreate
from security.auth_handler import hash_password, get_current_admin

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):

    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()

    return {
        "message": f"User {new_user.username} created by admin {admin['username']}"
    }