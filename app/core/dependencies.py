from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from app.database import get_db
from app.models.user import User
from app.core.security import SECRET_KEY,ALGORITHM

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token invalido",headers={"WWW-Authenticate":"Bearer"},)
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username:str=payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user=db.query(User).filter(User.username==username).first()
    if user is None:
        raise credentials_exception
    return user

