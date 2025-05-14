from datetime import datetime
from pydantic import BaseModel

class Cita(BaseModel):
    id: str
    pacienteId: str
    medicoId: str
    fecha: datetime
    estado: str = "Pendiente"
    notas: str | None = None
