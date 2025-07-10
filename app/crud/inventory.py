from sqlalchemy.orm import Session
from app.models.inventory import InventoryMovement
from app.models.product import Product
from app.schemas.inventory import MovementCreate
from fastapi import HTTPException,status
from datetime import datetime

def create_movement(db:Session,movement:MovementCreate,user_id:int):
    product=db.query(Product).filter(Product.id==movement.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Producto no encontrado")
    
    if movement.movement_type=="salida" and product.quantity < movement.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Stock insuficiente para la salida")
    
    if movement.movement_type=="entrada":
        product.quantity += movement.quantity
    else:
        product.quantity -= movement.quantity
    
    db_movement=InventoryMovement(
        product_id=movement.product_id,
        quantity=movement.quantity,
        movement_type=movement.movement_type,
        user_id=user_id
    )
    
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement


def get_movements(product_id:int=None,movement_type:str=None,start_date:str=None,end_date:str=None,user_id:int=None,db:Session=None):
    query=db.query(InventoryMovement)
    if product_id:
        query=query.filter(InventoryMovement.product_id==product_id)
    
    if movement_type in ["entrada","salida"]:
        query=query.filter(InventoryMovement.movement_type==movement_type)
    
    if user_id:
        query=query.filter(InventoryMovement.user_id==user_id)
        if query is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No hay movimientos asociados para este usuario")
    
    if start_date:
        try:
            start=datetime.fromisoformat(start_date)
            query=query.filter(InventoryMovement.created_at >= start)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="start_date invalida")
    
    if end_date:
        try:
            end=datetime.fromisoformat(end_date)
            query=query.filter(InventoryMovement.created_at <= end_date)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="end_date invalida")
    
    return query.order_by(InventoryMovement.created_at.desc()).all()