from datetime import datetime, timezone
from bson import ObjectId
from .database import get_database
from .base import BaseDAO

class HistorialDAO(BaseDAO):
    collection_name = "historial_medico"

    async def _collection(self):
        db = await get_database()
        return db[self.collection_name]

    async def create(self, data: dict[str, Any]):
        # auto‑fecha si no viene
        data.setdefault("fechaRegistro", datetime.now(timezone.utc))
        coll = await self._collection()
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

    async def delete(self, _id: str):
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