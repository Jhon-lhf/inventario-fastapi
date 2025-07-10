from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException,status
from app.schemas.sale import SaleCreate
from app.models.user import User
from app.models.product import Product
from app.models.sale_detail import SaleDetail
from app.models.sale import Sale

def crear_venta(venta:SaleCreate,db:Session,user:User):
    total=0
    detalles_creados=[]
    
    for item in venta.detalles:
        producto=db.query(Product).filter(Product.id==item.product_id).first()
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Producto {item.product_id} no existe")
        
        if producto.quantity < item.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Stock insuficiente para {producto.name}")
        
        producto.quantity -= item.quantity
        total += item.quantity * item.price
        
        detalle=SaleDetail(
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        detalles_creados.append(detalle)
        
    nueva_venta=Sale(
        user_id=user.id,
        total=total,
        detalles=detalles_creados
    )
    
    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)
    return nueva_venta

def obtener_ventas(db:Session,user:User):
    if user.rol=="vendedor":
        return db.query(Sale).filter(Sale.user_id==user.id).all()
    else:
        return db.query(Sale).options(joinedload(Sale.usuario)).all()