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


# Modelo de lenguaje. Gemini y OpenRouter usan el mismo formato, así que
# cambiar de proveedor es cambiar estos valores en el .env.
LLM_BASE_URL = leer("LLM_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
LLM_API_KEY = leer("LLM_API_KEY")
LLM_MODEL = leer("LLM_MODEL")
# Modelo de embeddings para la base de conocimiento (etapa 2). Usa la misma URL y clave.
LLM_MODELO_EMBEDDINGS = leer("LLM_MODELO_EMBEDDINGS", "gemini-embedding-001")

# Base de datos (etapa 2). POSTGRES_HOST es "localhost" desde la terminal (start-dev.bat)
# y "postgres" dentro de Docker (start-qa.bat, etapa 6).
POSTGRES_USER = leer("POSTGRES_USER", "agente")
POSTGRES_PASSWORD = leer("POSTGRES_PASSWORD")
POSTGRES_DB = leer("POSTGRES_DB", "agente")
POSTGRES_HOST = leer("POSTGRES_HOST", "localhost")

# Instrucciones del agente (JD+SOP). Está aquí para que la consola, la API y los scripts
# lean el mismo archivo sin depender unos de otros.
RUTA_PROMPT = Path(__file__).with_name("prompt_soporte_n1.md")

# Datos para estimar y calcular costos (scripts/estimar_costos.py; tickets desde la etapa 3).
# No configuran el modelo: son precios y supuestos. Detalle en docs/costos.md.
PRECIO_MILLON_TOKENS_ENTRADA = float(leer("PRECIO_MILLON_TOKENS_ENTRADA", "0.25"))
PRECIO_MILLON_TOKENS_SALIDA = float(leer("PRECIO_MILLON_TOKENS_SALIDA", "1.50"))
PRECIO_MILLON_TOKENS_EMBEDDINGS = float(leer("PRECIO_MILLON_TOKENS_EMBEDDINGS", "0.15"))
LLAMADAS_POR_CONSULTA = int(leer("LLAMADAS_POR_CONSULTA", "3"))
LIMITE_LLAMADAS_POR_MINUTO = float(leer("LIMITE_LLAMADAS_POR_MINUTO", "0"))  # 0: no anotado


def faltan_variables(con_base_de_datos=False):
    """Devuelve la lista de variables obligatorias que no están en el .env.
    Con con_base_de_datos=True revisa también la contraseña de PostgreSQL.
    Técnico: no viene del curso."""
    obligatorias = {"LLM_API_KEY": LLM_API_KEY, "LLM_MODEL": LLM_MODEL}
    if con_base_de_datos:
        obligatorias["POSTGRES_PASSWORD"] = POSTGRES_PASSWORD
    return [nombre for nombre, valor in obligatorias.items() if not valor]
