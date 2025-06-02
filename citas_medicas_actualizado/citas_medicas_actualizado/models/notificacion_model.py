from pydantic import BaseModel, Field
from datetime import datetime

class Notificacion(BaseModel):
    usuarioId: str = Field(..., description="ID del usuario que recibe la notificación")
    mensaje: str
    leido: bool = False
    fecha: datetime = Field(default_factory=datetime.utcnow)