from fastapi import APIRouter
from models.usuario_schema import Usuario
from dao.usuarios_dao import insertar_usuario

router = APIRouter()

@router.post("/")
async def crear_usuario(usuario: Usuario):
    usuario_id = await insertar_usuario(usuario.dict())
    return {"mensaje": "Usuario creado", "id": usuario_id}
