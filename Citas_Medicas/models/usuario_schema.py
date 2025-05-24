from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class TipoUsuario(str, Enum):
    paciente = "Paciente"
    medico = "Médico"
    administrador = "Administrador"

class Usuario(BaseModel):
    nombre: str = Field(..., max_length=100)
    correo: EmailStr
    contraseña: str = Field(..., min_length=8)
    tipo: TipoUsuario
    telefono: str | None = Field(default=None, max_length=10)
    domicilio: str | None = Field(default=None, max_length=150)
