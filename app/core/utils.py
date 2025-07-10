from fastapi import HTTPException,status
from app.models.user import User

def validar_rol(usuario:User,roles_permitidos:list):
    if usuario.rol not in roles_permitidos:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Acceso denegado. Rol requerido: {', '.join(roles_permitidos)}")