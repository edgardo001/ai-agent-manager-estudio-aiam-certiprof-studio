"""Script de asistencia, etapa 0, ampliado al cambiar de proveedor: comprueba que el proyecto
puede hablar con el modelo de chat, que ese modelo sabe usar herramientas y que el modelo de
embeddings entrega vectores del tamaño correcto.

Uso, desde la carpeta src/backend:  python -m scripts.prueba_conexion
Sirve cada vez que se cambia el proveedor o el modelo en el .env (docs/proveedores-de-modelos.md).
Cuesta una fracción de centavo: un saludo, un pedido de herramienta y un embedding.
"""
from aplicacion import config
from aplicacion.modelo import DIMENSIONES_EMBEDDING, conversar_con_herramientas, crear_embedding, preguntar_al_modelo

# Una herramienta inventada, solo para ver si el modelo sabe pedirla.
HERRAMIENTA_DE_PRUEBA = [{
    "type": "function",
    "function": {
        "name": "consultar_hora",
        "description": "Devuelve la hora actual de una ciudad.",
        "parameters": {"type": "object", "properties": {"ciudad": {"type": "string"}}, "required": ["ciudad"]},
    },
}]


def probar_conexion():
    """Prueba el chat, las herramientas y los embeddings, y dice qué funciona.

    Curso: todavía no hay agente; es la preparación técnica previa al onboarding agentic
    (Módulo 2, sección 2.1). Que el modelo sepa usar herramientas es requisito del agente
    de Nivel 3, que combina herramientas (sección 1.2).
    """
    faltan = config.faltan_variables()
    if faltan:
        print(f"Faltan en src/docker/.env: {', '.join(faltan)}. Copie example.env como .env y complételo.")
        return
    print(f"Chat: {config.LLM_MODEL} en {config.LLM_PROVEEDOR} ({config.LLM_BASE_URL})")
    try:
        print(f"  1. Saludo: {preguntar_al_modelo([{'role': 'user', 'content': 'Hola. Responde en una sola frase.'}])}")
        llamada = conversar_con_herramientas(
            [{"role": "user", "content": "¿Qué hora es en Santiago? Usa la herramienta."}], HERRAMIENTA_DE_PRUEBA)
        if llamada["llamadas"]:
            _, nombre, argumentos = llamada["llamadas"][0]
            print(f"  2. Herramientas: sí, pidió {nombre} con {argumentos}. Sirve para el agente.")
        else:
            print("  2. Herramientas: NO las usó (respondió con texto). Este modelo no sirve para el agente:"
                  " elija uno que acepte herramientas (tools).")
    except Exception as error:  # clave inválida, modelo inexistente, sin red...
        print(f"  El chat falló: {error}")
    print(f"Embeddings: {config.LLM_MODELO_EMBEDDINGS} en {config.LLM_EMBEDDINGS_PROVEEDOR} ({config.LLM_EMBEDDINGS_BASE_URL})")
    try:
        tamano = len(crear_embedding(["prueba"])[0])
        estado = "correcto" if tamano == DIMENSIONES_EMBEDDING else f"distinto de {DIMENSIONES_EMBEDDING}: no sirve con la base actual"
        print(f"  3. Vector de {tamano} números: {estado}.")
    except Exception as error:
        print(f"  Los embeddings fallaron: {error}")


if __name__ == "__main__":
    probar_conexion()
