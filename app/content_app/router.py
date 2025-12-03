import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from app.templates_config import templates
from app.database import db 
from . import services

router = APIRouter()

# --- RUTAS DE LISTADO ---
# Agregamos múltiples decoradores para que la misma función responda a:
# 1. /content/ (Index)
# 2. /content/list (Lista estándar)
# 3. /content/all (La ruta que estás intentando usar ahora)
@router.get("/", response_class=HTMLResponse, name="content.list.index")
@router.get("/list", response_class=HTMLResponse, name="content.list")
@router.get("/all", response_class=HTMLResponse, name="content.list.all") 
async def list_content(request: Request):
    """
    Muestra el catálogo de contenido.
    Responde en /, /list y /all para evitar errores 404.
    """
    print(f"DEBUG: Accediendo a la lista desde ruta: {request.url.path}")
    
    contenidos = services.get_content_list(db)
    
    return templates.TemplateResponse(
        "content_list.html", 
        {"request": request, "contenidos": contenidos}
    )

# --- RUTA DE IMÁGENES ---
@router.get("/img/{filename}", response_class=FileResponse, name="content.image")
async def get_content_image(filename: str):
    """
    Sirve imágenes desde app/content_app/static/
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "static", filename)
    
    # Debug para verificar rutas en consola
    print(f"DEBUG: Buscando imagen: {filename}")
    
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        print(f"DEBUG: ERROR - Imagen no encontrada en: {image_path}")
        return HTMLResponse(content="Imagen no encontrada", status_code=404)