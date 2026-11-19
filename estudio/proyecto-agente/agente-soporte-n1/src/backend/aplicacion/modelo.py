"""Conexión con el modelo de lenguaje (LLM): conversar y crear embeddings.

Etapa 0, ampliado en la etapa 2 con los embeddings y en la etapa 3 con las herramientas
y los tokens usados. Usa la librería openai porque Gemini, OpenRouter y Ollama aceptan
su formato: el mismo código sirve para todos, solo cambia la configuración del .env.
El chat y los embeddings pueden ir a proveedores distintos (decisión D13).
Es el único archivo que habla con el modelo.
"""
from openai import OpenAI

from aplicacion import config

# Segundos máximos de espera por respuesta: así una llamada nunca queda colgada
# y la regla de los 8 minutos se puede cumplir (plan, "Cómo funciona cada regla").
# Sin reintentos automáticos: la librería reintenta 2 veces por defecto, y una llamada
# podría tardar hasta 3 veces el límite. Si falla, quien llama decide qué hacer.
ESPERA_MAXIMA = 60

# Cantidad de números de cada embedding. Debe coincidir con la columna vector(768)
# de la tabla fragmentos_conocimiento (01_esquema.sql).
DIMENSIONES_EMBEDDING = 768


def conectar_modelo(para_embeddings=False):
    """Crea el cliente que habla con el modelo de chat o, con para_embeddings=True, con el de
    embeddings, cada uno con su URL y su clave (D13), y con el límite de espera.
    Técnico: no viene del curso."""
    # Se crea en cada llamada y no al importar el archivo: así, si falta la clave,
    # el programa alcanza a mostrar su propio aviso en vez de un error de la librería.
    if para_embeddings:
        direccion, clave = config.LLM_EMBEDDINGS_BASE_URL, config.LLM_EMBEDDINGS_API_KEY
    else:
        direccion, clave = config.LLM_BASE_URL, config.LLM_API_KEY
    return OpenAI(base_url=direccion, api_key=clave, timeout=ESPERA_MAXIMA, max_retries=0)


def opciones_de_llamada(temperatura):
    """Arma las opciones comunes de una llamada al chat: el modelo, el tope de salida y, solo si
    se pide, la temperatura. Sin temperatura, cada proveedor usa la suya por defecto; las evals
    (etapa 5) y el modelo juez piden 0, para que las respuestas varíen lo menos posible.
    Técnico: no viene del curso (evals-del-llm.md)."""
    opciones = {"model": config.LLM_MODEL, "max_tokens": config.LLM_MAXIMO_TOKENS_SALIDA}
    if temperatura is not None:
        opciones["temperature"] = temperatura
    return opciones


def preguntar_al_modelo(mensajes, temperatura=None):
    """Envía la conversación al modelo y devuelve el texto de su respuesta.
    Desde la etapa 3 el agente usa conversar_con_herramientas(); esta queda para scripts/prueba_conexion.py
    y, en la etapa 5, para el modelo juez de las evals (con temperatura=0).

    Curso: el modelo es la pieza con que el agente razona, pero qué puede hacer
    lo fijan su identidad y sus instrucciones (Módulo 2, secciones 2.2 y 2.5).
    """
    respuesta = conectar_modelo().chat.completions.create(messages=mensajes, **opciones_de_llamada(temperatura))
    # Si el proveedor bloquea la respuesta, el contenido llega vacío (None).
    return respuesta.choices[0].message.content or ""


def conversar_con_herramientas(mensajes, herramientas, temperatura=None):
    """Envía la conversación al modelo junto con la descripción de las herramientas.
    temperatura: None usa la del proveedor; las evals de la etapa 5 piden 0.
    Devuelve un diccionario con:
      mensaje: lo que respondió el modelo, listo para agregarlo a la conversación tal cual;
      texto: su texto (vacío si en vez de responder pidió herramientas);
      llamadas: lista de (id, nombre, argumentos en JSON) de las herramientas que pidió;
      fin: por qué terminó ('stop', 'tool_calls'; 'length' si se cortó por largo,
           'content_filter' si la bloqueó un filtro);
      tokens_entrada y tokens_salida: lo que gastó esta llamada (0 si el proveedor no los informa).

    Curso: el modelo razona y elige la herramienta, pero solo puede usar las que se le
    dan (Módulo 2, sección 2.3, permisos mínimos).
    """
    respuesta = conectar_modelo().chat.completions.create(
        messages=mensajes, tools=herramientas, **opciones_de_llamada(temperatura)
    )
    eleccion = respuesta.choices[0]
    mensaje = eleccion.message
    llamadas = [(llamada.id, llamada.function.name, llamada.function.arguments)
                for llamada in (mensaje.tool_calls or [])]
    uso = respuesta.usage
    return {
        # model_dump conserva los campos extra del proveedor, como los reasoning_details de
        # OpenRouter (D13) o la "firma de pensamiento" que Gemini 3 agrega a cada pedido de
        # herramienta: si no se devuelve en la siguiente llamada, Gemini responde error 400 (D11).
        "mensaje": mensaje.model_dump(exclude_none=True),
        "texto": mensaje.content or "",
        "llamadas": llamadas,
        "fin": eleccion.finish_reason,
        "tokens_entrada": uso.prompt_tokens if uso else 0,
        "tokens_salida": uso.completion_tokens if uso else 0,
    }


def calcular_costo(tokens_entrada, tokens_salida):
    """Pasa a dólares los tokens de una llamada, con los precios del .env.

    Curso: el costo por caso del Módulo 3 (sección 3.2) y el ROI del Módulo 5.
    """
    return (tokens_entrada * config.PRECIO_MILLON_TOKENS_ENTRADA
            + tokens_salida * config.PRECIO_MILLON_TOKENS_SALIDA) / 1_000_000


def crear_embedding(textos):
    """Convierte una lista de textos en vectores de 768 números que representan su significado.
    Textos parecidos dan vectores cercanos: así se buscan documentos por lo que dicen.

    Curso: es la base del RAG con que el agente encuentra soluciones documentadas
    (Módulo 2, sección 2.5); el término RAG no viene en el curso.
    """
    respuesta = conectar_modelo(para_embeddings=True).embeddings.create(
        model=config.LLM_MODELO_EMBEDDINGS, input=textos, dimensions=DIMENSIONES_EMBEDDING
    )
    return [dato.embedding for dato in respuesta.data]
