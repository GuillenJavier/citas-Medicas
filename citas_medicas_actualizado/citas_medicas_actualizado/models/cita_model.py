from pydantic import BaseModel, Field
from datetime import datetime

class Cita(BaseModel):
    pacienteId: str
    medicoId: str
    fecha: datetime
    estado: str = Field(..., pattern="^(Pendiente|Confirmada|Cancelada|Finalizada)$")
    notas: str | None = None
