"""Conexión con PostgreSQL y consultas a la base de conocimiento.

Etapa 2. Usa la librería pg8000 (licencia BSD, decisión D1). Es el único archivo
que habla con la base de datos: el resto del programa llama a estas funciones.
Los vectores se envían como texto y PostgreSQL los convierte con ::vector (decisión D2).
Quien abre una conexión la cierra al terminar, aunque haya un error (try/finally);
desde la etapa 3, el agente usa una sola conexión por ticket.
"""
import pg8000.dbapi

from aplicacion import config

ESPERA_CONEXION = 10  # segundos


def conectar():
    """Abre una conexión con PostgreSQL usando los datos del .env.
    Espera como máximo ESPERA_CONEXION segundos, para no quedar colgado si la base no responde.
    Técnico: no viene del curso."""
    return pg8000.dbapi.connect(
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        host=config.POSTGRES_HOST,
        database=config.POSTGRES_DB,
        timeout=ESPERA_CONEXION,
    )


def vector_a_texto(vector):
    """Convierte una lista de números en el texto que entiende pgvector: "[0.12,-0.03,...]".
    Técnico: no viene del curso (decisión D2)."""
    return "[" + ",".join(str(numero) for numero in vector) + "]"


def guardar_fragmento(conexion, documento, seccion, orden, texto, vector, hash_documento):
    """Guarda un fragmento de un documento con su vector en la base de conocimiento,
    junto con el modelo que lo creó y la huella del documento.

    Curso: la base de conocimiento son las soluciones documentadas con que
    responde el agente (Módulo 2, sección 2.5). Guardar el origen de cada vector
    es una práctica de RAG que no viene en el curso (decisión D8).
    """
    conexion.cursor().execute(
        "INSERT INTO fragmentos_conocimiento "
        "(documento, seccion, orden, texto, embedding, modelo_embedding, hash_documento) "
        "VALUES (%s, %s, %s, %s, %s::vector, %s, %s)",
        (documento, seccion, orden, texto, vector_a_texto(vector), config.LLM_MODELO_EMBEDDINGS, hash_documento),
    )


def buscar_fragmentos(conexion, vector, cantidad=5):
    """Devuelve los fragmentos más parecidos a un vector: (documento, sección, texto, similitud).
    La similitud va de 0 a 1; mientras más alta, más se parece al texto buscado.

    Curso: el agente solo responde con soluciones documentadas; si no encuentra
    una que corresponda, escala (Módulo 2, sección 2.5).
    """
    cursor = conexion.cursor()
    # <=> mide la distancia de coseno: ordenar de menor a mayor trae primero lo más parecido.
    # Solo se comparan vectores creados con el mismo modelo que la consulta (decisión D8).
    cursor.execute(
        "SELECT documento, seccion, texto, 1 - (embedding <=> %s::vector) AS similitud "
        "FROM fragmentos_conocimiento WHERE modelo_embedding = %s "
        "ORDER BY embedding <=> %s::vector LIMIT %s",
        (vector_a_texto(vector), config.LLM_MODELO_EMBEDDINGS, vector_a_texto(vector), cantidad),
    )
    return cursor.fetchall()
