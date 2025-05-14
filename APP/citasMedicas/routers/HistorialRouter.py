from fastapi import APIRouter, HTTPException
from typing import List

from app.dao.historial import HistorialDAO
from app.models.historial import Historial, HistorialCreate, HistorialUpdate

router = APIRouter(prefix="/historial", tags=["Historial Médico"])

@router.post("", response_model=Historial, status_code=201)
async def crear_historial(data: HistorialCreate):
    return await HistorialDAO().create(data.dict())

@router.get("/{hid}", response_model=Historial)
async def obtener_historial(hid: str):
    h = await HistorialDAO().get(hid)
    if not h:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return h

@router.put("/{hid}", response_model=Historial)
async def actualizar_historial(hid: str, data: HistorialUpdate):
    return await HistorialDAO().update(hid, data.dict(exclude_unset=True))

@router.delete("/{hid}", status_code=204)
async def eliminar_historial(hid: str):
    if not await HistorialDAO().delete(hid):
        raise HTTPException(status_code=404, detail="Registro no encontrado")

@router.get("", response_model=List[Historial])
async def listar_historial():
    return await HistorialDAO().list()
