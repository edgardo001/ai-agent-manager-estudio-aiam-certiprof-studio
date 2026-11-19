"""Script de asistencia, etapa 5: lista los modelos que ofrece cada proveedor hoy, para mantener al
día la lista comentada de example.env (pedido del usuario, 2026-11-19).

Uso, desde la carpeta src/backend:  python -m scripts.listar_modelos
- Gemini: los modelos de la cuenta, pedidos con la clave del .env (la clave nunca se muestra).
- OpenRouter: los gratuitos (terminan en :free) que aceptan herramientas, de su lista pública, sin clave.
- Ollama: los modelos descargados en el equipo, si Ollama está corriendo.
No cuesta nada: pedir la lista de modelos no llama a ningún modelo. Que un modelo aparezca no prueba
que sirva para el agente: eso lo comprueba python -m scripts.prueba_conexion.
"""
import json
import urllib.request

from openai import OpenAI

from aplicacion import config


def listar(proveedor):
    """Devuelve los nombres de los modelos de un proveedor que habla el formato de OpenAI, tal como
    se escriben en LLM_MODEL. Técnico: no viene del curso."""
    direccion, clave = config.datos_del_proveedor(proveedor)
    cliente = OpenAI(base_url=direccion, api_key=clave, timeout=30, max_retries=0)
    return sorted(modelo.id.removeprefix("models/") for modelo in cliente.models.list())


def gratuitos_de_openrouter():
    """Devuelve (nombre, contexto) de los modelos gratuitos de OpenRouter que aceptan herramientas,
    de su lista pública. Técnico: no viene del curso (docs/modelos-y-costos.md, sección 2)."""
    with urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=30) as respuesta:
        modelos = json.load(respuesta)["data"]
    return sorted((m["id"], m.get("context_length")) for m in modelos
                  if m["id"].endswith(":free") and "tools" in (m.get("supported_parameters") or []))


def listar_modelos():
    """Muestra las tres listas. Si una falla, dice por qué en una línea y sigue con la siguiente;
    solo muestra el tipo de error, para no repetir nada de la configuración. Técnico: no viene del curso."""
    print("Gemini (clave de Google AI Studio):")
    if not config.GEMINI_API_KEY:
        print("  sin GEMINI_API_KEY en el .env")
    else:
        try:
            for nombre in listar("gemini"):
                print(f"  {nombre}")
        except Exception as error:  # sin red, clave inválida o límite de uso
            print(f"  no se pudo leer la lista ({type(error).__name__})")

    print("\nOpenRouter, gratuitos que aceptan herramientas (50 pedidos al día):")
    try:
        for nombre, contexto in gratuitos_de_openrouter():
            print(f"  {nombre}  (contexto de {contexto} tokens)")
    except Exception as error:
        print(f"  no se pudo leer la lista ({type(error).__name__})")

    print("\nOllama, en este equipo:")
    try:
        for nombre in listar("ollama"):
            print(f"  {nombre}")
    except Exception:
        print("  Ollama no está corriendo (o no está instalado)")


if __name__ == "__main__":
    listar_modelos()
