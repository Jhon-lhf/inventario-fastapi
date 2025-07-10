from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext
from fastapi import HTTPException,status

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(db:Session,user:UserCreate):
    hashed_pw=get_password_hash(user.password)
    query=db.query(User).filter(User.email==user.email).first()
    if query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="El usuario ya existe")
    
    db_user=User(username=user.username,email=user.email,password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db:Session):
    users=db.query(User).all()
    return users

def get_user(user_id:int,db:Session):
    user=db.query(User).filter(User.id==user_id).first()
    if not user:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Usuario no encontrado")
    return user

def change_rol(user_id:int,new_rol:dict,db:Session):
    user=get_user(user_id,db)
    user.rol=new_rol.get("rol",user.rol)
    db.commit()
    return {"message":"Rol actualizado"}

def delete_user(user_id:int,db:Session):
    user=get_user(user_id,db)
    db.delete(user)

def active_user(user_id:int,db:Session):    
    user=get_user(user_id,db)
    user.is_active=not user.is_active
    db.commit()
    return {"message":"Estado actualizado","is_active":user.is_active}