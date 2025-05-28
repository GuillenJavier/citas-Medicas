from pydantic import BaseModel, EmailStr, Field

class Usuario(BaseModel):
    nombre: str = Field(..., max_length=100)
    correo: EmailStr
    contraseña: str = Field(..., min_length=8)
    tipo: str = Field(..., pattern="^(Paciente|Médico|Administrador)$")
    telefono: str | None = Field(default=None, max_length=10)
    domicilio: str | None = Field(default=None, max_length=150)

class LoginUsuario(BaseModel):
    correo: EmailStr
    contraseña: str = Field(..., min_length=8)
