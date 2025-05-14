from fastapi import APIRouter, HTTPException
from typing import List

from app.dao.notificaciones import NotificacionesDAO
from app.models.notificacion import Notificacion, NotificacionCreate, NotificacionUpdate

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])

@router.post("", response_model=Notificacion, status_code=201)
async def crear_notificacion(data: NotificacionCreate):
    return await NotificacionesDAO().create(data.dict())

@router.get("/{nid}", response_model=Notificacion)
async def obtener_notificacion(nid: str):
    n = await NotificacionesDAO().get(nid)
    if not n:
        raise HTTPException(status_code=404, detail="No encontrada")
    return n

@router.put("/{nid}", response_model=Notificacion)
async def actualizar_notificacion(nid: str, data: NotificacionUpdate):
    return await NotificacionesDAO().update(nid, data.dict(exclude_unset=True))

@router.delete("/{nid}", status_code=204)
async def eliminar_notificacion(nid: str):
    if not await NotificacionesDAO().delete(nid):
        raise HTTPException(status_code=404, detail="No encontrada")

@router.get("", response_model=List[Notificacion])
async def listar_notificaciones():
    return await NotificacionesDAO().list()
