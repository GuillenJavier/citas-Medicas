# main.py – Adaptado para ShopiteszREST2025

from importlib import reload
from fastapi import FastAPI
import uvicorn

# Importa la clase de conexión a Mongo
from dao.database import Conexion

# Importa los routers individuales
from routers import UsuarioRouter, CitaRouter, HistorialRouter, NotificacionesRouter

# Crear instancia de FastAPI
app = FastAPI()

# Registrar los routers
app.include_router(usuarios.router)
app.include_router(citas.router)
app.include_router(historial.router)
app.include_router(notificaciones.router)

# Ruta de prueba (inicio)
@app.get("/")
async def home():
    salida = {"mensaje": "Bienvenido a la API Shopitesz 2025"}
    return salida

# Evento al iniciar la app
@app.on_event("startup")
async def startup():
    print("Conectando a MongoDB...")
    conexion = Conexion()
    app.conexion = conexion
    app.db = conexion.getDB()

# Evento al cerrar la app
@app.on_event("shutdown")
async def shutdown():
    print("Cerrando conexión a MongoDB")
    app.conexion.cerrar()


# Punto de entrada para ejecución directa (modo desarrollo)
if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
