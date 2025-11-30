from fastapi import APIRouter, Request
from app.templates_config import templates

router = APIRouter()


@router.get("/")
async def content_home(request: Request):
    return templates.TemplateResponse("content_home.html", {"request": request})


@router.get("/all")
async def list_content(request: Request):
    db = request.app.state.db
    contenidos = await db.contenido.find().to_list(300)
    return templates.TemplateResponse("content_list.html", {
        "request": request,
        "contenidos": contenidos
    })
