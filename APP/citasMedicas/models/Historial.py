from datetime import datetime
from pydantic import BaseModel

class Historial(BaseModel):
    id: str
    pacienteId: str
    citaId: str
    diagnostico: str
    tratamiento: str
    fechaRegistro: datetime = datetime.utcnow()