from fastapi import APIRouter, Request, HTTPException
from models.cita_model import Cita
from dao import citas_dao

router = APIRouter()

@router.post("/", summary="Agendar Cita")
async def agendar_cita(request: Request, cita: Cita):
    conflicto = await citas_dao.cita_en_horario(request.app.db, cita.medicoId, cita.fecha.isoformat())
    if conflicto:
        raise HTTPException(status_code=400, detail="Ya hay una cita con ese médico en esa fecha y hora.")
    cita_id = await citas_dao.crear_cita(request.app.db, cita.dict())
    return {"mensaje": "Cita creada", "id": cita_id}

@router.get("/paciente/{paciente_id}", summary="Listar Citas")
async def listar_citas(request: Request, paciente_id: str):
    return await citas_dao.obtener_citas_por_paciente(request.app.db, paciente_id)

@router.get("/{cita_id}", summary="Ver Cita por ID")
async def ver_cita(request: Request, cita_id: str):
    cita = await citas_dao.obtener_cita_por_id(request.app.db, cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita

@router.delete("/{cita_id}", summary="Cancelar Cita")
async def cancelar_cita(request: Request, cita_id: str):
    borradas = await citas_dao.eliminar_cita(request.app.db, cita_id)
    if not borradas:
        raise HTTPException(status_code=404, detail="No se encontró la cita para eliminar")
    return {"mensaje": "Cita cancelada correctamente"}

@router.put("/{cita_id}", summary="Actualizar Cita")
async def actualizar_cita(request: Request, cita_id: str, datos: Cita):
    modificadas = await citas_dao.actualizar_cita(request.app.db, cita_id, datos.dict())
    if not modificadas:
        raise HTTPException(status_code=404, detail="No se encontró la cita para actualizar")
    return {"mensaje": "Cita actualizada correctamente"}
