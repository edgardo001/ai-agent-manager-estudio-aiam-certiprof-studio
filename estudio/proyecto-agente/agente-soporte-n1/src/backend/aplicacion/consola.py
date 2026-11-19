"""Etapa 1: conversar con el Agente de Soporte N1 en la terminal.

Uso, desde la carpeta src/backend:  python -m aplicacion.consola
El agente todavía no tiene herramientas ni base de conocimiento: solo su
identidad e instrucciones (JD+SOP). Sirve para ver cómo cambia su conducta
al editar prompt_soporte_n1.md, sin tocar el código.
"""
from aplicacion import config
from aplicacion.modelo import preguntar_al_modelo


def cargar_instrucciones():
    """Lee el system prompt del agente desde su archivo.

    Curso: instrucciones con el rigor de un job description más un SOP
    (Módulo 2, sección 2.5). El texto sale de la plantilla 05.
    """
    return config.RUTA_PROMPT.read_text(encoding="utf-8")


def conversar():
    """Lee lo que escribe la persona, lo envía al modelo junto con las instrucciones
    y muestra la respuesta. Guarda el historial para que el agente recuerde lo dicho.

    Curso: el agente opera literalmente según sus instrucciones; no completa con
    criterio propio lo que no se le dijo (Módulo 2, sección 2.4).
    """
    faltan = config.faltan_variables()
    if faltan:
        print(f"Faltan en src/docker/.env: {', '.join(faltan)}. Copie example.env como .env y complételo.")
        return
    mensajes = [{"role": "system", "content": cargar_instrucciones()}]
    print("Agente de Soporte N1. Escriba su consulta, o 'salir' para terminar.")
    while True:
        try:
            texto = input("\nCliente: ").strip()
        except (KeyboardInterrupt, EOFError):  # Ctrl+C o fin de la entrada: se sale sin error
            break
        if texto.lower() == "salir":
            break
        if not texto:
            continue
        mensajes.append({"role": "user", "content": texto})
        try:
            respuesta = preguntar_al_modelo(mensajes)
        except Exception as error:  # clave inválida, límite de uso, sin red...
            mensajes.pop()  # se quita la pregunta que no tuvo respuesta, para poder reintentar
            print(f"\n(No se pudo hablar con el modelo: {error}. Intente de nuevo.)")
            continue
        if respuesta:
            mensajes.append({"role": "assistant", "content": respuesta})
        print(f"\nAgente: {respuesta or '(el modelo no devolvió texto)'}")


if __name__ == "__main__":
    conversar()
