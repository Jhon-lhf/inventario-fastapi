from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional
from .user import UserOut

class SaleDetailBase(BaseModel):
    product_id:int
    quantity:int
    price:float

class SaleCreate(BaseModel):
    detalles:List[SaleDetailBase]

class SaleDetail(SaleDetailBase):
    id:int
    
    class Config:
        from_attributes=True
    
class Sale(BaseModel):
    id:int
    user_id:int
    total:float
    created_at:datetime
    detalles:List[SaleDetail]
    usuario:Optional[UserOut]
    
    class Config:
        from_attributes=True