from dao.mongo_connection import db
from bson import ObjectId

#  Función auxiliar para convertir ID de forma segura
def parse_object_id(id_str: str):
    try:
        return ObjectId(id_str)
    except Exception:
        return None

async def crear_cita(cita: dict):
    result = await db.citas.insert_one(cita)
    return str(result.inserted_id)

async def obtener_citas_por_paciente(paciente_id: str):
    return await db.citas.find({"pacienteId": paciente_id}).to_list(100)

async def obtener_cita_por_id(cita_id: str):
    object_id = parse_object_id(cita_id)
    if not object_id:
        return None
    return await db.citas.find_one({"_id": object_id})

async def eliminar_cita(cita_id: str):
    object_id = parse_object_id(cita_id)
    if not object_id:
        return 0
    result = await db.citas.delete_one({"_id": object_id})
    return result.deleted_count

async def actualizar_cita(cita_id: str, nueva_info: dict):
    object_id = parse_object_id(cita_id)
    if not object_id:
        return 0
    result = await db.citas.update_one({"_id": object_id}, {"$set": nueva_info})
    return result.modified_count

async def cita_en_horario(medico_id: str, fecha: str):
    return await db.citas.find_one({"medicoId": medico_id, "fecha": fecha})
