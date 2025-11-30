# app/templates_config.py
from jinja2 import ChoiceLoader, FileSystemLoader
from fastapi.templating import Jinja2Templates
import os

# base del proyecto (carpeta app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rutas (ordenadas por prioridad)
search_paths = [
    os.path.join(BASE_DIR, "templates"),                 # global (recomendado primero)
    os.path.join(BASE_DIR, "users_app", "templates"),   # templates por app (opcional)
    os.path.join(BASE_DIR, "content_app", "templates"),
    os.path.join(BASE_DIR, "activity_app", "templates"),
    os.path.join(BASE_DIR, "dashboard_app", "templates"),
]

# Inicializamos Jinja apuntando a la carpeta global (necesario para Jinja2Templates)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Reemplazamos el loader por un ChoiceLoader con todas las rutas
templates.env.loader = ChoiceLoader([FileSystemLoader(p) for p in search_paths])

# (opcional) debug: imprime paths al iniciarse (comenta si quieres silencio)
# print("Jinja2 search paths:", [p for p in search_paths])
