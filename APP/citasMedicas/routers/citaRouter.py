from fastapi import APIRouter, HTTPException
from typing import List

from app.dao.citas import CitasDAO
from app.models.cita import Cita, CitaCreate, CitaUpdate

router = APIRouter(prefix="/citas", tags=["Citas"])

@router.post("", response_model=Cita, status_code=201)
async def crear_cita(data: CitaCreate):
    return await CitasDAO().create(data.dict())

@router.get("/{cid}", response_model=Cita)
async def obtener_cita(cid: str):
    cita = await CitasDAO().get(cid)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita

@router.put("/{cid}", response_model=Cita)
async def actualizar_cita(cid: str, data: CitaUpdate):
    return await CitasDAO().update(cid, data.dict(exclude_unset=True))

@router.delete("/{cid}", status_code=204)
async def eliminar_cita(cid: str):
    if not await CitasDAO().delete(cid):
        raise HTTPException(status_code=404, detail="Cita no encontrada")

@router.get("", response_model=List[Cita])
async def listar_citas():
    return await CitasDAO().list()
