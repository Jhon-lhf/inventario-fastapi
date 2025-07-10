from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__="products"
    
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,index=True)
    description=Column(String)
    price=Column(Float)
    quantity=Column(Integer)
    image=Column(String,nullable=True)
    
    owner_id=Column(Integer,ForeignKey("users.id"))
    owner=relationship("User",back_populates="products")