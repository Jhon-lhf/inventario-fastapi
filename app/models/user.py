from sqlalchemy import Column,Integer,String,Enum,Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class RoleEnum(str,enum.Enum):
    admin="admin"
    vendedor="vendedor"
    cliente="cliente"
    
class User(Base):
    __tablename__="users"
    
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True)
    email=Column(String,unique=True,index=True)
    password=Column(String)
    rol=Column(Enum(RoleEnum), default="cliente")
    is_active=Column(Boolean,default=True,nullable=False)
    
    products=relationship("Product",back_populates="owner")