from datetime import datetime
from pydantic import BaseModel

class Notificacion(BaseModel):
    id: str
    usuarioId: str
    mensaje: str
    fechaEnvio: datetime = datetime.utcnow()
    estado: str | None = 'Pendiente'   # 'Pendiente' | 'Enviado'