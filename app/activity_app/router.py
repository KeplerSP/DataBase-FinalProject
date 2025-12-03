from fastapi import APIRouter, Request, Depends
from app.templates_config import templates
from datetime import datetime

router = APIRouter()

# ===============================
# Usuario “dummy” para pruebas
# ===============================
async def get_current_user(request: Request):
    return {
        "_id": "123456",
        "name": "Admin Demo",
        "email": "admin@example.com",
        "role": "admin"
    }

# ===============================
# Página principal de Activity
# ===============================
@router.get("/")
async def activity_home(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "activity_home.html",
        {"request": request, "current_user": current_user}
    )

# ===============================
# Listar búsquedas
# ===============================
@router.get("/searches")
async def list_searches(request: Request, current_user=Depends(get_current_user)):
    db = request.app.state.db
    busquedas = await db.busquedas.find().to_list(200)
    return templates.TemplateResponse(
        "searches_list.html",
        {"request": request, "busquedas": busquedas, "current_user": current_user}
    )

# ===============================
# Listar likes
# ===============================
@router.get("/likes")
async def list_likes(request: Request, current_user=Depends(get_current_user)):
    db = request.app.state.db
    likes = await db.likecontenido.find().to_list(200)
    return templates.TemplateResponse(
        "likes_list.html",
        {"request": request, "likes": likes, "current_user": current_user}
    )

# ===============================
# Listar reproducciones (plays)
# ===============================
@router.get("/plays")
async def list_plays(request: Request, current_user=Depends(get_current_user)):
    db = request.app.state.db
    plays = await db.reproducciones.find().to_list(200)
    return templates.TemplateResponse(
        "plays_list.html",
        {"request": request, "plays": plays, "current_user": current_user}
    )

# ===============================
# Listar comentarios
# ===============================
@router.get("/comments")
async def list_comments(request: Request, current_user=Depends(get_current_user)):
    db = request.app.state.db
    comments = await db.comentarios.find().to_list(200)
    return templates.TemplateResponse(
        "comments_list.html",
        {"request": request, "comments": comments, "current_user": current_user}
    )




