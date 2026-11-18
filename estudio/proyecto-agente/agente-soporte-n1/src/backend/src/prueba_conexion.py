"""Etapa 0: comprueba que el proyecto puede hablar con el modelo.

Uso, desde la carpeta src/backend:  python src/prueba_conexion.py
Si el modelo responde, la clave y el nombre del modelo del .env están bien.
"""
import config
from modelo import preguntar_al_modelo


def probar_conexion():
    """Manda un saludo al modelo y muestra la respuesta.

    Curso: todavía no hay agente; es la preparación técnica previa al
    onboarding agentic (Módulo 2, sección 2.1).
    """
    faltan = config.faltan_variables()
    if faltan:
        print(f"Faltan en src/docker/.env: {', '.join(faltan)}. Copie example.env como .env y complételo.")
        return
    print(preguntar_al_modelo([{"role": "user", "content": "Hola. Responde en una sola frase."}]))


if __name__ == "__main__":
    probar_conexion()
