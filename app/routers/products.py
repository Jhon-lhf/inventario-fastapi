import os
from fastapi import APIRouter,Depends,HTTPException,status,File,UploadFile
from fastapi.responses import FileResponse
from uuid import uuid4
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate,ProductOut
from app.crud import product as crud_product
from app.core.dependencies import get_current_user
from app.models.user import User
from app.core.utils import validar_rol

router=APIRouter(prefix="/products",tags=["Products"])

@router.post("/",response_model=ProductOut)
async def create_product_route(
    product:ProductCreate,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    validar_rol(current_user,["admin","vendedor"])
    return crud_product.create_product(db,product,current_user.id)

@router.post("/{product_id}/upload-image")
async def upload_image(
    product_id:int,
    file:UploadFile=File(...),
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    product=crud_product.get_product(db,product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Producto no encontrado")
    
    if current_user.rol != "admin" and product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No autorizado")
    
    extension=file.filename.split(".")[-1]
    filename=f"{uuid4().hex}.{extension}"
    path=os.path.join("static/images",filename)
    
    with open(path,"wb") as buffer:
        buffer.write(file.file.read())
        
    product.image=filename
    db.commit()
    
    return {"filename":filename,"url":f"static/images/{filename}"}

@router.get("/",response_model=list[ProductOut])
async def list_products(db:Session=Depends(get_db)):
    return crud_product.get_products(db)

@router.get("/{product_id}",response_model=ProductOut)
async def get_product_by_id(product_id:int,db:Session=Depends(get_db)):
    product=crud_product.get_product(db,product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Producto no encontrado")
    return product

@router.delete("/{post_id}")
async def delete_product_route(product_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    deleted=crud_product.delete_product(db,product_id,current_user.id,is_admin=(current_user.rol=="admin"))
    if deleted is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No puedes eliminar este producto.")
    return {"detail":"Producto eliminado"}