from sqlalchemy import Column,Integer,Float,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Sale(Base):
    __tablename__="sales"
    
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    total=Column(Float)
    created_at=Column(DateTime,default=datetime.utcnow)
    
    detalles=relationship("SaleDetail",back_populates="venta")
    usuario=relationship("User")