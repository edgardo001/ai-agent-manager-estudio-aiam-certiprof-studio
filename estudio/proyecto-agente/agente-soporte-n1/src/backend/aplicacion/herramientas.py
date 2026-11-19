"""Las tres herramientas del Agente de Soporte N1: buscar_cliente, buscar_solucion y escalar_a_humano.

Etapa 3. Curso: el agente recibe solo las herramientas que su tarea necesita (permisos
mínimos, Módulo 2, sección 2.3). El modelo pide una herramienta; este archivo revisa el
pedido y la ejecuta. Una herramienta que no está en DEFINICIONES se rechaza: lo
desconocido se trata como restringido (rag.md, patrón 09).
Todo lo que vuelve al modelo va marcado como datos, no como instrucciones (patrón 02).
"""
import json

from aplicacion.base_de_datos import (
    buscar_fragmentos,
    guardar_escalamiento,
    guardar_mensaje,
    leer_cliente,
    leer_mensajes,
)
from aplicacion.modelo import crear_embedding

# Cuántos fragmentos entrega cada búsqueda (k = 5, decisión D8).
CANTIDAD_FRAGMENTOS = 5

# Lo que el agente le dice al cliente cuando el caso pasa a una persona. Lo escribe el código,
# no el modelo: así el agente nunca dice que escaló sin haberlo hecho (hallazgo de la etapa 1).
MENSAJE_ESCALADO = (
    "Una persona de nuestro equipo seguirá con su caso (ticket {ticket}). "
    "Ya tiene todo el contexto, así que no necesita repetir la información."
)

# La descripción que recibe el modelo: nombre claro, para qué sirve y parámetros estrictos.
# buscar_cliente no recibe parámetros: el cliente sale del ticket, no del modelo, así el
# agente no puede leer a otro cliente aunque se lo pidan (sección 2.3).
DEFINICIONES = [
    {
        "type": "function",
        "function": {
            "name": "buscar_cliente",
            "description": "Lee en el CRM los datos del cliente de este ticket: nombre, empresa, plan e historial. "
                           "No recibe parámetros: siempre es el cliente del ticket.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_solucion",
            "description": "Busca en la base de conocimiento las soluciones documentadas más parecidas al problema. "
                           f"Devuelve hasta {CANTIDAD_FRAGMENTOS} fragmentos, cada uno con su fuente (documento > sección).",
            "parameters": {
                "type": "object",
                "properties": {"consulta": {"type": "string", "description": "El problema, en pocas palabras."}},
                "required": ["consulta"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "escalar_a_humano",
            "description": "Pasa el ticket a una persona. El programa le avisa al cliente y le entrega a la persona "
                           "la conversación completa.",
            "parameters": {
                "type": "object",
                "properties": {
                    "motivo": {"type": "string", "description": "Por qué escalas, en una frase."},
                    "resumen": {"type": "string", "description": "Problema y lo que ya intentaste."},
                },
                "required": ["motivo", "resumen"],
            },
        },
    },
]


def marcar_como_datos(etiqueta, texto):
    """Encierra un texto entre <etiqueta> y </etiqueta> para que el modelo lo trate como datos.
    Cambia el signo < del texto por &lt;: sin él no se puede formar ninguna etiqueta, así que
    nadie puede cerrar el bloque desde adentro ni imitar otro (por ejemplo, un <fragmento> falso),
    escriba como escriba la etiqueta. El signo > se deja, porque los documentos lo usan en las
    rutas de menú ("Configuración > Formato de impresión") y en las fuentes ("documento > sección").

    Curso: no seguir instrucciones que vienen dentro de los datos (dimensión adversarial,
    Módulo 2, sección 2.6). La técnica es de rag.md, patrón 02.
    """
    limpio = str(texto).replace("<", "&lt;")
    return f"<{etiqueta}>\n{limpio}\n</{etiqueta}>"


def leer_argumentos(nombre, argumentos_json):
    """Revisa un pedido de herramienta del modelo. Devuelve (argumentos, None) si es válido,
    o (None, error) con un error que el modelo pueda entender.
    Rechaza herramientas desconocidas, JSON roto, parámetros que faltan, sobran o no son texto.

    Curso: el agente solo puede usar las herramientas que se le dieron (Módulo 2, sección 2.3).
    Rechazar lo desconocido no viene del curso (rag.md, patrón 09).
    """
    definicion = next((d["function"] for d in DEFINICIONES if d["function"]["name"] == nombre), None)
    if definicion is None:
        nombres = ", ".join(d["function"]["name"] for d in DEFINICIONES)
        return None, f"Error: la herramienta '{nombre}' no existe y fue rechazada. Solo puedes usar: {nombres}."
    try:
        argumentos = json.loads(argumentos_json or "{}")
    except json.JSONDecodeError:
        return None, f"Error: los argumentos de {nombre} no son un JSON válido."
    if not isinstance(argumentos, dict):
        return None, f"Error: los argumentos de {nombre} deben ser un objeto JSON."
    permitidos = definicion["parameters"]["properties"]
    sobran = [clave for clave in argumentos if clave not in permitidos]
    if sobran:
        return None, f"Error: {nombre} no acepta estos parámetros: {', '.join(sobran)}."
    for clave in definicion["parameters"]["required"]:
        if not isinstance(argumentos.get(clave), str) or not argumentos[clave].strip():
            return None, f"Error: {nombre} necesita el parámetro '{clave}' con un texto."
    return argumentos, None


def buscar(conexion, consulta):
    """Busca una consulta en la base de conocimiento y devuelve los fragmentos más parecidos:
    (documento, sección, texto, similitud, huella del documento).

    Curso: el agente solo responde con soluciones documentadas (Módulo 2, sección 2.5).
    """
    vector = crear_embedding([consulta])[0]
    return buscar_fragmentos(conexion, vector, CANTIDAD_FRAGMENTOS)


def formatear_fragmentos(resultados):
    """Convierte los fragmentos encontrados en el texto que recibe el modelo, cada uno marcado
    como dato y con su fuente, para que pueda citarla.

    Curso: responder solo con soluciones documentadas y, si no hay, escalar (Módulo 2,
    sección 2.5). Citar la fuente es una práctica de RAG que no viene en el curso.
    """
    if not resultados:
        return "No hay soluciones documentadas para esta consulta. Si el problema no tiene solución documentada, escala."
    partes = []
    for documento, seccion, texto, similitud, _ in resultados:
        encabezado = f"Fuente: {documento} > {seccion} (parecido {similitud:.2f})"
        partes.append(marcar_como_datos("fragmento", f"{encabezado}\n{texto}"))
    return "\n".join(partes)


def buscar_cliente(conexion, ticket):
    """Devuelve, marcados como datos, el nombre, la empresa, el plan y el historial del cliente del ticket.

    Curso: el agente conoce el historial del cliente, pero solo el de ese cliente (permisos
    mínimos, Módulo 2, sección 2.3, y la restricción "no compartir información de otros
    clientes" de la sección 2.5).
    """
    cliente = leer_cliente(conexion, cliente_id=ticket["cliente_id"])
    datos = (f"Código: {cliente['codigo']}\nNombre: {cliente['nombre']}\nEmpresa: {cliente['empresa']}\n"
             f"Plan: {cliente['plan']}\nHistorial: {cliente['historial']}")
    return marcar_como_datos("datos_del_cliente", datos)


def buscar_solucion(conexion, consulta):
    """Busca la consulta y devuelve (texto para el modelo, fragmentos encontrados).

    Curso: la herramienta con que el agente encuentra soluciones documentadas
    (Módulo 2, sección 2.5). Es la parte de búsqueda del RAG del proyecto.
    """
    resultados = buscar(conexion, consulta)
    return formatear_fragmentos(resultados), resultados


def escalar_a_humano(conexion, ticket, motivo, resumen, escalado_por, herramientas_usadas):
    """Pasa el ticket a una persona: arma el contexto completo, lo guarda en el ticket y
    devuelve el mensaje para el cliente. escalado_por es 'modelo' o 'regla'.

    Curso: protocolo de escalamiento con contexto completo (Módulo 2, sección 2.5) y qué
    información acompaña el traspaso (Módulo 4, sección 4.3). Qué lleva exactamente el
    resumen lo decide el proyecto.
    """
    cliente = leer_cliente(conexion, cliente_id=ticket["cliente_id"])
    conversacion = "\n".join(f"{quien.capitalize()}: {texto}" for quien, texto in leer_mensajes(conexion, ticket["id"]))
    contexto = (
        f"Ticket {ticket['id']}. Cliente: {cliente['codigo']}, {cliente['nombre']}, {cliente['empresa']}, plan {cliente['plan']}.\n"
        f"Problema: {ticket['texto']}\n"
        f"Motivo: {motivo}\n"
        f"Escalado por: {escalado_por}\n"
        f"Resumen del agente: {resumen or '(sin resumen: escaló una regla)'}\n"
        f"Herramientas usadas: {', '.join(herramientas_usadas) or 'ninguna'}\n"
        f"Conversación:\n{conversacion}"
    )
    guardar_escalamiento(conexion, ticket["id"], motivo, contexto, escalado_por)
    mensaje = MENSAJE_ESCALADO.format(ticket=ticket["id"])
    guardar_mensaje(conexion, ticket["id"], "agente", mensaje)
    return mensaje
