from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr
from core.config import settings

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data:dict, expires_delta: Optional[timedelta] = None):
    encoded = data.copy()
    if expires_delta:
        expire = datetime.utcnow() +expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded.update({"exp": expire})
    encoded_jwt = jwt.encode(encoded, settings.SECRET_KEY)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    encoded = data.copy()
    if expires_delta:
        expire = datetime.utcnow() +expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded.update({"exp": expire})
    encoded_jwt = jwt.encode(encoded, settings.SECRET_KEY)
    return encoded_jwt

def decode_token(token:str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: EmailStr = payload.get("sub")
        if email is None:
            raise JWTError()
        return  TokenData(email = email)
    except JWTError:
        return None
    
def create_reset_password_token(email: str):
    expire = datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_reset_password_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except jwt.JWTError:
        return None
