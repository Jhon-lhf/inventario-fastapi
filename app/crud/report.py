from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app import models

def fetch_query(resource:str,db:Session,user:models.User):
    if resource=="products":
        query=db.query(models.Product)
    elif resource=="inventory":
        query=db.query(models.InventoryMovement)
    elif resource=="sales":
        if user.rol=="cliente":
            query=db.query(models.Sale).filter(models.Sale.user_id==user.id)
        else:
            query=db.query(models.Sale)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Recurso desconocido")
    return query.all()


    