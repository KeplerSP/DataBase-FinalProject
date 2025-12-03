from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import app.database as database
from app.database import connect_to_mongo, close_mongo_connection
from app.templates_config import templates

# Routers
from app.users_app.router import router as users_router
from app.content_app.router import router as content_router
from app.activity_app.router import router as activity_router


app = FastAPI(title="FISI Streaming")

# ==========================================
# Archivos estáticos
# ==========================================
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ==========================================
# Eventos de inicio / cierre
# ==========================================
@app.on_event("startup")
async def startup_event():
    print(">>> [startup] Iniciando conexión a MongoDB...")
    await connect_to_mongo()
    app.state.db = database.db
    
    # --- AUTO-CREACIÓN DE ADMIN ---
    # Crearemos el admin con la contraseña que pediste (1234566) si no existe.
    try:
        if database.db.usuario is not None:
            admin = await database.db.usuario.find_one({"email": "admin@example.com"})
            if not admin:
                print(">>> [startup] CREANDO ADMIN...")
                await database.db.usuario.insert_one({
                    "name": "Super Admin",
                    "email": "admin@example.com",
                    "password": "1234566", # Contraseña solicitada
                    "role": "admin",
                    "active": True
                })
                print(">>> [startup] Admin creado: admin@example.com")
    except Exception as e:
        print(f">>> [startup] Error verificando admin: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# ==========================================
# Home (CON DETECCIÓN DE ROL)
# ==========================================
@app.get("/")
async def home(request: Request):
    user_email = request.cookies.get("user_session")
    user = None
    
    # Si hay cookie, buscamos los detalles completos (nombre, rol, etc.)
    if user_email:
        user = await database.db.usuario.find_one({"email": user_email})

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "user": user # Pasamos el objeto usuario completo
        }
    )

# ==========================================
# Routers
# ==========================================
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(content_router, prefix="/content", tags=["Content"])
app.include_router(activity_router, prefix="/activity", tags=["Activity"])

