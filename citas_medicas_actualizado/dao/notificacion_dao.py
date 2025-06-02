from bson import ObjectId

async def crear_notificacion(db, noti: dict):
    noti["usuarioId"] = ObjectId(noti["usuarioId"])
    result = await db.notificaciones.insert_one(noti)
    return str(result.inserted_id)

async def listar_notificaciones(db, usuario_id: str):
    return await db.notificaciones.find({"usuarioId": ObjectId(usuario_id)}).sort("fecha", -1).to_list(100)

async def marcar_como_leida(db, noti_id: str):
    result = await db.notificaciones.update_one({"_id": ObjectId(noti_id)}, {"$set": {"leido": True}})
    return result.modified_count

async def eliminar_notificacion(db, noti_id: str):
    result = await db.notificaciones.delete_one({"_id": ObjectId(noti_id)})
    return result.deleted_count
