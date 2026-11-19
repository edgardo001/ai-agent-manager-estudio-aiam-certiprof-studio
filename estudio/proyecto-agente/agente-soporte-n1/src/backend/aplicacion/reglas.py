"""Reglas en código: lo que el agente debe cumplir siempre, sin depender de lo que decida el modelo.

Etapa 4. El modelo decide lo que requiere razonamiento; estas funciones controlan lo que
requiere garantías (rag.md): el kill switch, los 8 minutos de cada mensaje, la cancelación,
lo que nunca puede decir una respuesta y los tickets que quedaron sin atender.
Las revisiones son patrones de palabras, simples a propósito (D16): no entienden el sentido, así
que sus límites se miden en las evals (etapa 5) y en la revisión por muestreo (Módulo 3, 3.3).
"""
import re
import time
import unicodedata

from aplicacion import config, herramientas
from aplicacion.base_de_datos import (
    cambiar_detencion,
    leer_agente,
    leer_ticket,
    marcar_sin_confirmar,
    registrar_paso,
    tickets_sin_respuesta,
)

# Largo máximo del mensaje de un cliente. Uno más largo no se envía al modelo: se escala.
# Valor del proyecto, no viene en el curso (rag.md, guardrails de entrada).
MAXIMO_CARACTERES_MENSAJE = 2000

# Cancelación: el curso pide escalar siempre (Módulo 2, sección 2.5). Se busca sin tildes y exige
# intención u objeto (decisión del usuario): "ya cancelé la factura" significa pagarla en Chile y
# en buena parte de Latinoamérica, y no es pedir la baja.
OBJETO_DE_LA_BAJA = r"(cuenta|suscripcion|servicio|plan|contrato|membresia)"
PATRON_CANCELACION = re.compile(
    r"\b(quiero|quisiera|queremos|deseo|necesito|voy a|vamos a|me gustaria|como (puedo|hago para))\s+"
    r"(cancelar|anular|terminar|cerrar|dar(me|lo|la|nos|se)? de baja)\b"
    rf"|\b(cancel|anul)\w*\s+(mi|la|el|nuestra|nuestro|esta|este)?\s*{OBJETO_DE_LA_BAJA}\b"
    r"|\bcancelacion\b|\bdar(me|te|se|nos|lo|la)? de baja\b|\bcerrar (mi |la |nuestra )?cuenta\b"
    r"|\bdesuscrib\w*|\b(terminar|rescindir) (el |mi |nuestro )?contrato\b|\bno (quiero|queremos) renovar\b")

# Lo que una respuesta nunca puede decir (restricciones del SOP, Módulo 2, sección 2.5). Se busca
# ofrecer o afirmar, no mencionar: "no ofrecemos descuentos" o "usted pidió un reembolso" pasan.
BENEFICIO = r"(descuento|rebaja|gratis|sin cargo|sin costo|credito|reembolso|bonificacion|mes de regalo)"
PATRON_DESCUENTO = re.compile(
    r"\b(ofrezco|ofrecemos|le doy|te doy|le damos|te damos|aplico|aplicamos|aplicaremos|regalamos|"
    rf"le haremos|bonificamos|abonamos|otorgamos)\b(\W+\w+){{0,5}}?\W+{BENEFICIO}"
    rf"|\b\d+\s?%\s*(de\s+)?(descuento|rebaja)|\b(un|una|dos|tres|\d+)\s+(mes|meses|semana|semanas)\s+(gratis|sin cargo|sin costo)")
# Afirmar un cambio ya hecho. Va sobre el texto con tildes: "actualicé su cuenta" (lo hizo el
# agente) no es "actualice su aplicación" (una indicación al cliente).
PATRON_CAMBIO_DE_CUENTA = re.compile(  # "se ha actualizado" habla de la aplicación, no de lo que hizo el agente
    r"(?<!\bse )\b(he|hemos|ha|han|ya)\s+(sido\s+)?(cambiad|modificad|actualizad|cancelad|eliminad|reembolsad|anulad|"
    r"aplicad|procesad)[oa]s?\b|\b(fue|fueron)\s+(cambiad|modificad|actualizad|cancelad|eliminad|reembolsad|anulad)[oa]s?\b"
    r"|\b(cambié|modifiqué|actualicé|cancelé|eliminé|reembolsé|anulé|procesé)\b")
PATRON_CODIGO_CLIENTE = re.compile(r"\bC[- ]?(\d{3})\b", re.IGNORECASE)
# Una negación no es una oferta: "no ofrecemos descuentos" o "no podemos darle un reembolso" pasan.
PATRON_NEGACION = re.compile(
    r"\bno\s+(podemos\s+|puedo\s+)?(le |te |les )?(ofrezco|ofrecemos|ofrecer\w*|doy|damos|dar\w*|aplico|aplicamos|aplicar\w*)\b")

MINUTOS_SIN_CONFIRMAR = 24 * 60  # un ticket respondido sin confirmar en 24 horas (decisión del proyecto)

# Trucos de caracteres para saltarse un patrón (pruebas adversariales de la etapa 5): caracteres
# invisibles dentro de una palabra, letras cirílicas o griegas que se ven iguales a las latinas, y
# guiones que pegan palabras ("quiero-cancelar") o que no son el guion común ("C‑002").
INVISIBLES = dict.fromkeys(map(ord, "\u00ad\u200b\u200c\u200d\u2060\ufeff"))
PARECIDAS = str.maketrans("аеорсхуіАЕОРСХУІοαΟΑ", "aeopcxyiAEOPCXYIoaOA")
GUIONES = re.compile(r"[\u2010-\u2015\u2212_-]")


def normalizar(texto):
    """Quita los trucos de caracteres: compone las letras (NFKC), borra los invisibles, cambia las
    letras parecidas por las latinas y los guiones por espacios. Técnico: no viene del curso."""
    texto = unicodedata.normalize("NFKC", texto).translate(INVISIBLES).translate(PARECIDAS)
    return GUIONES.sub(" ", texto)


def sin_tildes(texto):
    """Pasa el texto a minúsculas y sin tildes, sin trucos de caracteres, para comparar palabras
    escritas de cualquier forma. Técnico: no viene del curso."""
    normal = unicodedata.normalize("NFD", normalizar(texto).lower())
    return "".join(letra for letra in normal if unicodedata.category(letra) != "Mn")


def agente_detenido(agente):
    """Dice si el agente está detenido por el kill switch.

    Curso: kill switch (Módulo 1, sección 1.2, pedido para el Nivel 4) y circuit breaker
    (Módulo 4, sección 4.5). Con el agente detenido, los tickets no se rechazan: pasan a una
    persona (decisión del proyecto).
    """
    return bool(agente["detenido"])


def tiempo_excedido(inicio):
    """Dice si la atención del mensaje actual ya pasó los minutos permitidos, contados desde que
    llegó el mensaje (inicio, en segundos de time.monotonic()).

    Curso: escalar si el tiempo de resolución supera 8 minutos (Módulo 2, sección 2.5); medirlo
    por mensaje es decisión del usuario (plan, "Cómo funciona cada regla"). El modelo no tiene reloj.
    """
    return time.monotonic() - inicio > config.MINUTOS_MAXIMOS_ANTES_DE_ESCALAR * 60


def revisar_entrada(texto):
    """Revisa el mensaje del cliente antes de enviarlo al modelo. Devuelve el motivo para escalar,
    o None si puede seguir.

    Curso: el cliente que menciona cancelación pasa a una persona (Módulo 2, sección 2.5).
    El largo máximo es una práctica que no viene del curso (rag.md, guardrails de entrada).
    """
    if len(texto) > MAXIMO_CARACTERES_MENSAJE:
        return f"el mensaje del cliente supera {MAXIMO_CARACTERES_MENSAJE} caracteres"
    if PATRON_CANCELACION.search(sin_tildes(texto)):
        return "el cliente menciona cancelación"
    return None


def revisar_respuesta(texto, codigo_cliente, otros_clientes=()):
    """Revisa la respuesta del modelo antes de enviarla al cliente. Devuelve el motivo para no
    enviarla y escalar, o None si se puede enviar. No se reintenta: se escala (rag.md).
    otros_clientes son los nombres y las empresas de los demás clientes: se buscan completos
    (el apellido solo no se detecta; límite conocido, en las pruebas adversariales).

    Curso: restricciones del SOP: "No realizar cambios en la cuenta del cliente sin confirmación
    humana. No compartir información de otros clientes. No ofrecer descuentos no autorizados."
    (Módulo 2, sección 2.5). Revisar la salida antes de que llegue al cliente está inspirado en los
    puntos de verificación obligatoria de los fallos silenciosos (Módulo 3, sección 3.3).
    """
    if PATRON_DESCUENTO.search(PATRON_NEGACION.sub(" ", sin_tildes(texto))):
        return "la respuesta ofrece un descuento"
    if PATRON_CAMBIO_DE_CUENTA.search(normalizar(texto).lower()):  # con tildes: "actualicé" no es "actualice"
        return "la respuesta afirma un cambio en la cuenta sin confirmación humana"
    propio = PATRON_CODIGO_CLIENTE.search(codigo_cliente or "")
    otros = sorted({f"C-{numero}" for numero in PATRON_CODIGO_CLIENTE.findall(normalizar(texto))
                    if not propio or numero != propio.group(1)})
    comparable = f" {' '.join(re.findall(r'\w+', sin_tildes(texto)))} "
    otros += [nombre for nombre in otros_clientes
              if f" {' '.join(re.findall(r'\w+', sin_tildes(nombre)))} " in comparable]
    if otros:
        return f"la respuesta menciona a otro cliente ({', '.join(otros)})"
    return None


def cambiar_kill_switch(conexion, detener, quien, motivo):
    """Activa (detener=True) o desactiva el kill switch. Con el agente detenido, los tickets pasan a
    una persona. Queda en la auditoría como intervención, sin ticket, con quién, cuándo y por qué
    (registrarlo así es decisión del proyecto).

    Curso: kill switch (Módulo 1, sección 1.2, pedido para el Nivel 4) y circuit breaker (Módulo 4,
    sección 4.5); cuándo intervenir lo dicen las señales de la sección 3.4 del Módulo 3.
    """
    agente = leer_agente(conexion)
    cambiar_detencion(conexion, agente["id"], detener, motivo if detener else None)
    decision = "agente detenido" if detener else "agente reactivado"
    registrar_paso(conexion, agente["id"], None, None, "intervencion", decision, {}, motivo, None, None, quien)


def escalar_vencidos(conexion):
    """Revisa los tickets que quedaron sin atender: escala los que tienen un mensaje del cliente
    sin respuesta por más de los minutos permitidos (el agente se cayó a mitad), y deja como
    'resuelto_sin_confirmar' los respondidos que el cliente no confirmó en 24 horas.
    Devuelve (cuántos escaló, cuántos marcó sin confirmar). Se llama al abrir la consola y, en la
    etapa 7, la cola de escalaciones y el dashboard.

    Curso: los 8 minutos (Módulo 2, sección 2.5). No contar como resueltos los tickets que nadie
    confirmó es una regla del proyecto, inspirada en la tasa de resolución autónoma (Módulo 3,
    sección 3.2) y en los fallos silenciosos (sección 3.3).
    """
    agente = leer_agente(conexion)
    motivo = f"el mensaje del cliente lleva más de {config.MINUTOS_MAXIMOS_ANTES_DE_ESCALAR:g} minutos sin respuesta"
    ids = tickets_sin_respuesta(conexion, config.MINUTOS_MAXIMOS_ANTES_DE_ESCALAR)
    for ticket_id in ids:
        herramientas.escalar_a_humano(conexion, leer_ticket(conexion, ticket_id), motivo, "", "regla", [])
        registrar_paso(conexion, agente["id"], ticket_id, None, "regla", f"escalar_a_humano: {motivo}", {}, motivo,
                       None, None, None)
    return len(ids), marcar_sin_confirmar(conexion, MINUTOS_SIN_CONFIRMAR)
