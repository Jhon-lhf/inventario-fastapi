from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.product import Product
from app.models.inventory import InventoryMovement
from app.core.utils import validar_rol

router=APIRouter(prefix="/dashboard",tags=["Dashboard"])

@router.get("/")
async def get_dashboard(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    validar_rol(current_user,["admin","vendedor"])
    
    total_productos=db.query(func.count(Product.id)).scalar()
    stock_total=db.query(func.sum(Product.quantity)).scalar() or 0
    
    productos_bajo_stock=db.query(Product).filter(Product.quantity < 10).all()
    
    total_entradas=db.query(func.count(InventoryMovement.id)).filter(InventoryMovement.movement_type=="entrada").scalar()
    
    total_salidas=db.query(func.count(InventoryMovement.id)).filter(InventoryMovement.movement_type=="salida").scalar()
    
    ultimos_movimientos=db.query(InventoryMovement).order_by(InventoryMovement.created_at.desc()).limit(5).all()
    
    return {
        "resumen":{
            "total_productos":total_productos,
            "stock_total":stock_total,
            "total_entradas":total_entradas,
            "total_salidas":total_salidas
        },
        "bajo_stock":[
            {"id":p.id, "nombre":p.name,"cantidad":p.quantity}
            for p in productos_bajo_stock
        ],
        "ultimos_movimientos":[
            {
                "id":m.id,
                "producto_id":m.product_id,
                "cantidad":m.quantity,
                "tipo":m.movement_type,
                "fecha":m.created_at.isoformat()
            }for m in ultimos_movimientos
        ]
    }