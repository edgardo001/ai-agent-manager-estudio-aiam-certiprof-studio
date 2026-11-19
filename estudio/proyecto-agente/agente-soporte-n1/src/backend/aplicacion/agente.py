"""El Agente de Soporte N1: atiende cada mensaje de un ticket con el modelo y sus tres herramientas.

Etapa 3. Es la única versión del agente: la consola y, desde la etapa 6, la API llaman a
atender_mensaje() (decisión D6). El bucle es corto y con límites: el modelo decide qué
herramienta usar; el código controla cuántas vueltas, cuántos tokens y qué herramientas
existen (buenas-practicas.md: "el modelo decide lo que requiere razonamiento; el código
controla lo que requiere garantías").
Todo lo de un mensaje viaja en un diccionario, el "turno", para que anotar() y escalar()
sean el único lugar donde, desde la etapa 4, cada paso se guarda en el registro de auditoría.
En la etapa 4 se suman también las reglas en código (8 minutos, cancelación) y el kill switch.
"""
import time

from aplicacion import config, herramientas
from aplicacion.base_de_datos import (
    guardar_mensaje,
    guardar_respuesta,
    leer_agente,
    leer_mensajes,
    leer_ticket,
    sumar_tokens,
)
from aplicacion.modelo import calcular_costo, conversar_con_herramientas

# Máximo de llamadas al modelo por cada mensaje del cliente. Un caso normal usa 3:
# buscar al cliente, buscar la solución y responder. Si se acaban, el ticket se escala.
MAXIMO_LLAMADAS_POR_MENSAJE = 6

MENSAJE_YA_ESCALADO = "Su caso ya está con una persona de nuestro equipo, que le responderá pronto."


def leer_version_prompt(prompt):
    """Devuelve el número de versión de la primera línea del prompt ("Versión del prompt: 3" da "3").
    Desde la etapa 4 se guarda en cada paso de la auditoría; en la etapa 5, en la aprobación.

    Curso: cada versión de las instrucciones se valida y se aprueba (Módulo 2, sección 2.6).
    """
    primera_linea = prompt.splitlines()[0] if prompt else ""
    return primera_linea.split(":", 1)[1].strip() if ":" in primera_linea else "sin versión"


def armar_instrucciones(prompt, agente):
    """Agrega al prompt lo que el agente no atiende, tomado del registro de agentes,
    que es la única fuente de esa lista (así no se repite en dos lugares).

    Curso: instrucciones con el rigor de un job description más un SOP (Módulo 2, sección 2.5)
    y el alcance, con lo que queda fuera (sección 2.2), guardado en el registro de agentes (2.7).
    """
    return (f"{prompt}\n\n# Lo que no atiendes (del registro de agentes)\n"
            f"{agente['fuera_de_alcance']}.\nSi el caso es de esta lista, escala.")


def armar_conversacion(instrucciones, mensajes):
    """Arma la lista de mensajes para el modelo: las instrucciones y la conversación del ticket.
    Lo que escribe el cliente va marcado como datos.

    Curso: el agente sigue sus instrucciones, no las que aparezcan dentro de los datos
    (Módulo 2, sección 2.6, dimensión adversarial).
    """
    conversacion = [{"role": "system", "content": instrucciones}]
    for quien, texto in mensajes:
        if quien == "cliente":
            conversacion.append({"role": "user", "content": herramientas.marcar_como_datos("mensaje_del_cliente", texto)})
        elif quien == "persona":  # hoy no ocurre: un ticket escalado no vuelve al agente
            conversacion.append({"role": "assistant", "content": f"(Respondió una persona del equipo) {texto}"})
        else:
            conversacion.append({"role": "assistant", "content": texto})
    return conversacion


def anotar(turno, tipo, detalle, **datos):
    """Guarda un paso del agente y, si la consola lo pidió, se lo muestra al momento.
    tipo es uno de los del registro de auditoría: 'modelo', 'herramienta' o 'regla'.
    Desde la etapa 4, este es el único lugar que llama a registrar_paso().

    Curso: poder explicar qué hizo el agente y por qué (Módulo 1, pregunta 9, audit trail).
    """
    paso = {"tipo": tipo, "detalle": detalle, **datos}
    turno["pasos"].append(paso)
    if turno["al_paso"]:
        turno["al_paso"](paso)


def escalar(turno, motivo, resumen, escalado_por):
    """Pasa el ticket a una persona, anota el paso y devuelve el resultado del mensaje.
    escalado_por es 'modelo' (usó la herramienta) o 'regla' (lo decidió el código).

    Curso: protocolo de escalamiento con contexto completo (Módulo 2, sección 2.5).
    """
    mensaje = herramientas.escalar_a_humano(turno["conexion"], turno["ticket"], motivo, resumen,
                                            escalado_por, turno["usadas"])
    tipo = "herramienta" if escalado_por == "modelo" else "regla"
    anotar(turno, tipo, f"escalar_a_humano: {motivo}")
    return {"estado": "escalado", "respuesta": mensaje, "pasos": turno["pasos"]}


def usar_herramienta(turno, nombre, argumentos):
    """Ejecuta buscar_cliente o buscar_solucion, anota el paso y devuelve el texto para el modelo.

    Curso: el agente usa solo sus herramientas y solo con el cliente del ticket
    (permisos mínimos, Módulo 2, sección 2.3).
    """
    if nombre == "buscar_cliente":
        resultado = herramientas.buscar_cliente(turno["conexion"], turno["ticket"])
        turno["usadas"].append("buscar_cliente")
        anotar(turno, "herramienta", "buscar_cliente")
        return resultado
    inicio = time.monotonic()
    resultado, fragmentos = herramientas.buscar_solucion(turno["conexion"], argumentos["consulta"])
    turno["usadas"].append(f"buscar_solucion(\"{argumentos['consulta']}\")")
    anotar(turno, "herramienta", f"buscar_solucion(\"{argumentos['consulta']}\")",
           fragmentos=[(documento, seccion, similitud) for documento, seccion, _, similitud in fragmentos],
           segundos=time.monotonic() - inicio)
    return resultado


def atender_mensaje(conexion, ticket_id, texto, al_paso=None):
    """Atiende un mensaje del cliente: lo guarda, conversa con el modelo y ejecuta las
    herramientas que pida, hasta que responde o escala.
    Devuelve {"estado": "respondido" o "escalado", "respuesta": texto para el cliente, "pasos": [...]}.
    No confirma los cambios en la base: lo hace quien llama (decisión D11).
    al_paso: función opcional que recibe cada paso al momento (el modo detallado de la consola).

    Curso: el proceso del SOP, paso a paso (Módulo 2, sección 2.5), con un agente de
    Nivel 3 que combina herramientas para completar un objetivo de varios pasos (sección 1.2).
    """
    ticket = leer_ticket(conexion, ticket_id)
    if ticket is None:
        raise ValueError(f"El ticket {ticket_id} no existe.")
    guardar_mensaje(conexion, ticket_id, "cliente", texto)
    if ticket["estado"] == "escalado":  # una persona ya lo atiende: el agente no vuelve a intervenir
        guardar_mensaje(conexion, ticket_id, "agente", MENSAJE_YA_ESCALADO)
        return {"estado": "escalado", "respuesta": MENSAJE_YA_ESCALADO, "pasos": []}

    agente = leer_agente(conexion)
    if agente is None:
        raise ValueError("El Agente de Soporte N1 no está en el registro de agentes: revise 02_datos_ficticios.sql.")
    prompt = config.RUTA_PROMPT.read_text(encoding="utf-8")
    turno = {"conexion": conexion, "ticket": ticket, "agente": agente, "version_prompt": leer_version_prompt(prompt),
             "pasos": [], "usadas": [], "al_paso": al_paso}
    conversacion = armar_conversacion(armar_instrucciones(prompt, agente), leer_mensajes(conexion, ticket_id))
    tokens_del_ticket = ticket["tokens_entrada"] + ticket["tokens_salida"]
    tope = config.TOPE_TOKENS_POR_TICKET

    for vuelta in range(1, MAXIMO_LLAMADAS_POR_MENSAJE + 1):
        if tokens_del_ticket >= tope:  # el ticket llegó (o quedó) pasado del tope: no se llama más al modelo
            return escalar(turno, f"el ticket superó el tope de {tope} tokens", "", "regla")
        inicio = time.monotonic()
        try:
            llamada = conversar_con_herramientas(conversacion, herramientas.DEFINICIONES)
        except Exception as error:  # sin red, clave inválida, límite de uso, 60 segundos sin respuesta...
            return escalar(turno, f"no se pudo hablar con el modelo ({error})", "", "regla")
        entrada, salida = llamada["tokens_entrada"], llamada["tokens_salida"]
        costo = calcular_costo(entrada, salida)
        sumar_tokens(conexion, ticket_id, entrada, salida, costo)
        tokens_del_ticket += entrada + salida
        anotar(turno, "modelo", "pide herramientas" if llamada["llamadas"] else "responde",
               tokens_entrada=entrada, tokens_salida=salida, costo=costo, segundos=time.monotonic() - inicio)

        if not llamada["llamadas"]:  # el modelo respondió al cliente
            if llamada["fin"] not in ("stop", None):  # cortada por largo o bloqueada por un filtro
                return escalar(turno, f"la respuesta del modelo llegó incompleta ({llamada['fin']})", "", "regla")
            if not llamada["texto"].strip():  # el proveedor bloqueó la respuesta o llegó vacía
                return escalar(turno, "el modelo no devolvió una respuesta", "", "regla")
            guardar_mensaje(conexion, ticket_id, "agente", llamada["texto"])
            guardar_respuesta(conexion, ticket_id, llamada["texto"])
            return {"estado": "respondido", "respuesta": llamada["texto"], "pasos": turno["pasos"]}

        # El modelo pidió herramientas. Si superó el tope o es la última vuelta, no se ejecutan:
        # nadie usaría su resultado.
        if tokens_del_ticket >= tope:
            return escalar(turno, f"el ticket superó el tope de {tope} tokens", "", "regla")
        if vuelta == MAXIMO_LLAMADAS_POR_MENSAJE:
            break
        # Un pedido válido de escalar se atiende primero, sin pagar antes las otras herramientas.
        for _, nombre, argumentos_json in llamada["llamadas"]:
            argumentos, error = herramientas.leer_argumentos(nombre, argumentos_json)
            if nombre == "escalar_a_humano" and not error:
                turno["usadas"].append("escalar_a_humano")
                return escalar(turno, argumentos["motivo"], argumentos["resumen"], "modelo")

        # Su mensaje se agrega tal cual (con la firma de Gemini, D11) y cada pedido recibe su resultado.
        conversacion.append(llamada["mensaje"])
        for llamada_id, nombre, argumentos_json in llamada["llamadas"]:
            argumentos, error = herramientas.leer_argumentos(nombre, argumentos_json)
            if error:
                resultado = error
                anotar(turno, "herramienta", f"rechazada: {error}")
            else:
                try:
                    resultado = usar_herramienta(turno, nombre, argumentos)
                except Exception as falla:  # sin red en el embedding, base caída...
                    return escalar(turno, f"la herramienta {nombre} falló ({falla})", "", "regla")
            conversacion.append({"role": "tool", "tool_call_id": llamada_id, "content": resultado})

    return escalar(turno, f"el agente no terminó en {MAXIMO_LLAMADAS_POR_MENSAJE} llamadas al modelo", "", "regla")
