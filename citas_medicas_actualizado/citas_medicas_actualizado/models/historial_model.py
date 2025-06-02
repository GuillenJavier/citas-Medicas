from pydantic import BaseModel, Field
from datetime import datetime

class HistorialMedico(BaseModel):
    pacienteId: str = Field(..., description="ID del paciente")
    fecha: datetime = Field(default_factory=datetime.utcnow, description="Fecha del registro")
    descripcion: str
    diagnostico: str
    tratamiento: str