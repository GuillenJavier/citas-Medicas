
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "clave-super-secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/usuarios/login")

def crear_token(datos: dict, expires_delta: timedelta = None):
    to_encode = datos.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(roles_permitidos: list[str] = None):
    async def _wrapper(token: str = Depends(oauth2_scheme)):
        payload = verificar_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        if roles_permitidos and payload.get("rol") not in roles_permitidos:
            raise HTTPException(status_code=403, detail="Acceso denegado")
        return payload
    return _wrapper
