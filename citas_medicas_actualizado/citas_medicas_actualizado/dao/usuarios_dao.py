import bcrypt
from bson import ObjectId

def parse_object_id(id_str: str):
    try:
        return ObjectId(id_str)
    except Exception:
        return None

async def insertar_usuario(db, usuario: dict):
    existente = await db.usuarios.find_one({"correo": usuario["correo"]})
    if existente:
        return {"error": "Ya existe un usuario con ese correo"}

    usuario["contraseña"] = bcrypt.hashpw(
        usuario["contraseña"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    result = await db.usuarios.insert_one(usuario)
    return {"id": str(result.inserted_id)}

async def verificar_credenciales(db, correo: str, contraseña: str):
    usuario = await db.usuarios.find_one({"correo": correo})
    if not usuario:
        return {"error": "Usuario no encontrado"}

    if not bcrypt.checkpw(
        contraseña.encode("utf-8"), usuario["contraseña"].encode("utf-8")
    ):
        return {"error": "Contraseña incorrecta"}

    return {
        "id": str(usuario["_id"]),
        "nombre": usuario.get("nombre"),
        "correo": usuario.get("correo"),
        "tipo": usuario.get("tipo")
    }

async def obtener_usuario_por_id(db, usuario_id: str):
    object_id = parse_object_id(usuario_id)
    if not object_id:
        return None
    usuario = await db.usuarios.find_one({"_id": object_id})
    if usuario:
        usuario["_id"] = str(usuario["_id"])
        del usuario["contraseña"]
    return usuario

async def actualizar_usuario(db, usuario_id: str, nuevos_datos: dict):
    object_id = parse_object_id(usuario_id)
    if not object_id:
        return 0

    if "contraseña" in nuevos_datos:
        nuevos_datos["contraseña"] = bcrypt.hashpw(
            nuevos_datos["contraseña"].encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    result = await db.usuarios.update_one({"_id": object_id}, {"$set": nuevos_datos})
    return result.modified_count

async def eliminar_usuario(db, usuario_id: str):
    object_id = parse_object_id(usuario_id)
    if not object_id:
        return 0
    result = await db.usuarios.delete_one({"_id": object_id})
    return result.deleted_count
