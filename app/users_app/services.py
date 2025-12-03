from bson import ObjectId

# ===============================
# Listar usuarios
# ===============================
async def get_all_users(db):
    return await db.usuario.find().to_list(500)


# ===============================
# Obtener usuario por ID
# ===============================
async def get_user_by_id(db, user_id: str):
    return await db.usuario.find_one({"_id": ObjectId(user_id)})


# ===============================
# Obtener usuario por Email (Necesario para Login y Registro)
# ===============================
async def get_user_by_email(db, email: str):
    return await db.usuario.find_one({"email": email})


# ===============================
# Crear usuario (CORREGIDO Y AJUSTADO)
# ===============================
async def create_user(db, name: str, email: str, password: str, role: str = "user"):
    # Verificar si ya existe el correo
    existe = await get_user_by_email(db, email)
    if existe:
        return None  # Indicamos que ya existe

    nuevo = {
        "name": name,
        "email": email,
        "password": password,
        "role": role,
        "active": True
    }
    await db.usuario.insert_one(nuevo)
    return nuevo


# ===============================
# Autenticar usuario (LOGIN)
# ===============================
async def authenticate_user(db, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return False
    if user.get("password") != password:
        return False
    return user


# ===============================
# Editar usuario
# ===============================
async def update_user(db, user_id: str, name: str, email: str):
    return await db.usuario.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"name": name, "email": email}}
    )


# ===============================
# Eliminar usuario
# ===============================
async def delete_user(db, user_id: str):
    return await db.usuario.delete_one({"_id": ObjectId(user_id)})


# ========================
# Buscar usuarios
# ========================
async def search_users_service(db, query: str):
    return await db.usuario.find({
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"email": {"$regex": query, "$options": "i"}}
        ]
    }).to_list(200)


# ========================
# Activar usuario
# ========================
async def activate_user(db, user_id: str):
    return await db.usuario.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"active": True}}
    )


# ========================
# Desactivar usuario
# ========================
async def disable_user(db, user_id: str):
    return await db.usuario.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"active": False}}
    )