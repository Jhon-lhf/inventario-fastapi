from pydantic import BaseModel, EmailStr
from enum import Enum

class RoleEnum(str,Enum):
    admin="admin"
    vendedor="vendedor"
    cliente="cliente"

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    username:str
    email:EmailStr
    rol:RoleEnum
    is_active:bool
    
    class Config:
        from_attributes=True
    
    