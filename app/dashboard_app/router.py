from fastapi import APIRouter, Request
from app.templates_config import templates

router = APIRouter()


@router.get("/")
async def dashboard_home(request: Request):
    db = request.app.state.db
    total_users = await db.usuario.count_documents({})
    total_content = await db.contenido.count_documents({})
    total_reproductions = await db.reproduccion.count_documents({})

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_users": total_users,
        "total_content": total_content,
        "total_reproductions": total_reproductions
    })
