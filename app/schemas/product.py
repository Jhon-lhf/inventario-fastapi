from pydantic import BaseModel

class ProductBase(BaseModel):
    name:str
    description:str
    price:float
    quantity:int

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id:int
    owner_id:int
    image: str | None = None #Url completa
    
    class Config:
        from_attributes=True