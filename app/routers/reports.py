from fastapi import APIRouter,status,Depends,HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import StringIO,BytesIO
import csv
import pandas as pd
from app.database import get_db
from app.core.dependencies import get_current_user
from app.core.utils import validar_rol
from app.crud.report import fetch_query
from app.models.user import User

router=APIRouter(prefix="/reports",tags=["Reports"])

@router.get("/{resource}/csv")
async def export_csv(resource:str,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    validar_rol(current_user,["admin","vendedor"])
    
    items=fetch_query(resource,db,current_user)
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No hay datos para exportar")
    
    #Convertir a CSV
    sio=StringIO()
    writer=csv.writer(sio)
    
    #Cabeceras segun recurso
    if resource=="products":
        writer.writerow(["id","name","description","price","quantity","owner_id"])
        for p in items:
            writer.writerow([p.id,p.name,p.description,p.price,p.quantity,p.owner_id])
        filename="products.csv"
    elif resource=="inventory":
        writer.writerow(["id","product_id","quantity","type","created_at","user_id"])
        for m in items:
            writer.writerow([m.id,m.product_id,m.quantity,m.movement_type,m.created_at,m.user_id])
        filename="inventory.csv"
    else: #sales
        writer.writerow(["id","user_id","total","created_at"])
        for s in items:
            writer.writerow([s.id,s.user_id,s.total,s.created_at])
        filename="sales.csv"
    
    sio.seek(0)
    return StreamingResponse(
        sio,media_type="text/csv",
        headers={"Content-Disposition":f"attachment; filename={filename}"}
    )
    
@router.get("/{resource}/excel")
async def export_excel(resource:str,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    validar_rol(current_user,["admin","vendedor"])
    
    items=fetch_query(resource,db,current_user)
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No hay datos para exportar")
    
    #Convertir a DataFrame
    if resource=="products":
        data=[{
            "ID":p.id,
            "Nombre":p.name,
            "Descripcion":p.description,
            "Precio":p.price,
            "Cantidad":p.quantity,
            "Owner ID":p.owner_id
        }for p in items]
        filename="products.xlsx"
    elif resource=="inventory":
        data=[{
            "ID":m.id,
            "Product ID":m.product_id,
            "Cantidad":m.quantity,
            "Tipo":m.movement_type,
            "Fecha":m.created_at,
            "User ID":m.user_id
        }for m in items]
        filename="inventory.xlsx"
    else: #sales
        data=[{
            "ID":s.id,
            "User ID":s.user_id,
            "Total":s.total,
            "Fecha":s.created_at
        }for s in items]
        filename="sales.xlsx"
    
    df=pd.DataFrame(data)
    bio=BytesIO()
    with pd.ExcelWriter(bio,engine="openpyxl") as writer:
        df.to_excel(writer,index=False,sheet_name=resource.capitalize())
    bio.seek(0)
    
    return StreamingResponse(
        bio,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition":f"attachment; filename={filename}"}
    )