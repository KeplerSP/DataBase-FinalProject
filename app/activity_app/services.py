# Servicio para Activity App

# ===============================
# Listar todas las búsquedas
# ===============================
async def get_all_searches(db):
    return await db.busqueda.find().to_list(200)

# ===============================
# Listar todos los likes
# ===============================
async def get_all_likes(db):
    return await db.likecontenido.find().to_list(200)
