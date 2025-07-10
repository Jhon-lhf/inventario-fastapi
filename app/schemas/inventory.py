from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional
from .product import ProductBase
from .user import UserOut

class MovementType(str,Enum):
    entrada="entrada"
    salida="salida"

class MovementCreate(BaseModel):
    product_id:int
    quantity:int
    movement_type:MovementType

class MovementOut(MovementCreate):
    id:int
    created_at:datetime
    user_id:int 
    
    producto:Optional[ProductBase]
    usuario:Optional[UserOut]
    
    class Config:
        from_attributes=True