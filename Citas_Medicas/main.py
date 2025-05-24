from fastapi import FastAPI
from rooters.usuarios_router import router as usuarios_router
from rooters.citas_router import router as citas_router

# Instancia de la aplicación
app = FastAPI(
    title="Sistema de Citas Médicas",
    description="API para agendar y gestionar citas médicas",
    version="1.0.0"
)

# Registrar routers de cada microservicio
app.include_router(usuarios_router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(citas_router, prefix="/api/citas", tags=["Citas"])

print(app.routes)

# Ruta raíz
@app.get("/", tags=["default"])
async def root():
    return {"mensaje": "Bienvenido a la API de Citas Médicas"}
