from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user
from app.crud import inventory as crud_inventory
from app.models.user import User
from app.schemas.inventory import MovementOut,MovementCreate
from app.core.utils import validar_rol

router=APIRouter(prefix="/inventory",tags=["Inventory"])

@router.post("/",response_model=MovementOut,status_code=status.HTTP_201_CREATED)
async def register_movement(movement:MovementCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    validar_rol(current_user,["admin","vendedor"])
    return crud_inventory.create_movement(db,movement,current_user.id)

@router.get("/",response_model=list[MovementOut])
async def list_movements(product_id:int=None,movement_type:str=None,start_date:str=None,end_date:str=None,user_id:int=None,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    validar_rol(current_user,["admin","vendedor"])
    return crud_inventory.get_movements(product_id,movement_type,start_date,end_date,user_id,db)