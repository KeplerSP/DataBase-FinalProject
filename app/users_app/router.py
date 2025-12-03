from fastapi import APIRouter, Request, Form, HTTPException, status, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from app.templates_config import templates
from .services import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
    search_users_service,
    activate_user,
    disable_user,
    authenticate_user
)

router = APIRouter()

# --- Obtener usuario actual (Cookie) ---
async def get_current_user(request: Request):
    user_email = request.cookies.get("user_session")
    if not user_email: return None
    db = request.app.state.db
    return await db.usuario.find_one({"email": user_email})

def require_role(role: str):
    async def role_checker(user=Depends(get_current_user)):
        if not user or user.get("role") != role:
            raise HTTPException(status_code=403, detail="No autorizado")
        return user
    return role_checker

# ===============================
# LOGIN (INICIAR SESIÓN)
# ===============================
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_submit(request: Request, email: str = Form(...), password: str = Form(...)):
    db = request.app.state.db
    user = await authenticate_user(db, email, password)
    
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request, "error": "Credenciales incorrectas"
        })
    
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="user_session", value=user["email"], httponly=True)
    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("user_session")
    return response

# ===============================
# REGISTRO (NUEVA FUNCIONALIDAD)
# ===============================
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register_submit(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    db = request.app.state.db
    # Por defecto, todos los registros nuevos son "user". Solo el admin pre-creado es "admin".
    result = await create_user(db, name, email, password, role="user")
    
    if not result:
        return templates.TemplateResponse("register.html", {
            "request": request, "error": "El correo ya está registrado"
        })
    
    # Si se registra bien, lo mandamos al login para que entre
    return RedirectResponse(url="/users/login", status_code=303)

# ===============================
# CRUD (Rutas existentes)
# ===============================
@router.get("/")
async def users_home(request: Request, current_user=Depends(get_current_user)):
    if not current_user: return RedirectResponse("/users/login")
    return templates.TemplateResponse("users_home.html", {"request": request, "current_user": current_user})

@router.get("/all")
async def list_users(request: Request, current_user=Depends(get_current_user)):
    if not current_user: return RedirectResponse("/users/login")
    db = request.app.state.db
    users = await get_all_users(db)
    return templates.TemplateResponse("users_list.html", {"request": request, "users": users, "current_user": current_user})

@router.get("/create")
async def create_user_form(request: Request, current_user=Depends(require_role("admin"))):
    return templates.TemplateResponse("users_create.html", {"request": request, "current_user": current_user})

@router.post("/create")
async def create_user_submit(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form("123456"), role: str = Form("user"), current_user=Depends(require_role("admin"))):
    db = request.app.state.db
    await create_user(db, name, email, password, role)
    return RedirectResponse("/users/all", status_code=303)

@router.get("/{user_id}")
async def detail_user(request: Request, user_id: str, current_user=Depends(get_current_user)):
    if not current_user: return RedirectResponse("/users/login")
    db = request.app.state.db
    user = await get_user_by_id(db, user_id)
    return templates.TemplateResponse("users_detail.html", {"request": request, "user": user, "current_user": current_user})

@router.get("/{user_id}/edit")
async def edit_user_form(request: Request, user_id: str, current_user=Depends(get_current_user)):
    if not current_user: return RedirectResponse("/users/login")
    db = request.app.state.db
    user = await get_user_by_id(db, user_id)
    return templates.TemplateResponse("users_edit.html", {"request": request, "user": user, "current_user": current_user})

@router.post("/{user_id}/edit")
async def edit_user_submit(request: Request, user_id: str, name: str = Form(...), email: str = Form(...), current_user=Depends(get_current_user)):
    db = request.app.state.db
    await update_user(db, user_id, name, email)
    return RedirectResponse(f"/users/{user_id}", status_code=303)

@router.get("/{user_id}/delete")
async def delete_user_form(request: Request, user_id: str, current_user=Depends(require_role("admin"))):
    db = request.app.state.db
    user = await get_user_by_id(db, user_id)
    return templates.TemplateResponse("users_delete_confirm.html", {"request": request, "user": user, "current_user": current_user})

@router.post("/{user_id}/delete")
async def delete_user_confirm(request: Request, user_id: str, admin_email: str = Form(...), current_user=Depends(require_role("admin"))):
    db = request.app.state.db
    if admin_email != current_user["email"]: return RedirectResponse("/users/all", status_code=303)
    await delete_user(db, user_id)
    return RedirectResponse("/users/all", status_code=303)

@router.get("/{user_id}/activate")
async def activate_user_form(request: Request, user_id: str, current_user=Depends(require_role("admin"))):
    db = request.app.state.db
    user = await get_user_by_id(db, user_id)
    return templates.TemplateResponse("users_activate_confirm.html", {"request": request, "user": user, "current_user": current_user})

@router.post("/{user_id}/activate")
async def activate_user_confirm(request: Request, user_id: str, admin_email: str = Form(...), current_user=Depends(require_role("admin"))):
    db = request.app.state.db
    await activate_user(db, user_id)
    return RedirectResponse("/users/all", status_code=303)

@router.get("/{user_id}/disable")
async def disable_user_form(request: Request, user_id: str, current_user=Depends(require_role("admin"))):
    db = request.app.state.db
    user = await get_user_by_id(db, user_id)
    return templates.TemplateResponse("users_disable_confirm.html", {"request": request, "user": user, "current_user": current_user})

@router.post("/{user_id}/disable")
async def disable_user_confirm(request: Request, user_id: str, admin_email: str = Form(...), current_user=Depends(require_role("admin"))):
    db = request.app.state.db
    await disable_user(db, user_id)
    return RedirectResponse("/users/all", status_code=303)

@router.get("/search")
async def search_users(request: Request, q: str = "", current_user=Depends(get_current_user)):
    if not current_user: return RedirectResponse("/users/login")
    db = request.app.state.db
    users = []
    if q.strip(): users = await search_users_service(db, q)
    return templates.TemplateResponse("users_search.html", {"request": request, "users": users, "query": q, "current_user": current_user})
