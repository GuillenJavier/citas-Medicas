from fastapi import FastAPI
from rooters.usuarios_router import router as usuarios_router
from rooters.citas_router import router as citas_router
from dao.mongo_connection import Conexion
from rooters.historial_router import router as historial_router
from rooters.notificacion_router import router as notificacion_router

app = FastAPI(
    title="Citas Medicas",
    description="Bienvenido a la API Citas Medicas",
    version="1.0.0"
)

app.include_router(usuarios_router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(citas_router, prefix="/api/citas", tags=["Citas"])
app.include_router(historial_router)

app.include_router(notificacion_router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "API activa"}

@app.get("/check")
async def check():
    return {"proyecto": "BASE MONGO OK"}

@app.on_event("startup")
async def startup():
    print(" Conectando con MongoDB...")
    conexion = Conexion()
    app.conexion = conexion
    app.db = conexion.getDB()
    try:
        await app.db.command("ping")
        print(" Conexión establecida con MongoDB.")
    except Exception as e:
        print(" Error al conectar con MongoDB:", e)

@app.on_event("shutdown")
async def shutdown():
    print(" Cerrando conexión con MongoDB...")
    if hasattr(app, "conexion"):
        app.conexion.cerrar()
