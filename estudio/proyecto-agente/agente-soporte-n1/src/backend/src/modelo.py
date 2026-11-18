"""Conexión con el modelo de lenguaje (LLM).

Etapa 0. Usa la librería openai porque Gemini y OpenRouter aceptan su formato:
el mismo código sirve para los dos, solo cambia la configuración del .env.
"""
from openai import OpenAI

import config

# Segundos máximos de espera por respuesta: así una llamada nunca queda colgada
# y la regla de los 8 minutos se puede cumplir (plan, "Cómo funciona cada regla").
# Sin reintentos automáticos: la librería reintenta 2 veces por defecto, y una llamada
# podría tardar hasta 3 veces el límite. Si falla, quien llama decide qué hacer.
ESPERA_MAXIMA = 60


def preguntar_al_modelo(mensajes):
    """Envía la conversación al modelo y devuelve el texto de su respuesta.

    Curso: el modelo es la pieza con que el agente razona, pero qué puede hacer
    lo fijan su identidad y sus instrucciones (Módulo 2, secciones 2.2 y 2.5).
    """
    # El cliente se crea aquí y no al importar el archivo: así, si falta la clave,
    # el programa alcanza a mostrar su propio aviso en vez de un error de la librería.
    cliente = OpenAI(base_url=config.LLM_BASE_URL, api_key=config.LLM_API_KEY, timeout=ESPERA_MAXIMA, max_retries=0)
    respuesta = cliente.chat.completions.create(model=config.LLM_MODEL, messages=mensajes)
    # Si el proveedor bloquea la respuesta, el contenido llega vacío (None).
    return respuesta.choices[0].message.content or ""
