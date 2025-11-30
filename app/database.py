from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "streaming_db")

client = None
db = None


async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    print("📡 Conectado a MongoDB.")


async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("🔌 Conexión a MongoDB cerrada.")
