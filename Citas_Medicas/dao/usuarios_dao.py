from dao.mongo_connection import db

async def insertar_usuario(usuario: dict):
    result = await db.usuarios.insert_one(usuario)
    return str(result.inserted_id)
