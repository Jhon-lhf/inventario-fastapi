from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate,UserOut
from app.crud import user as crud_user
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.core.utils import validar_rol
from typing import List

router=APIRouter(prefix="/users",tags=["Users"])

@router.post("/",response_model=UserOut,status_code=status.HTTP_201_CREATED)
async def register_user(user:UserCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    validar_rol(current_user,["admin"])
    return crud_user.create_user(db,user)

@router.get("/",response_model=List[UserOut])
async def list_users(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    validar_rol(current_user,["admin"])
    return  crud_user.get_users(db)

@router.put("/{user_id}/rol")
async def change_rol_user(user_id:int,new_rol:dict,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    validar_rol(current_user,["admin"])
    return crud_user.change_rol(user_id,new_rol,db)

@router.delete("/{user_id}")
async def delete_user(user_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    validar_rol(current_user,["admin"])
    if user_id==current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No puedes eliminar tu propio usuario")
    return crud_user.delete_user(user_id,db)

@router.put("/{user_id}/toggle-active")
async def toggle_user_active(user_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    validar_rol(current_user,["admin"])
    if user_id==current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No puedes desactivar tu propio usuario")
    return crud_user.active_user(user_id,db)