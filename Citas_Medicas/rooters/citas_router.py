from fastapi import APIRouter, HTTPException
from models.cita_model import Cita
from dao import citas_dao

router = APIRouter()

@router.post("/", summary="Agendar nueva cita")
async def agendar_cita(cita: Cita):
    conflicto = await citas_dao.cita_en_horario(cita.medicoId, cita.fecha.isoformat())
    if conflicto:
        raise HTTPException(status_code=400, detail="Ya hay una cita con ese médico en esa fecha y hora.")
    cita_id = await citas_dao.crear_cita(cita.dict())
    return {"mensaje": "Cita creada", "id": cita_id}

@router.get("/paciente/{paciente_id}", summary="Listar citas por paciente")
async def listar_citas(paciente_id: str):
    return await citas_dao.obtener_citas_por_paciente(paciente_id)

@router.get("/{cita_id}", summary="Obtener cita por ID")
async def ver_cita(cita_id: str):
    cita = await citas_dao.obtener_cita_por_id(cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita

@router.delete("/{cita_id}", summary="Cancelar cita por ID")
async def cancelar_cita(cita_id: str):
    borradas = await citas_dao.eliminar_cita(cita_id)
    if not borradas:
        raise HTTPException(status_code=404, detail="No se encontró la cita para eliminar")
    return {"mensaje": "Cita cancelada correctamente"}

@router.put("/{cita_id}", summary="Actualizar cita por ID")
async def actualizar_cita(cita_id: str, datos: Cita):
    modificadas = await citas_dao.actualizar_cita(cita_id, datos.dict())
    if not modificadas:
        raise HTTPException(status_code=404, detail="No se encontró la cita para actualizar")
    return {"mensaje": "Cita actualizada correctamente"}
