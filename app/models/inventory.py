from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class MovementType(str,enum.Enum):
    entrada="entrada"
    salida="salida"
    
class InventoryMovement(Base):
    __tablename__="inventory_movements"
    
    id=Column(Integer,primary_key=True,index=True)
    product_id=Column(Integer,ForeignKey("products.id"))
    quantity=Column(Integer)
    movement_type=Column(Enum(MovementType))
    created_at=Column(DateTime,default=datetime.utcnow)
    user_id=Column(Integer,ForeignKey("users.id"))
    
    producto=relationship("Product",backref="movements")
    usuario=relationship("User",backref="movements")