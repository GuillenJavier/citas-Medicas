from fastapi import APIRouter, Request, HTTPException, Depends
from models.notificacion_model import Notificacion
from dao import notificacion_dao
from security.security import get_current_user

router = APIRouter(prefix="/api/notificaciones", tags=["Notificaciones"])

@router.post("/", summary="Crear notificación", dependencies=[Depends(get_current_user(["Administrador", "Médico"]))])
async def crear_notificacion(request: Request, datos: Notificacion):
    nueva_id = await notificacion_dao.crear_notificacion(request.app.db, datos.dict())
    return {"mensaje": "Notificación creada", "id": nueva_id}

@router.get("/usuario/{usuario_id}", summary="Listar notificaciones", dependencies=[Depends(get_current_user(["Administrador", "Paciente", "Médico"]))])
async def listar_notis(request: Request, usuario_id: str):
    return await notificacion_dao.listar_notificaciones(request.app.db, usuario_id)

@router.put("/{noti_id}", summary="Marcar como leída", dependencies=[Depends(get_current_user(["Paciente", "Administrador"]))])
async def marcar_leida(request: Request, noti_id: str):
    actualizado = await notificacion_dao.marcar_como_leida(request.app.db, noti_id)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return {"mensaje": "Notificación marcada como leída"}

@router.delete("/{noti_id}", summary="Eliminar notificación", dependencies=[Depends(get_current_user(["Administrador"]))])
async def eliminar_noti(request: Request, noti_id: str):
    eliminado = await notificacion_dao.eliminar_notificacion(request.app.db, noti_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return {"mensaje": "Notificación eliminada"}
