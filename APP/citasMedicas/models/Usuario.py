from datetime import datetime
from pydantic import BaseModel

class Usuario(BaseModel):
    id: str
    nombre: str
    correo: str
    contraseña: str
    tipo: str
    telefono: str | None = None
    domicilio: str | None = None
