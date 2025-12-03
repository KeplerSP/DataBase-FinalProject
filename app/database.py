from motor.motor_asyncio import AsyncIOMotorClient

# ❗ Inserta aquí tu cadena de conexión REAL de MongoDB Atlas.
#   Reemplaza <PASSWORD> por tu contraseña.
MONGO_URI = "mongodb+srv://leonardocordovag_db_user:IhQJ6UW6NsPa8GZV@cluster0.83cfzur.mongodb.net/streaming_db?retryWrites=true&w=majority&appName=Cluster0"

DB_NAME = "streaming_db"

client = None
db = None


async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    print("📡 Conectado a MongoDB Atlas.")


async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("🔌 Conexión a MongoDB cerrada.")