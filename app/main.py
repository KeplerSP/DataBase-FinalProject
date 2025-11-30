from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import app.database as database
from app.database import connect_to_mongo, close_mongo_connection
from app.templates_config import templates

# Routers
from app.users_app.router import router as users_router
from app.content_app.router import router as content_router
from app.activity_app.router import router as activity_router
from app.dashboard_app.router import router as dashboard_router

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
    print(">>> [startup] Resultado db =", database.db)
    app.state.db = database.db
    print(">>> [startup] app.state.db =", app.state.db)


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()


# ==========================================
# Home (usa plantilla global)
# ==========================================
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )


# ==========================================
# Routers
# ==========================================
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(content_router, prefix="/content", tags=["Content"])
app.include_router(activity_router, prefix="/activity", tags=["Activity"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
