"""Configuración del agente: lee las variables del archivo .env.

Etapa 0, ampliado en la etapa 2 (base de datos y embeddings). Las claves nunca se
escriben en el código: viven en src/docker/.env, que no se sube al repositorio
(regla 5 del plan). Este archivo solo las lee y las deja disponibles para el resto.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Ruta al .env contando desde este archivo: src/backend/aplicacion/config.py -> src/docker/.env
# Desde la terminal se lee este archivo. Dentro de Docker (etapa 6) no se copia a la imagen
# (lo impide src/.dockerignore) y no pasa nada: el docker-compose.yml entrega las mismas
# variables con "env_file".
load_dotenv(Path(__file__).resolve().parents[2] / "docker" / ".env")


def leer(nombre, por_defecto=""):
    """Devuelve una variable del .env, o el valor por defecto si no está o está vacía.
    Técnico: no viene del curso."""
    return os.getenv(nombre) or por_defecto


# Proveedores de modelos (decisión D14). Gemini, OpenRouter y Ollama aceptan el mismo formato
# (el de OpenAI); cada uno tiene su dirección y su clave con nombre propio, las dos en el .env,
# para poder cambiar una dirección sin tocar el código. Cambiar de proveedor es cambiar
# LLM_PROVEEDOR en el .env, sin comentar ni descomentar líneas.
GEMINI_API_KEY = leer("GEMINI_API_KEY")
OPENROUTER_API_KEY = leer("OPENROUTER_API_KEY")
PROVEEDORES = {  # nombre: (dirección, variable con su clave; Ollama no pide clave)
    "gemini": (leer("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/"), "GEMINI_API_KEY"),
    "openrouter": (leer("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"), "OPENROUTER_API_KEY"),
    "ollama": (leer("OLLAMA_BASE_URL", "http://localhost:11434/v1"), None),
}


def datos_del_proveedor(nombre):
    """Devuelve (dirección, clave) de un proveedor, o (None, None) si no se conoce.
    Técnico: no viene del curso."""
    if nombre not in PROVEEDORES:
        return None, None
    direccion, variable = PROVEEDORES[nombre]
    # Ollama no pide clave, pero la librería openai exige un texto: cualquiera sirve.
    return direccion, globals()[variable] if variable else "ollama"


# Modelo de chat: el que conversa y usa las herramientas.
LLM_PROVEEDOR = leer("LLM_PROVEEDOR", "gemini").strip().lower()
LLM_BASE_URL, LLM_API_KEY = datos_del_proveedor(LLM_PROVEEDOR)
LLM_MODEL = leer("LLM_MODEL")
# Máximo de tokens que puede escribir el modelo en cada respuesta. El agente responde en menos
# de 300; sin tope, OpenRouter reserva saldo para la salida máxima del modelo (65.536) y con poco
# saldo rechaza el pedido (error 402, 2026-11-19). Holgado porque algunos modelos razonan antes.
LLM_MAXIMO_TOKENS_SALIDA = int(leer("LLM_MAXIMO_TOKENS_SALIDA", "2000"))
# Modelo de embeddings para la base de conocimiento (etapa 2). Tiene su propio proveedor
# (decisión D13): así se puede cambiar el chat sin recargar los vectores, que solo se comparan
# con los de su mismo modelo (D8). Vacío, usa el mismo proveedor del chat.
LLM_EMBEDDINGS_PROVEEDOR = leer("LLM_EMBEDDINGS_PROVEEDOR", LLM_PROVEEDOR).strip().lower()
LLM_EMBEDDINGS_BASE_URL, LLM_EMBEDDINGS_API_KEY = datos_del_proveedor(LLM_EMBEDDINGS_PROVEEDOR)
LLM_MODELO_EMBEDDINGS = leer("LLM_MODELO_EMBEDDINGS", "gemini-embedding-001")

# Base de datos (etapa 2). POSTGRES_HOST es "127.0.0.1" desde la terminal (start-dev.bat; no "localhost", D12)
# y "postgres" dentro de Docker (start-qa.bat, etapa 6).
POSTGRES_USER = leer("POSTGRES_USER", "agente")
POSTGRES_PASSWORD = leer("POSTGRES_PASSWORD")
POSTGRES_DB = leer("POSTGRES_DB", "agente")
POSTGRES_HOST = leer("POSTGRES_HOST", "127.0.0.1")

# Instrucciones del agente (JD+SOP). Está aquí para que la consola, la API y los scripts
# lean el mismo archivo sin depender unos de otros.
RUTA_PROMPT = Path(__file__).with_name("prompt_soporte_n1.md")

# Tope de tokens por ticket (etapa 3): si la conversación con el modelo lo supera, el ticket
# se escala. Evita que un caso enredado gaste sin límite (rag.md, patrón 08).
TOPE_TOKENS_POR_TICKET = int(leer("TOPE_TOKENS_POR_TICKET", "20000"))

# Datos para estimar y calcular costos (scripts/estimar_costos.py; tickets desde la etapa 3).
# No configuran el modelo: son precios y supuestos. Detalle en docs/modelos-y-costos.md.
PRECIO_MILLON_TOKENS_ENTRADA = float(leer("PRECIO_MILLON_TOKENS_ENTRADA", "0.25"))
PRECIO_MILLON_TOKENS_SALIDA = float(leer("PRECIO_MILLON_TOKENS_SALIDA", "1.50"))
PRECIO_MILLON_TOKENS_EMBEDDINGS = float(leer("PRECIO_MILLON_TOKENS_EMBEDDINGS", "0.15"))
LLAMADAS_POR_CONSULTA = int(leer("LLAMADAS_POR_CONSULTA", "3"))
LIMITE_LLAMADAS_POR_MINUTO = float(leer("LIMITE_LLAMADAS_POR_MINUTO", "0"))  # 0: no anotado


def faltan_variables(con_base_de_datos=False):
    """Devuelve la lista de variables obligatorias que faltan o están mal en el .env: un
    proveedor desconocido, la clave del proveedor del chat o de los embeddings, el modelo y,
    con con_base_de_datos=True, la contraseña de PostgreSQL.
    Técnico: no viene del curso."""
    faltan = []
    for variable_proveedor, proveedor in (("LLM_PROVEEDOR", LLM_PROVEEDOR),
                                          ("LLM_EMBEDDINGS_PROVEEDOR", LLM_EMBEDDINGS_PROVEEDOR)):
        if proveedor not in PROVEEDORES:
            faltan.append(f"{variable_proveedor} (use {', '.join(PROVEEDORES)})")
            continue
        variable_clave = PROVEEDORES[proveedor][1]
        if variable_clave and not globals()[variable_clave] and variable_clave not in faltan:
            faltan.append(variable_clave)
    if not LLM_MODEL:
        faltan.append("LLM_MODEL")
    if con_base_de_datos and not POSTGRES_PASSWORD:
        faltan.append("POSTGRES_PASSWORD")
    return faltan
