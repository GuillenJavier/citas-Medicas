from fastapi import APIRouter, Request, HTTPException, Depends
from models.historial_model import HistorialMedico
from dao import historial_dao
from security.security import get_current_user

router = APIRouter(prefix="/api/historial", tags=["Historial Médico"])

@router.post("/", summary="Crear entrada de historial", dependencies=[Depends(get_current_user(["Médico", "Administrador"]))])
async def crear_historial(request: Request, datos: HistorialMedico):
    nuevo_id = await historial_dao.crear_historial(request.app.db, datos.dict())
    return {"mensaje": "Entrada de historial creada", "id": nuevo_id}

@router.get("/paciente/{paciente_id}", summary="Obtener historial por paciente", dependencies=[Depends(get_current_user(["Médico", "Administrador"]))])
async def historial_por_paciente(request: Request, paciente_id: str):
    return await historial_dao.obtener_historial_por_paciente(request.app.db, paciente_id)

@router.get("/{historial_id}", summary="Obtener historial por ID", dependencies=[Depends(get_current_user(["Médico", "Administrador"]))])
async def historial_individual(request: Request, historial_id: str):
    historial = await historial_dao.obtener_historial_por_id(request.app.db, historial_id)
    if not historial:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return historial

@router.put("/{historial_id}", summary="Actualizar historial", dependencies=[Depends(get_current_user(["Médico", "Administrador"]))])
async def actualizar_historial(request: Request, historial_id: str, datos: HistorialMedico):
    actualizados = await historial_dao.actualizar_historial(request.app.db, historial_id, datos.dict())
    if not actualizados:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"mensaje": "Registro actualizado correctamente"}

@router.delete("/{historial_id}", summary="Eliminar historial", dependencies=[Depends(get_current_user(["Administrador"]))])
async def eliminar_historial(request: Request, historial_id: str):
    eliminados = await historial_dao.eliminar_historial(request.app.db, historial_id)
    if not eliminados:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"mensaje": "Registro eliminado correctamente"}