from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status
from app.models.user import User
from app.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.sale import Sale,SaleCreate
from app.crud import sale as crud_sale
from typing import List
from app.core.utils import validar_rol

router=APIRouter(prefix="/sales",tags=["Sales"])

@router.post("/",response_model=Sale)
async def registrar_venta(venta:SaleCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    validar_rol(current_user,["admin","vendedor"])
    
    return crud_sale.crear_venta(venta,db,current_user)

@router.get("/",response_model=List[Sale])
async def listar_ventas(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return crud_sale.obtener_ventas(db,current_user)