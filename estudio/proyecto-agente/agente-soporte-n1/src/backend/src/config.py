"""Configuración del agente: lee las variables del archivo .env.

Etapa 0. Las claves nunca se escriben en el código: viven en src/docker/.env,
que no se sube al repositorio (regla 5 del plan). Este archivo solo las lee
y las deja disponibles para el resto del programa.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Ruta al .env contando desde este archivo: src/backend/src/config.py -> src/docker/.env
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


def faltan_variables():
    """Devuelve la lista de variables obligatorias que no están en el .env.
    Técnico: no viene del curso."""
    obligatorias = {"LLM_API_KEY": LLM_API_KEY, "LLM_MODEL": LLM_MODEL}
    return [nombre for nombre, valor in obligatorias.items() if not valor]
