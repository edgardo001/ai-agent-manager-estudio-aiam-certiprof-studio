"""Conversar con el Agente de Soporte N1 en la terminal.

Etapa 1, ampliada en la etapa 3: pide el código del cliente, crea un ticket y pasa cada
mensaje a agente.py, la misma función que usará la API (decisión D6). Necesita PostgreSQL
levantado y la base de conocimiento cargada.
Uso, desde la carpeta src/backend:
    python -m aplicacion.consola              conversación normal
    python -m aplicacion.consola --detallado  muestra cada paso: herramientas, fragmentos,
                                              parecido, tokens, costo y segundos
"""
import argparse

from aplicacion import config
from aplicacion.agente import atender_mensaje
from aplicacion.base_de_datos import conectar, contar_fragmentos, crear_ticket, leer_agente, leer_cliente, leer_ticket


def decimal(valor, decimales):
    """Escribe un número con coma decimal, como el resto del proyecto (0,000271).
    Técnico: no viene del curso."""
    return f"{float(valor):.{decimales}f}".replace(".", ",")


def mostrar_paso(paso):
    """Muestra un paso del agente en el modo detallado: es la consola como herramienta de estudio,
    para ver por dentro cómo trabaja el agente.
    Técnico: no viene del curso (buenas-practicas.md)."""
    if paso["tipo"] == "modelo":
        print(f"  [modelo] {paso['detalle']}: {paso['tokens_entrada']} tokens de entrada, {paso['tokens_salida']} de salida,"
              f" {decimal(paso['costo'], 6)} dólares, {decimal(paso['segundos'], 1)} s")
    else:
        print(f"  [{paso['tipo']}] {paso['detalle']}")
    for documento, seccion, similitud in paso.get("fragmentos", []):
        print(f"      {decimal(similitud, 2)}  {documento} > {seccion}")


def pedir_cliente(conexion):
    """Pide el código del cliente hasta que exista en el CRM. Devuelve el cliente, o None para salir.

    Curso: el cliente sale del ticket, no del modelo (Módulo 2, sección 2.3, permisos mínimos).
    """
    while True:
        try:
            codigo = input("\nCódigo del cliente (C-001 a C-006), o 'salir': ").strip().upper()
        except (KeyboardInterrupt, EOFError):
            return None
        if codigo in ("SALIR", ""):
            return None
        cliente = leer_cliente(conexion, codigo=codigo)
        if cliente:
            print(f"Cliente: {cliente['nombre']}, {cliente['empresa']}, plan {cliente['plan']}.")
            return cliente
        print("Ese código no existe en el CRM.")


def atender_ticket(conexion, agente, cliente, detallado):
    """Conversa sobre un ticket hasta que el cliente sale o el ticket pasa a una persona.
    Confirma los cambios en la base después de cada mensaje (decisión D11).
    Devuelve False si la persona quiere terminar la consola.

    Curso: el agente atiende el ticket según su SOP (Módulo 2, sección 2.5).
    """
    ticket_id = None
    print("Escriba su consulta. 'nuevo' empieza otro ticket; 'salir' termina.")
    while True:
        try:
            texto = input("\nCliente: ").strip()
        except (KeyboardInterrupt, EOFError):  # Ctrl+C o fin de la entrada: se sale sin error
            return False
        if texto.lower() in ("salir", "nuevo"):
            return texto.lower() == "nuevo"
        if not texto:
            continue
        ticket_nuevo = ticket_id is None
        try:
            if ticket_nuevo:
                ticket_id = crear_ticket(conexion, agente["id"], cliente["id"], texto)
                print(f"(ticket {ticket_id})")
            resultado = atender_mensaje(conexion, ticket_id, texto, mostrar_paso if detallado else None)
            conexion.commit()
        except Exception as error:  # la base se cayó a mitad, por ejemplo
            conexion.rollback()
            if ticket_nuevo:  # el rollback también borró el ticket: el próximo mensaje crea otro
                ticket_id = None
            print(f"\n(No se pudo atender el mensaje: {error}. Intente de nuevo.)")
            continue
        print(f"\nAgente: {resultado['respuesta']}")
        if detallado:
            ticket = leer_ticket(conexion, ticket_id)
            print(f"  [ticket {ticket_id}] estado {ticket['estado']}, {ticket['tokens_entrada']} tokens de entrada y"
                  f" {ticket['tokens_salida']} de salida en total, {decimal(ticket['costo_tokens'], 6)} dólares")
        if resultado["estado"] == "escalado":
            print(f"\n(El ticket {ticket_id} pasó a una persona. Empieza un ticket nuevo.)")
            return True


def conversar():
    """Prepara la conexión, revisa que la base de conocimiento esté cargada y atiende tickets uno tras otro.
    Técnico: no viene del curso."""
    parser = argparse.ArgumentParser(description="Conversar con el Agente de Soporte N1.")
    parser.add_argument("--detallado", action="store_true", help="muestra cada paso del agente")
    detallado = parser.parse_args().detallado

    faltan = config.faltan_variables(con_base_de_datos=True)
    if faltan:
        print(f"Faltan en src/docker/.env: {', '.join(faltan)}. Copie example.env como .env y complételo.")
        return
    try:
        conexion = conectar()
    except Exception as error:  # PostgreSQL apagado, contraseña equivocada...
        print(f"No se pudo conectar con PostgreSQL ({error}). ¿Está abierto Docker y se ejecutó start-dev.bat?")
        return
    try:
        if contar_fragmentos(conexion) == 0:
            print(f"La base no tiene fragmentos del modelo {config.LLM_MODELO_EMBEDDINGS}: "
                  "ejecute python -m scripts.cargar_conocimiento desde src/backend.")
            return
        agente = leer_agente(conexion)
        if agente is None:
            print("El Agente de Soporte N1 no está en el registro de agentes: revise 02_datos_ficticios.sql.")
            return
        print(f"{agente['nombre']}." + (" Modo detallado." if detallado else ""))
        while True:
            cliente = pedir_cliente(conexion)
            if cliente is None or not atender_ticket(conexion, agente, cliente, detallado):
                break
    finally:
        conexion.close()


if __name__ == "__main__":
    conversar()
