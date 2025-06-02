from fastapi import APIRouter, Request, HTTPException
from models.usuario_schema import Usuario, LoginUsuario
from dao.usuarios_dao import (
    insertar_usuario,
    verificar_credenciales,
    obtener_usuario_por_id,
    actualizar_usuario,
    eliminar_usuario
)
from security.security import crear_token

router = APIRouter()


@router.post("/", summary="Registrar usuario")
async def crear_usuario(request: Request, usuario: Usuario):
    resultado = await insertar_usuario(request.app.db, usuario.dict())
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return {"mensaje": "Usuario creado", "id": resultado["id"]}


@router.post("/login", summary="Iniciar sesión")
async def login(request: Request, credenciales: LoginUsuario):
    resultado = await verificar_credenciales(
        request.app.db,
        credenciales.correo,
        credenciales.contraseña
    )
    if "error" in resultado:
        raise HTTPException(status_code=401, detail=resultado["error"])

    usuario = resultado
    token = crear_token({
        "sub": str(usuario["_id"]),
        "correo": usuario["correo"],
        "rol": usuario["tipo"]
    })
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": str(usuario["_id"]),
            "nombre": usuario["nombre"],
            "correo": usuario["correo"],
            "tipo": usuario["tipo"]
        }
    }


@router.get("/{usuario_id}", summary="Obtener usuario por ID")
async def obtener_usuario(request: Request, usuario_id: str):
    usuario = await obtener_usuario_por_id(request.app.db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/{usuario_id}", summary="Actualizar usuario")
async def actualizar_usuario_endpoint(request: Request, usuario_id: str, datos: Usuario):
    resultado = await actualizar_usuario(request.app.db, usuario_id, datos.dict())
    if resultado == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario actualizado correctamente"}


@router.delete("/{usuario_id}", summary="Eliminar usuario")
async def eliminar_usuario_endpoint(request: Request, usuario_id: str):
    resultado = await eliminar_usuario(request.app.db, usuario_id)
    if resultado == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado correctamente"}
