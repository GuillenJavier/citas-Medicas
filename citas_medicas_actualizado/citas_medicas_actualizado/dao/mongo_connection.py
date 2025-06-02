from motor.motor_asyncio import AsyncIOMotorClient
import os

class Conexion:
    def __init__(self):
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client["citasMedicas"]

    def getDB(self):
        return self.db

    def cerrar(self):
        self.client.close()
