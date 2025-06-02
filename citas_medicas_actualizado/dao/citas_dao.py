from bson import ObjectId

async def crear_cita(db, cita: dict):
    cita["pacienteId"] = ObjectId(cita["pacienteId"])
    cita["medicoId"] = ObjectId(cita["medicoId"])
    result = await db.citas.insert_one(cita)
    return str(result.inserted_id)

async def obtener_citas_por_paciente(db, paciente_id: str):
    return await db.citas.find({"pacienteId": ObjectId(paciente_id)}).to_list(100)

async def obtener_cita_por_id(db, cita_id: str):
    return await db.citas.find_one({"_id": ObjectId(cita_id)})

async def eliminar_cita(db, cita_id: str):
    result = await db.citas.delete_one({"_id": ObjectId(cita_id)})
    return result.deleted_count

async def actualizar_cita(db, cita_id: str, nueva_info: dict):
    if "pacienteId" in nueva_info:
        nueva_info["pacienteId"] = ObjectId(nueva_info["pacienteId"])
    if "medicoId" in nueva_info:
        nueva_info["medicoId"] = ObjectId(nueva_info["medicoId"])
    result = await db.citas.update_one({"_id": ObjectId(cita_id)}, {"$set": nueva_info})
    return result.modified_count

async def cita_en_horario(db, medico_id: str, fecha: str):
    return await db.citas.find_one({"medicoId": ObjectId(medico_id), "fecha": fecha})
