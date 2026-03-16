from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET = "supersecretkey"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):

    return pwd_context.hash(password)


def verify_password(password, hashed):

    return pwd_context.verify(password, hashed)


def create_token(username: str, role: str):

    payload = {
        "username": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    return jwt.encode(payload, SECRET, algorithm="HS256")