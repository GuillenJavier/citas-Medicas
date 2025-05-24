from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum

class EstadoCita(str, Enum):
    pendiente = "Pendiente"
    confirmada = "Confirmada"
    cancelada = "Cancelada"
    finalizada = "Finalizada"

class Cita(BaseModel):
    pacienteId: str
    medicoId: str
    fecha: datetime
    estado: EstadoCita
    notas: str | None = Field(default=None, max_length=250)

    @validator("fecha")
    def validar_fecha_futura(cls, value):
        if value < datetime.now():
            raise ValueError("La fecha debe ser en el futuro")
        return value
