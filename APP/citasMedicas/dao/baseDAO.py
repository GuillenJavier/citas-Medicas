from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os

_MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
_DB_NAME: str = os.getenv("MONGO_DB", "shopitesz_db")

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None

async def get_database() -> AsyncIOMotorDatabase:
    """Singleton‑ish helper that returns the app database."""
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(_MONGO_URI)
        _db = _client[_DB_NAME]
    return _db