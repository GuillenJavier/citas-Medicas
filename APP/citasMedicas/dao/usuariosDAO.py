from bson import ObjectId
from pydantic import EmailStr
from .database import get_database
from .base import BaseDAO

class UsersDAO(BaseDAO):
    collection_name = "usuarios"

    async def _collection(self):
        db = await get_database()
        return db[self.collection_name]

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        # Normaliza y valida correo
        correo: EmailStr = data["correo"]  # raises ValidationError if invalid
        data["correo"] = correo.lower()

        coll = await self._collection()
        # Asegurar unicidad
        existing = await coll.find_one({"correo": data["correo"]})
        if existing:
            raise ValueError("Correo ya registrado")
        res = await coll.insert_one(data)
        return {"_id": str(res.inserted_id), **data}

    async def get(self, _id: str):
        coll = await self._collection()
        doc = await coll.find_one({"_id": ObjectId(_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def update(self, _id: str, data: dict[str, Any]):
        coll = await self._collection()
        await coll.update_one({"_id": ObjectId(_id)}, {"$set": data})
        return await self.get(_id)

    async def delete(self, _id: str) -> bool:
        coll = await self._collection()
        res = await coll.delete_one({"_id": ObjectId(_id)})
        return res.deleted_count == 1

    async def list(self, *, skip: int = 0, limit: int = 20, filters: dict | None = None):
        coll = await self._collection()
        cursor = coll.find(filters or {}).skip(skip).limit(limit)
        docs = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            docs.append(doc)
        return docs
