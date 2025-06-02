from bson import ObjectId

async def crear_historial(db, entrada: dict):
    entrada["pacienteId"] = ObjectId(entrada["pacienteId"])
    result = await db.historial.insert_one(entrada)
    return str(result.inserted_id)

async def obtener_historial_por_paciente(db, paciente_id: str):
    return await db.historial.find({"pacienteId": ObjectId(paciente_id)}).to_list(100)

async def obtener_historial_por_id(db, historial_id: str):
    return await db.historial.find_one({"_id": ObjectId(historial_id)})

async def actualizar_historial(db, historial_id: str, nueva_info: dict):
    result = await db.historial.update_one({"_id": ObjectId(historial_id)}, {"$set": nueva_info})
    return result.modified_count

async def eliminar_historial(db, historial_id: str):
    result = await db.historial.delete_one({"_id": ObjectId(historial_id)})
    return result.deleted_count