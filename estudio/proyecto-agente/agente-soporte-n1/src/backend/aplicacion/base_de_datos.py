"""Conexión con PostgreSQL: base de conocimiento, registro del agente, clientes y tickets.

Etapa 2, ampliado en la etapa 3 (clientes, tickets y mensajes). Usa la librería pg8000
(licencia BSD, decisión D1). Es el único archivo que habla con la base de datos: el resto
del programa llama a estas funciones, y todo el SQL vive aquí.
Los vectores se envían como texto y PostgreSQL los convierte con ::vector (decisión D2).
Quien abre una conexión la cierra al terminar, aunque haya un error (try/finally).
Estas funciones no confirman los cambios (commit): lo hace quien abrió la conexión,
al terminar cada mensaje (decisión D11). Así las pruebas pueden deshacerlo todo.
"""
import pg8000.dbapi

from aplicacion import config

ESPERA_CONEXION = 10  # segundos


def conectar():
    """Abre una conexión con PostgreSQL usando los datos del .env.
    Espera como máximo ESPERA_CONEXION segundos, para no quedar colgado si la base no responde.
    Técnico: no viene del curso."""
    return pg8000.dbapi.connect(
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        host=config.POSTGRES_HOST,
        database=config.POSTGRES_DB,
        timeout=ESPERA_CONEXION,
    )


def vector_a_texto(vector):
    """Convierte una lista de números en el texto que entiende pgvector: "[0.12,-0.03,...]".
    Técnico: no viene del curso (decisión D2)."""
    return "[" + ",".join(str(numero) for numero in vector) + "]"


def borrar_fragmentos(conexion):
    """Borra toda la base de conocimiento, antes de volver a cargarla completa.
    Técnico: no viene del curso (la carga completa es la decisión D8)."""
    conexion.cursor().execute("DELETE FROM fragmentos_conocimiento")


def guardar_fragmento(conexion, documento, seccion, orden, texto, vector, hash_documento):
    """Guarda un fragmento de un documento con su vector en la base de conocimiento,
    junto con el modelo que lo creó y la huella del documento.

    Curso: la base de conocimiento son las soluciones documentadas con que
    responde el agente (Módulo 2, sección 2.5). Guardar el origen de cada vector
    es una práctica de RAG que no viene en el curso (decisión D8).
    """
    conexion.cursor().execute(
        "INSERT INTO fragmentos_conocimiento "
        "(documento, seccion, orden, texto, embedding, modelo_embedding, hash_documento) "
        "VALUES (%s, %s, %s, %s, %s::vector, %s, %s)",
        (documento, seccion, orden, texto, vector_a_texto(vector), config.LLM_MODELO_EMBEDDINGS, hash_documento),
    )


def buscar_fragmentos(conexion, vector, cantidad):
    """Devuelve los fragmentos más parecidos a un vector: (documento, sección, texto, similitud).
    La similitud va de 0 a 1; mientras más alta, más se parece al texto buscado.

    Curso: el agente solo responde con soluciones documentadas; si no encuentra
    una que corresponda, escala (Módulo 2, sección 2.5).
    """
    cursor = conexion.cursor()
    texto_vector = vector_a_texto(vector)
    # <=> mide la distancia de coseno: ordenar de menor a mayor trae primero lo más parecido.
    # Solo se comparan vectores creados con el mismo modelo que la consulta (decisión D8).
    cursor.execute(
        "SELECT documento, seccion, texto, 1 - (embedding <=> %s::vector) AS similitud "
        "FROM fragmentos_conocimiento WHERE modelo_embedding = %s "
        "ORDER BY embedding <=> %s::vector LIMIT %s",
        (texto_vector, config.LLM_MODELO_EMBEDDINGS, texto_vector, cantidad),
    )
    return cursor.fetchall()


def contar_fragmentos(conexion):
    """Cuenta los fragmentos cargados con el modelo de embeddings actual.
    Si es 0, la búsqueda no encontraría nada: hay que ejecutar la carga.
    Técnico: no viene del curso (rag.md)."""
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT count(*) FROM fragmentos_conocimiento WHERE modelo_embedding = %s",
        (config.LLM_MODELO_EMBEDDINGS,),
    )
    return cursor.fetchone()[0]


def leer_agente(conexion):
    """Devuelve el registro del agente como diccionario: id, nombre, fuera_de_alcance, detenido.

    Curso: el registro de agentes dice quién es cada agente y qué no atiende
    (Módulo 2, secciones 2.2 y 2.7).
    """
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id, nombre, fuera_de_alcance, detenido FROM registro_agentes WHERE nombre = %s",
        ("Agente de Soporte N1",),
    )
    fila = cursor.fetchone()
    if fila is None:
        return None
    return {"id": fila[0], "nombre": fila[1], "fuera_de_alcance": fila[2], "detenido": fila[3]}


def leer_cliente(conexion, cliente_id=None, codigo=None):
    """Devuelve un cliente del CRM simulado, por su id interno o por su código (C-001).
    Devuelve None si no existe.

    Curso: el CRM es de solo lectura para el agente; no hay ninguna función que lo cambie
    (permisos mínimos, Módulo 2, sección 2.3).
    """
    cursor = conexion.cursor()
    if codigo is not None:
        cursor.execute("SELECT id, codigo, nombre, empresa, plan, historial FROM clientes WHERE codigo = %s", (codigo,))
    else:
        cursor.execute("SELECT id, codigo, nombre, empresa, plan, historial FROM clientes WHERE id = %s", (cliente_id,))
    fila = cursor.fetchone()
    if fila is None:
        return None
    return dict(zip(("id", "codigo", "nombre", "empresa", "plan", "historial"), fila))


def crear_ticket(conexion, agente_id, cliente_id, texto):
    """Crea un ticket nuevo y devuelve su número.

    Curso: el ticket es el caso, la unidad que se mide (Módulo 3, sección 3.2).
    """
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO tickets (agente_id, cliente_id, texto) VALUES (%s, %s, %s) RETURNING id",
        (agente_id, cliente_id, texto),
    )
    return cursor.fetchone()[0]


def leer_ticket(conexion, ticket_id):
    """Devuelve un ticket como diccionario, con sus tokens y su costo acumulados,
    o None si no existe. Técnico: no viene del curso."""
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id, agente_id, cliente_id, texto, estado, respuesta, motivo_escalamiento, "
        "resumen_escalamiento, escalado_por, tokens_entrada, tokens_salida, costo_tokens "
        "FROM tickets WHERE id = %s",
        (ticket_id,),
    )
    fila = cursor.fetchone()
    if fila is None:
        return None
    nombres = ("id", "agente_id", "cliente_id", "texto", "estado", "respuesta", "motivo_escalamiento",
               "resumen_escalamiento", "escalado_por", "tokens_entrada", "tokens_salida", "costo_tokens")
    return dict(zip(nombres, fila))


def guardar_mensaje(conexion, ticket_id, quien, texto):
    """Guarda un mensaje de la conversación del ticket: quien es 'cliente', 'agente' o 'persona'.

    Curso: la persona que recibe un caso escalado debe ver todo el contexto
    (Módulo 2, sección 2.5, y Módulo 4, sección 4.3).
    """
    conexion.cursor().execute(
        "INSERT INTO mensajes (ticket_id, quien, texto) VALUES (%s, %s, %s)",
        (ticket_id, quien, texto),
    )


def leer_mensajes(conexion, ticket_id):
    """Devuelve la conversación del ticket en orden: una lista de (quien, texto).
    Técnico: no viene del curso."""
    cursor = conexion.cursor()
    cursor.execute("SELECT quien, texto FROM mensajes WHERE ticket_id = %s ORDER BY id", (ticket_id,))
    return [tuple(fila) for fila in cursor.fetchall()]


def sumar_tokens(conexion, ticket_id, tokens_entrada, tokens_salida, costo):
    """Suma al ticket los tokens y el costo de una llamada al modelo.

    Curso: el costo por caso es uno de los indicadores de negocio (Módulo 3, sección 3.2).
    """
    conexion.cursor().execute(
        "UPDATE tickets SET tokens_entrada = tokens_entrada + %s, tokens_salida = tokens_salida + %s, "
        "costo_tokens = costo_tokens + %s WHERE id = %s",
        (tokens_entrada, tokens_salida, costo, ticket_id),
    )


def guardar_respuesta(conexion, ticket_id, respuesta):
    """Guarda la respuesta del agente y deja el ticket como 'respondido'.
    No toca un ticket que ya pasó a una persona.

    Curso: el agente resuelve con una solución documentada (Módulo 2, sección 2.5).
    Que el ticket quede 'resuelto' solo cuando el cliente lo confirma es una decisión
    del proyecto, no viene en el curso (plan, "Cómo funciona cada regla").
    """
    conexion.cursor().execute(
        "UPDATE tickets SET estado = 'respondido', respuesta = %s WHERE id = %s AND estado <> 'escalado'",
        (respuesta, ticket_id),
    )


def guardar_escalamiento(conexion, ticket_id, motivo, resumen, escalado_por):
    """Deja el ticket como 'escalado', con el motivo, el resumen para la persona y quién escaló
    ('modelo' o 'regla').

    Curso: protocolo de escalamiento con el contexto completo (Módulo 2, sección 2.5).
    """
    conexion.cursor().execute(
        "UPDATE tickets SET estado = 'escalado', motivo_escalamiento = %s, resumen_escalamiento = %s, "
        "escalado_por = %s, cerrado_en = now() WHERE id = %s",
        (motivo, resumen, escalado_por, ticket_id),
    )


def promedio_tokens_por_ticket(conexion):
    """Devuelve (tickets con tokens, promedio de tokens de entrada, de salida y costo por ticket),
    o None si todavía no hay tickets. Lo usa estimar_costos.py para reemplazar sus supuestos.

    Curso: costo por caso (Módulo 3, sección 3.2).
    """
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT count(*), avg(tokens_entrada), avg(tokens_salida), avg(costo_tokens) "
        "FROM tickets WHERE tokens_entrada > 0"
    )
    cantidad, entrada, salida, costo = cursor.fetchone()
    if not cantidad:
        return None
    return cantidad, float(entrada), float(salida), float(costo)
