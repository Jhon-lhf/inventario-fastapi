from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models.user import User
from app.schemas.token import Token
from app.core.security import verify_password,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router=APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/login",response_model=Token)
async def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(User).filter(User.username==form_data.username).first()
    if not user or not verify_password(form_data.password,user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Usuario o contraseña incorrectos",headers={"WWW-Authenticate":"Bearer"},)
    
    if user.is_active==False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Usuario desactivado")
    
    access_token=create_access_token(data={"sub":user.username,"role":user.rol},expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),)
    return {"access_token":access_token,"token_type":"bearer"}