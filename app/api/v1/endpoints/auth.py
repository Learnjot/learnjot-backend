from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from core.security import (get_password_hash,
                           verify_password,
                           create_access_token,
                           create_refresh_token,
                           decode_token,
                           create_reset_password_token,
                           verify_reset_password_token)

from db.repositories.user import UserRepository
from db.dependency import get_database
from db.models.user import User, UserCreate
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "api/v1/auth/token")

class LoginRequest(BaseModel):
    username: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    

class PasswordResetRequest(BaseModel):
    email: EmailStr
    
class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
    
@router.post("/register")
async def register_user(user_create: UserCreate, db = Depends(get_database)):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(user_create.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user_create.password)
    user_data = user_create.model_dump()
    user_data.pop("password")
    user_in_db = User(**user_data, hashed_password=hashed_password, created_at = datetime.utcnow(), updated_at=datetime.utcnow())
    
    await user_repo.create_user(user_in_db)
    return {"msg": "User registered successfully"}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_database)):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        return HTTPException(status_code=400, detail = "Incorrect username or password")
    access_token = create_access_token(data = {"sub": user["email"]})
    refresh_token = create_refresh_token(data = {"sub": user["email"]})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_database)):
    token_data = decode_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail= "Invalid Token")
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(token_data.email)
    if not user:
        return HTTPException(status_code=401, detail = "User not Found")