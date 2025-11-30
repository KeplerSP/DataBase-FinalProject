from app.templates_config import templates
from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def activity_home(request: Request):
    return templates.TemplateResponse("activity_home.html", {"request": request})


@router.get("/searches")
async def list_searches(request: Request):
    db = request.app.state.db  # <--- ESTA ES LA FORMA CORRECTA
    busquedas = await db.busqueda.find().to_list(200)
    return templates.TemplateResponse(
        "searches_list.html",
        {"request": request, "busquedas": busquedas}
    )


@router.get("/likes")
async def list_likes(request: Request):
    db = request.app.state.db
    likes = await db.likecontenido.find().to_list(200)
    return templates.TemplateResponse(
        "likes_list.html",
        {"request": request, "likes": likes}
    )
