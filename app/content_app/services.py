from app.database import db

def get_content_list(db_session=None):
    """
    Obtiene la lista de contenidos y genera el nombre de archivo de la imagen
    basado en el título.
    """
    
    # ---------------------------------------------------------
    # DATOS BASADOS EN TU CAPTURA DE PANTALLA
    # ---------------------------------------------------------
    raw_data = [
        {
            "titulo": "Inception",
            "tipo": "Película",
            "descripcion": "Un ladrón que roba secretos a través de los sueños.",
            "anio": 2010,
            "duracion": "148 min",
            "generos": ["Ciencia Ficción", "Acción"]
        },
        {
            "titulo": "Interstellar",
            "tipo": "Película",
            "descripcion": "Exploración espacial para salvar a la humanidad.",
            "anio": 2014,
            "duracion": "169 min",
            "generos": ["Ciencia Ficción", "Drama"]
        },
        {
            "titulo": "Stranger Things",
            "tipo": "Serie",
            "descripcion": "Niños enfrentan fenómenos paranormales en Hawkins.",
            "anio": 2016,
            "generos": ["Ciencia Ficción", "Terror"],
            # Simulamos el Array(2) de temporadas que se ve en la imagen
            "temporadas": [
                {"numero": 1, "episodios": [1,2,3,4,5,6,7,8]},
                {"numero": 2, "episodios": [1,2,3,4,5,6,7,8,9]}
            ]
        }
    ]
    # ---------------------------------------------------------

    processed_list = []

    for item in raw_data:
        # Creamos una copia para no alterar el objeto original
        content = item.copy()
        
        # Generamos el nombre del archivo de imagen basado en el título
        # La lógica busca: "Título.jpg"
        # Ej: "Inception" -> "Inception.jpg"
        
        # Obtenemos el título usando 'titulo' (BD) o 'title' (alternativo)
        title = content.get('titulo') or content.get('title') or 'default'
        
        # Asignamos el nombre del archivo
        content['image_file'] = f"{title}.jpg"
        
        processed_list.append(content)

    return processed_list