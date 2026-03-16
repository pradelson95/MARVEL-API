from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from models.user import User
from schemas.user_schema import UserCreate, UserLogin
from security.auth_handler import hash_password, verify_password, create_token
from app.core.limiter import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])


# ============================
# REGISTER
# ============================

@router.post("/register")
@limiter.limit("2/minute")
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):

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

    return {"message": f"User {new_user.username} created"}


# ============================
# LOGIN
# ============================

@router.post("/login")
@limiter.limit("3/minute")
def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(db_user.username, db_user.role)

    return {
        "access_token": token,
        "token_type": "bearer"
    }