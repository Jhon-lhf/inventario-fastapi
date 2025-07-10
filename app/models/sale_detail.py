from sqlalchemy import Column,Integer,Float,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class SaleDetail(Base):
    __tablename__="sale_details"
    
    id=Column(Integer,primary_key=True,index=True)
    sale_id=Column(Integer,ForeignKey("sales.id"))
    product_id=Column(Integer,ForeignKey("products.id"))
    quantity=Column(Integer)
    price=Column(Float) #precio por unidad
    
    venta=relationship("Sale",back_populates="detalles")
    producto=relationship("Product")