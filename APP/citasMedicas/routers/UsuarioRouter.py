from fastapi import APIRouter, HTTPException
from typing import List

from app.dao.users import UsersDAO
from app.models.usuario import Usuario, UsuarioCreate, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("", response_model=Usuario, status_code=201)
async def crear_usuario(data: UsuarioCreate):
    dao = UsersDAO()
    try:
        return await dao.create(data.dict())
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/{uid}", response_model=Usuario)
async def obtener_usuario(uid: str):
    dao = UsersDAO()
    user = await dao.get(uid)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{uid}", response_model=Usuario)
async def actualizar_usuario(uid: str, data: UsuarioUpdate):
    dao = UsersDAO()
    return await dao.update(uid, data.dict(exclude_unset=True))

@router.delete("/{uid}", status_code=204)
async def eliminar_usuario(uid: str):
    dao = UsersDAO()
    if not await dao.delete(uid):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.get("", response_model=List[Usuario])
async def listar_usuarios():
    dao = UsersDAO()
    return await dao.list()
