# **DataBase Final Project**
## NoSQL project using MongoDB and FastAPI for a streaming database


### Pasos:
### 1. Crear un entorno virtual
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
### 2. Instalar dependencias:
```bash
pip install -r requirements.txt
```
### 3. Ejecutar servidor
```bash
uvicorn app.main:app --reload
```

# División del Proyecto

## **APP 1 — users_app**

**Maneja todo lo relacionado a usuarios y perfiles.**

Tablas que agrupa:

* `usuario`
* `cuenta`
* `perfil`
* `region` (opcional)
* `pertenecea` (relación cuenta–usuario)

Endpoints posibles:

* `/users`
* `/accounts`
* `/profiles`

---

## **APP 2 — content_app**

**Todo lo relacionado al contenido audiovisual.**

Tablas que agrupa:

* `contenido`
* `genero`
* `temporada`
* `episodio`
* `ofrece` (relación contenido–perfil/servicio)

Endpoints:

* `/content`
* `/genres`
* `/seasons`
* `/episodes`

---

**Interacciones del usuario con la plataforma.**

Tablas:

* `interaccion`
* `busqueda`
* `likecontenido`
* `reproduccion`
* `registra` (actividad registrada en perfil)

Endpoints:

* `/activity/searches`
* `/activity/likes`
* `/activity/playback`

---

## **APP 4 — dashboard_app**

**Vista general: reportes, estadísticas y UI principal.**

NO maneja tablas directamente, pero usa datos de las otras apps.

Ejemplos de vistas:

* página principal
* dashboards
* reportes en HTML
* lista de contenido integrada
* estadísticas de usuarios, géneros, reproducciones

Endpoints:

* `/dashboard`
* `/report/users`
* `/report/content`

---


## Estructura del proyecto (para 4 apps)

```
project/
│── app/
│   ├── main.py
│   ├── database.py
│   ├── templates_config.py   
│   ├── users_app/
│   │   ├── router.py
│   │   ├── templates/
│   │   └── services.py
│   ├── content_app/
│   │   ├── router.py
│   │   ├── templates/
│   │   └── services.py
│   ├── activity_app/
│   │   ├── router.py
│   │   ├── templates/
│   │   └── services.py
│   ├── dashboard_app/
│   │   ├── router.py
│   │   ├── templates/
│   │   └── services.py
│   ├── templates/  (global)
│   └── static/
│
│── requirements.txt
│── README.md
```
