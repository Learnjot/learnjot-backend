from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Optional, List
from datetime import datetime
from db.dependency import PyObjectId

# Model to accept the user during the registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    date_of_birth: datetime
    
# Model to represent the user in the database
class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default = None)
    email: EmailStr
    hashed_password: str
    first_name: str
    middle_name: Optional[str] =  None
    last_name: str
    date_of_birth: datetime
    is_active: bool = True
    is_superuser: bool = False
    is_subscribed: bool = True
    created_at: datetime
    updated_at: datetime