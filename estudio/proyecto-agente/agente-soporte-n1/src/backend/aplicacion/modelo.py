"""Conexión con el modelo de lenguaje (LLM): conversar y crear embeddings.

Etapa 0, ampliado en la etapa 2 con los embeddings. Usa la librería openai porque
Gemini y OpenRouter aceptan su formato: el mismo código sirve para los dos, solo
cambia la configuración del .env. Es el único archivo que habla con el modelo.
"""
from openai import OpenAI

from aplicacion import config

# Segundos máximos de espera por respuesta: así una llamada nunca queda colgada
# y la regla de los 8 minutos se puede cumplir (plan, "Cómo funciona cada regla").
# Sin reintentos automáticos: la librería reintenta 2 veces por defecto, y una llamada
# podría tardar hasta 3 veces el límite. Si falla, quien llama decide qué hacer.
ESPERA_MAXIMA = 60

# Cantidad de números de cada embedding. Debe coincidir con la columna vector(768)
# de la tabla fragmentos_conocimiento (01_esquema.sql).
DIMENSIONES_EMBEDDING = 768


def conectar_modelo():
    """Crea el cliente que habla con el modelo, con la URL, la clave y el límite de espera.
    Técnico: no viene del curso."""
    # Se crea en cada llamada y no al importar el archivo: así, si falta la clave,
    # el programa alcanza a mostrar su propio aviso en vez de un error de la librería.
    return OpenAI(base_url=config.LLM_BASE_URL, api_key=config.LLM_API_KEY, timeout=ESPERA_MAXIMA, max_retries=0)


def preguntar_al_modelo(mensajes):
    """Envía la conversación al modelo y devuelve el texto de su respuesta.

    Curso: el modelo es la pieza con que el agente razona, pero qué puede hacer
    lo fijan su identidad y sus instrucciones (Módulo 2, secciones 2.2 y 2.5).
    """
    respuesta = conectar_modelo().chat.completions.create(model=config.LLM_MODEL, messages=mensajes)
    # Si el proveedor bloquea la respuesta, el contenido llega vacío (None).
    return respuesta.choices[0].message.content or ""


def crear_embedding(textos):
    """Convierte una lista de textos en vectores de 768 números que representan su significado.
    Textos parecidos dan vectores cercanos: así se buscan documentos por lo que dicen.

    Curso: es la base del RAG con que el agente encuentra soluciones documentadas
    (Módulo 2, sección 2.5); el término RAG no viene en el curso.
    """
    respuesta = conectar_modelo().embeddings.create(
        model=config.LLM_MODELO_EMBEDDINGS, input=textos, dimensions=DIMENSIONES_EMBEDDING
    )
    return [dato.embedding for dato in respuesta.data]
