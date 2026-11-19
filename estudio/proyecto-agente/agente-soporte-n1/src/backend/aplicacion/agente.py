"""El Agente de Soporte N1: atiende cada mensaje de un ticket con el modelo y sus tres herramientas.

Etapa 3. Es la única versión del agente: la consola y, desde la etapa 6, la API llaman a
atender_mensaje() (decisión D6). El bucle es corto y con límites: el modelo decide qué
herramienta usar; el código controla cuántas vueltas, cuántos tokens y qué herramientas
existen (rag.md: "el modelo decide lo que requiere razonamiento; el código
controla lo que requiere garantías").
Todo lo de un mensaje viaja en un diccionario, el "turno", y anotar() registra en la auditoría
cada paso de un ticket (etapa 4), con la versión y la huella de las instrucciones (D15); las
intervenciones humanas, como detener el agente, las registra reglas.py. Las reglas que no pueden depender del modelo
(kill switch, 8 minutos, cancelación, lo que una respuesta no puede decir) están en reglas.py.
"""
import hashlib
import time

from aplicacion import config, herramientas, reglas
from aplicacion.base_de_datos import (
    crear_punto_de_retorno,
    guardar_mensaje,
    guardar_respuesta,
    leer_agente,
    leer_cliente,
    leer_mensajes,
    leer_ticket,
    registrar_paso,
    sumar_tokens,
    ultimo_paso,
    volver_al_punto_de_retorno,
)
from aplicacion.modelo import calcular_costo, conversar_con_herramientas

# Máximo de llamadas al modelo por cada mensaje del cliente. Un caso normal usa 3:
# buscar al cliente, buscar la solución y responder. Si se acaban, el ticket se escala.
MAXIMO_LLAMADAS_POR_MENSAJE = 6

MENSAJE_YA_ESCALADO = "Su caso ya está con una persona de nuestro equipo, que le responderá pronto."


def leer_version_prompt(prompt):
    """Devuelve el número de versión de la primera línea del prompt ("Versión del prompt: 3" da "3").
    Desde la etapa 4 se guarda en cada paso de la auditoría; en la etapa 5, en la aprobación.

    Curso: validación antes de producción (Módulo 2, sección 2.6). Identificar la versión exacta de
    las instrucciones es decisión del proyecto (D15).
    """
    primera_linea = prompt.splitlines()[0] if prompt else ""
    return primera_linea.split(":", 1)[1].strip() if ":" in primera_linea else "sin versión"


def huella_de(texto):
    """Devuelve la huella SHA-256 de un texto: cambia si cambia una sola letra.

    Curso: validación antes de producción (Módulo 2, sección 2.6) y registro con la fecha de la
    última validación (sección 2.7). Identificar con una huella qué instrucciones exactas atendieron
    cada caso es decisión del proyecto (D15).
    """
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


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
        # Un ticket escalado no vuelve al agente, así que aquí solo hay mensajes del cliente y del agente.
        if quien == "cliente":
            conversacion.append({"role": "user", "content": herramientas.marcar_como_datos("mensaje_del_cliente", texto)})
        else:
            conversacion.append({"role": "assistant", "content": texto})
    return conversacion


def anotar(turno, tipo, detalle, motivo=None, tokens=None, **datos):
    """Guarda un paso del agente en el registro de auditoría y, si la consola lo pidió, se lo
    muestra al momento. tipo es 'modelo', 'herramienta' o 'regla'. Cada paso lleva su número dentro
    del ticket, la versión y la huella de las instrucciones (D15) y, si llamó al modelo, el proveedor
    y el modelo.

    Curso: poder explicar qué hizo el agente y por qué en cada caso (Módulo 1, pregunta 9, audit trail).
    """
    turno["numero_paso"] += 1
    paso = {"tipo": tipo, "detalle": detalle, **datos}
    turno["pasos"].append(paso)
    datos_usados = {**datos, "huella_instrucciones": turno["huella"]}
    if tipo == "modelo":  # solo los pasos que llamaron al modelo dicen cuál fue
        datos_usados.update(proveedor=config.LLM_PROVEEDOR, modelo=config.LLM_MODEL)
    registrar_paso(turno["conexion"], turno["agente"]["id"], turno["ticket"]["id"], turno["numero_paso"], tipo,
                   detalle, datos_usados, motivo, turno["version_prompt"], tokens, None)
    if turno["al_paso"]:
        turno["al_paso"](paso)


def escalar(turno, motivo, resumen, escalado_por, **datos):
    """Pasa el ticket a una persona, anota el paso y devuelve el resultado del mensaje.
    escalado_por es 'modelo' (usó la herramienta) o 'regla' (lo decidió el código). datos va a la
    auditoría, por ejemplo el texto de una respuesta bloqueada.

    Curso: protocolo de escalamiento con contexto completo (Módulo 2, sección 2.5).
    """
    mensaje = herramientas.escalar_a_humano(turno["conexion"], turno["ticket"], motivo, resumen,
                                            escalado_por, turno["usadas"])
    tipo = "herramienta" if escalado_por == "modelo" else "regla"
    anotar(turno, tipo, f"escalar_a_humano: {motivo}", motivo=motivo, **datos)
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
    if nombre != "buscar_solucion":  # una herramienta nueva necesita su propia rama aquí
        raise ValueError(f"usar_herramienta no sabe ejecutar {nombre}")
    inicio = time.monotonic()
    resultado, fragmentos = herramientas.buscar_solucion(turno["conexion"], argumentos["consulta"])
    turno["usadas"].append(f"buscar_solucion(\"{argumentos['consulta']}\")")
    anotar(turno, "herramienta", f"buscar_solucion(\"{argumentos['consulta']}\")",
           fragmentos=[(documento, seccion, round(similitud, 4), huella[:12])
                       for documento, seccion, _, similitud, huella in fragmentos],
           segundos=time.monotonic() - inicio)
    return resultado


def atender_mensaje(conexion, ticket_id, texto, al_paso=None, mensaje_ya_guardado=False):
    """Atiende un mensaje del cliente: lo guarda, conversa con el modelo y ejecuta las
    herramientas que pida, hasta que responde o escala.
    Devuelve {"estado": "respondido" o "escalado", "respuesta": texto para el cliente, "pasos": [...]}.
    No confirma los cambios en la base: lo hace quien llama (decisión D11).
    al_paso: función opcional que recibe cada paso al momento (el modo detallado de la consola).
    mensaje_ya_guardado: True si quien llama ya guardó y confirmó el mensaje del cliente, para que no
    se pierda si el proceso se cae a mitad; escalar_vencidos() lo rescata después (D11).

    Curso: el proceso del SOP, paso a paso (Módulo 2, sección 2.5), con un agente de
    Nivel 3 que combina herramientas para completar un objetivo de varios pasos (sección 1.2).
    """
    inicio_del_mensaje = time.monotonic()  # los 8 minutos se cuentan por mensaje (plan)
    ticket = leer_ticket(conexion, ticket_id)
    if ticket is None:
        raise ValueError(f"El ticket {ticket_id} no existe.")
    if not mensaje_ya_guardado:
        guardar_mensaje(conexion, ticket_id, "cliente", texto)
    agente = leer_agente(conexion)
    if agente is None:
        raise ValueError("El Agente de Soporte N1 no está en el registro de agentes: revise 02_datos_ficticios.sql.")
    turno = {"conexion": conexion, "ticket": ticket, "agente": agente, "version_prompt": None, "huella": None,
             "numero_paso": ultimo_paso(conexion, ticket_id), "pasos": [], "usadas": [], "al_paso": al_paso}
    if ticket["estado"] == "escalado":  # una persona ya lo atiende: el agente no vuelve a intervenir
        guardar_mensaje(conexion, ticket_id, "agente", MENSAJE_YA_ESCALADO)
        anotar(turno, "regla", "ticket ya escalado: el mensaje queda para la persona")
        return {"estado": "escalado", "respuesta": MENSAJE_YA_ESCALADO, "pasos": turno["pasos"]}

    # Las instrucciones se leen primero, para que todo paso lleve su versión y su huella (D15).
    try:
        prompt = config.RUTA_PROMPT.read_text(encoding="utf-8")
    except OSError:  # el archivo de instrucciones no está: sin instrucciones, el agente no atiende
        return escalar(turno, "falta el archivo de instrucciones del agente", "", "regla")
    instrucciones = armar_instrucciones(prompt, agente)
    turno["version_prompt"], turno["huella"] = leer_version_prompt(prompt), huella_de(instrucciones)

    # Reglas que se revisan antes de llamar al modelo (reglas.py).
    if reglas.agente_detenido(agente):
        return escalar(turno, f"agente detenido ({agente['motivo_detencion'] or 'sin motivo anotado'})", "", "regla")
    motivo = reglas.revisar_entrada(texto)
    if motivo:
        return escalar(turno, motivo, "", "regla")
    codigo_cliente = leer_cliente(conexion, cliente_id=ticket["cliente_id"])["codigo"]
    conversacion = armar_conversacion(instrucciones, leer_mensajes(conexion, ticket_id))
    tokens_del_ticket = ticket["tokens_entrada"] + ticket["tokens_salida"]
    tope = config.TOPE_TOKENS_POR_TICKET

    for vuelta in range(1, MAXIMO_LLAMADAS_POR_MENSAJE + 1):
        # Antes de cada llamada al modelo: el kill switch (alguien pudo detener el agente a mitad)
        # y los 8 minutos.
        if vuelta > 1:
            agente_ahora = leer_agente(conexion)
            if reglas.agente_detenido(agente_ahora):
                return escalar(turno, f"agente detenido ({agente_ahora['motivo_detencion'] or 'sin motivo anotado'})",
                               "", "regla")
        if reglas.tiempo_excedido(inicio_del_mensaje):
            return escalar(turno, f"la atención superó {config.MINUTOS_MAXIMOS_ANTES_DE_ESCALAR:g} minutos", "", "regla")
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
        anotar(turno, "modelo", "pide herramientas" if llamada["llamadas"] else "responde", tokens=entrada + salida,
               tokens_entrada=entrada, tokens_salida=salida, costo=costo, segundos=round(time.monotonic() - inicio, 2))

        if not llamada["llamadas"]:  # el modelo respondió al cliente
            if llamada["fin"] not in ("stop", None):  # cortada por largo o bloqueada por un filtro
                return escalar(turno, f"la respuesta del modelo llegó incompleta ({llamada['fin']})", "", "regla")
            if not llamada["texto"].strip():  # el proveedor bloqueó la respuesta o llegó vacía
                return escalar(turno, "el modelo no devolvió una respuesta", "", "regla")
            motivo = reglas.revisar_respuesta(llamada["texto"], codigo_cliente)
            if motivo:  # la respuesta no se envía; sin reintentos (rag.md). Su texto queda en la auditoría
                return escalar(turno, f"respuesta bloqueada: {motivo}", "", "regla", texto_bloqueado=llamada["texto"])
            guardar_mensaje(conexion, ticket_id, "agente", llamada["texto"])
            guardar_respuesta(conexion, ticket_id, llamada["texto"])
            return {"estado": "respondido", "respuesta": llamada["texto"], "pasos": turno["pasos"]}

        # El modelo pidió herramientas: cada pedido se revisa una sola vez.
        pedidos = [(llamada_id, nombre, *herramientas.leer_argumentos(nombre, argumentos_json))
                   for llamada_id, nombre, argumentos_json in llamada["llamadas"]]
        # Un pedido válido de escalar se atiende primero, aunque sea la última vuelta o se haya
        # pasado el tope: así la persona recibe el motivo y el resumen del modelo (curso 2.5 y 4.3).
        for _, nombre, argumentos, error in pedidos:
            if nombre == "escalar_a_humano" and not error:
                turno["usadas"].append("escalar_a_humano")
                return escalar(turno, argumentos["motivo"], argumentos["resumen"], "modelo")
        # Si superó el tope o es la última vuelta, las demás no se ejecutan: nadie usaría su resultado.
        if tokens_del_ticket >= tope:
            return escalar(turno, f"el ticket superó el tope de {tope} tokens", "", "regla")
        if vuelta == MAXIMO_LLAMADAS_POR_MENSAJE:
            break

        # Su mensaje se agrega tal cual (con la firma de Gemini, D11) y cada pedido recibe su resultado.
        conversacion.append(llamada["mensaje"])
        for llamada_id, nombre, argumentos, error in pedidos:
            if error:
                resultado = error
                anotar(turno, "herramienta", f"rechazada: {error}")
            else:
                crear_punto_de_retorno(conexion)
                try:
                    resultado = usar_herramienta(turno, nombre, argumentos)
                except Exception as falla:  # sin red en el embedding, un error de la base...
                    volver_al_punto_de_retorno(conexion)  # deja la transacción usable para escalar
                    return escalar(turno, f"la herramienta {nombre} falló ({falla})", "", "regla")
            conversacion.append({"role": "tool", "tool_call_id": llamada_id, "content": resultado})

    return escalar(turno, f"el agente no terminó en {MAXIMO_LLAMADAS_POR_MENSAJE} llamadas al modelo", "", "regla")
