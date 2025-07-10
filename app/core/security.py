from datetime import datetime,timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext

#Config
SECRET_KEY="mi_clave_super_secreta"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

#Encriptacion
pw_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def verify_password(plain_password,hashed_password):
    return pw_context.verify(plain_password,hashed_password)

def create_access_token(data:dict,expires_delta:timedelta=None):
    to_encode=data.copy()
    expire=datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def get_password_hash(password):
    return pw_context.hash(password)