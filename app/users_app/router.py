from fastapi import APIRouter, Request
from app.templates_config import templates

router = APIRouter()


@router.get("/")
async def users_home(request: Request):
    return templates.TemplateResponse("users_home.html", {"request": request})


@router.get("/all")
async def list_users(request: Request):
    db = request.app.state.db
    usuarios = await db.usuario.find().to_list(200)
    return templates.TemplateResponse("users_list.html", {
        "request": request,
        "usuarios": usuarios
    })
