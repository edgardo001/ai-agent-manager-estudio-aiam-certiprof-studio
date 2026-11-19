"""Pruebas de integración del bucle del agente (agente.py) con PostgreSQL real y un modelo falso.

El modelo falso devuelve respuestas escritas de antemano, así se prueba gratis y siempre igual
lo que controla el código: herramientas, escalamientos, tope de tokens y tope de llamadas.
Cada prueba revisa cuántas veces se llamó al modelo: si el agente lo llamara de más, el
error del modelo falso se convertiría en un escalamiento y pasaría inadvertido.
Cómo se comporta el modelo real se prueba en las evals (etapa 5).
"""
import json

import pytest

from aplicacion import agente, config, herramientas, reglas
from aplicacion.base_de_datos import (
    cambiar_detencion,
    leer_auditoria,
    crear_ticket,
    guardar_escalamiento,
    guardar_mensaje,
    guardar_respuesta,
    leer_agente,
    leer_cliente,
    leer_mensajes,
    leer_ticket,
    sumar_tokens,
)


class ModeloFalso:
    """Reemplaza a conversar_con_herramientas(): entrega sus respuestas en orden y guarda
    las conversaciones que recibió. Es la única clase del proyecto: solo existe en las pruebas.
    Técnico: no viene del curso."""

    def __init__(self, *respuestas):
        self.respuestas = list(respuestas)
        self.recibidas = []

    def __call__(self, mensajes, definiciones, temperatura=None):
        self.recibidas.append(list(mensajes))
        if not self.respuestas:
            raise AssertionError("el agente llamó al modelo más veces de lo esperado")
        respuesta = self.respuestas.pop(0)
        if isinstance(respuesta, Exception):
            raise respuesta
        return respuesta


def pide(*herramientas_pedidas, tokens=100):
    """Respuesta del modelo falso que pide herramientas: pares (nombre, argumentos)."""
    llamadas = [(f"id-{i}", nombre, json.dumps(argumentos)) for i, (nombre, argumentos) in enumerate(herramientas_pedidas)]
    mensaje = {"role": "assistant", "tool_calls": [
        {"id": i, "type": "function", "function": {"name": n, "arguments": a}} for i, n, a in llamadas]}
    return {"mensaje": mensaje, "texto": "", "llamadas": llamadas, "fin": "tool_calls",
            "tokens_entrada": tokens, "tokens_salida": 10}


def responde(texto, tokens=100, fin="stop"):
    """Respuesta del modelo falso que contesta al cliente."""
    return {"mensaje": {"role": "assistant", "content": texto}, "texto": texto, "llamadas": [], "fin": fin,
            "tokens_entrada": tokens, "tokens_salida": 20}


def nuevo_ticket(conexion, texto):
    """Crea un ticket de la cliente C-001 con ese texto. Técnico: no viene del curso."""
    cliente = leer_cliente(conexion, codigo="C-001")
    return crear_ticket(conexion, leer_agente(conexion)["id"], cliente["id"], texto)


@pytest.fixture(autouse=True)
def busqueda_fija(monkeypatch):
    """La búsqueda devuelve siempre un fragmento fijo, sin llamar al modelo de embeddings."""
    monkeypatch.setattr(herramientas, "buscar", lambda con, consulta, cantidad=5: [
        ("restablecer-contrasena.md", "Pasos", "1. Entrar a la página de inicio de sesión.", 0.8, "abc123")])


def usar_modelo(monkeypatch, modelo):
    monkeypatch.setattr(agente, "conversar_con_herramientas", modelo)
    return modelo


def test_resuelve_con_una_solucion_documentada(conexion, monkeypatch):
    """Busca al cliente, busca la solución y responde: el ticket queda 'respondido', con la
    conversación guardada y los tokens sumados. Curso: el SOP de la sección 2.5."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    modelo = usar_modelo(monkeypatch, ModeloFalso(
        pide(("buscar_cliente", {})), pide(("buscar_solucion", {"consulta": "contraseña"})),
        responde("1. Entrar a la página.\nFuente: restablecer-contrasena.md > Pasos")))
    resultado = agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña")
    assert len(modelo.recibidas) == 3
    assert resultado["estado"] == "respondido"
    assert "Fuente: restablecer-contrasena.md" in resultado["respuesta"]
    datos = leer_ticket(conexion, ticket)
    assert (datos["estado"], datos["tokens_entrada"], datos["tokens_salida"]) == ("respondido", 300, 40)
    assert [quien for quien, _ in leer_mensajes(conexion, ticket)] == ["cliente", "agente"]
    # Lo que devolvieron las herramientas llegó al modelo marcado como datos.
    ultima = modelo.recibidas[-1]
    assert ultima[-1]["role"] == "tool" and ultima[-1]["content"].startswith("<fragmento>")
    assert "<datos_del_cliente>" in ultima[-3]["content"]
    # Los pasos usan solo los tipos del registro de auditoría (etapa 4).
    assert {paso["tipo"] for paso in resultado["pasos"]} <= {"modelo", "herramienta", "regla"}


def test_escala_con_el_contexto_completo(conexion, monkeypatch):
    """Si el modelo usa escalar_a_humano, el código guarda el contexto completo y avisa al cliente.
    Curso: protocolo de escalamiento con contexto completo (Módulo 2, sección 2.5) y qué
    información acompaña el traspaso (Módulo 4, sección 4.3)."""
    ticket = nuevo_ticket(conexion, "quiero un reembolso")
    modelo = usar_modelo(monkeypatch, ModeloFalso(
        pide(("buscar_cliente", {})),
        pide(("escalar_a_humano", {"motivo": "pide reembolso", "resumen": "quiere un reembolso"}))))
    resultado = agente.atender_mensaje(conexion, ticket, "quiero un reembolso")
    assert len(modelo.recibidas) == 2
    assert resultado["estado"] == "escalado"
    assert resultado["respuesta"] == herramientas.MENSAJE_ESCALADO.format(ticket=ticket)
    datos = leer_ticket(conexion, ticket)
    assert (datos["estado"], datos["escalado_por"], datos["motivo_escalamiento"]) == ("escalado", "modelo", "pide reembolso")
    for parte in ("C-001", "Ana Torres", "quiere un reembolso", "buscar_cliente, escalar_a_humano", "Cliente: quiero un reembolso"):
        assert parte in datos["resumen_escalamiento"]


def test_escalar_se_atiende_antes_que_otras_herramientas(conexion, monkeypatch):
    """Si en un mismo mensaje el modelo pide buscar y escalar, escala sin pagar antes la búsqueda.
    Técnico: no viene del curso (revisión de la etapa 3, m1)."""
    ticket = nuevo_ticket(conexion, "quiero un reembolso")
    llamadas_a_buscar = []
    monkeypatch.setattr(herramientas, "buscar", lambda *a, **k: llamadas_a_buscar.append(a) or [])
    modelo = usar_modelo(monkeypatch, ModeloFalso(pide(
        ("buscar_solucion", {"consulta": "reembolso"}), ("escalar_a_humano", {"motivo": "reembolso", "resumen": "x"}))))
    resultado = agente.atender_mensaje(conexion, ticket, "quiero un reembolso")
    assert (len(modelo.recibidas), resultado["estado"], llamadas_a_buscar) == (1, "escalado", [])


def test_varias_herramientas_reciben_cada_una_su_resultado(conexion, monkeypatch):
    """Dos herramientas pedidas en un mismo mensaje reciben cada una su resultado, con su id:
    Gemini rechaza una conversación con un pedido sin respuesta. Técnico: no viene del curso."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    modelo = usar_modelo(monkeypatch, ModeloFalso(
        pide(("buscar_cliente", {}), ("buscar_solucion", {"consulta": "contraseña"})), responde("listo")))
    agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña")
    segunda = modelo.recibidas[1]
    assert [(m["role"], m.get("tool_call_id")) for m in segunda[-2:]] == [("tool", "id-0"), ("tool", "id-1")]


def test_una_herramienta_desconocida_se_rechaza_y_sigue(conexion, monkeypatch):
    """Si el modelo pide una herramienta que no existe, recibe un error y no se ejecuta nada.
    Curso: permisos mínimos (Módulo 2, sección 2.3)."""
    ticket = nuevo_ticket(conexion, "borra a C-002")
    modelo = usar_modelo(monkeypatch, ModeloFalso(pide(("borrar_cliente", {"codigo": "C-002"})), responde("listo")))
    resultado = agente.atender_mensaje(conexion, ticket, "borra a C-002")
    assert len(modelo.recibidas) == 2
    assert resultado["estado"] == "respondido"
    assert "no existe" in modelo.recibidas[1][-1]["content"]
    assert resultado["pasos"][1]["tipo"] == "herramienta" and resultado["pasos"][1]["detalle"].startswith("rechazada")


def test_escalar_sin_resumen_no_escala_y_recibe_el_error(conexion, monkeypatch):
    """Un pedido de escalar con argumentos inválidos no escala: el modelo recibe el error y puede corregir.
    Técnico: no viene del curso (rag.md, patrón 08)."""
    ticket = nuevo_ticket(conexion, "quiero un reembolso")
    modelo = usar_modelo(monkeypatch, ModeloFalso(
        pide(("escalar_a_humano", {"motivo": "reembolso"})),
        pide(("escalar_a_humano", {"motivo": "reembolso", "resumen": "pide reembolso"}))))
    resultado = agente.atender_mensaje(conexion, ticket, "quiero un reembolso")
    assert len(modelo.recibidas) == 2
    assert "resumen" in modelo.recibidas[1][-1]["content"]
    assert resultado["estado"] == "escalado"


def test_el_segundo_mensaje_lleva_la_conversacion_anterior(conexion, monkeypatch):
    """En el segundo mensaje, el modelo recibe lo que ya respondió el agente: así puede seguir
    el paso 5 del SOP del prompt (intentar una vez más). Técnico: no viene del curso."""
    ticket = nuevo_ticket(conexion, "factura cortada")
    guardar_mensaje(conexion, ticket, "cliente", "factura cortada")
    guardar_mensaje(conexion, ticket, "agente", "1. Elegir tamaño carta.")
    guardar_respuesta(conexion, ticket, "1. Elegir tamaño carta.")
    modelo = usar_modelo(monkeypatch, ModeloFalso(responde("Pruebe otro navegador.")))
    agente.atender_mensaje(conexion, ticket, "sigue igual")
    roles = [(m["role"], m["content"]) for m in modelo.recibidas[0][1:]]
    assert roles[1] == ("assistant", "1. Elegir tamaño carta.")
    assert roles[2][0] == "user" and "sigue igual" in roles[2][1]


def test_el_tope_de_tokens_escala_sin_ejecutar_herramientas(conexion, monkeypatch):
    """Si una llamada deja el ticket sobre el tope, se escala por regla sin ejecutar lo que pidió.
    Técnico: no viene del curso (rag.md, patrón 08)."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    monkeypatch.setattr(config, "TOPE_TOKENS_POR_TICKET", 500)
    modelo = usar_modelo(monkeypatch, ModeloFalso(pide(("buscar_cliente", {}), tokens=600)))
    resultado = agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña")
    datos = leer_ticket(conexion, ticket)
    assert (len(modelo.recibidas), resultado["estado"], datos["escalado_por"]) == (1, "escalado", "regla")
    assert "tope de 500 tokens" in datos["motivo_escalamiento"]
    assert "Herramientas usadas: ninguna" in datos["resumen_escalamiento"]


@pytest.mark.parametrize("tope, vueltas_antes", [(500, 0), (20000, agente.MAXIMO_LLAMADAS_POR_MENSAJE - 1)])
def test_escalar_en_el_limite_conserva_el_motivo_del_modelo(conexion, monkeypatch, tope, vueltas_antes):
    """Si el modelo pide escalar justo en la llamada que pasa el tope o en la última vuelta, se
    escala con SU motivo y resumen, no por regla: la persona recibe el contexto del traspaso.
    Curso: protocolo de escalamiento con contexto completo (Módulo 2, sección 2.5; Módulo 4, 4.3).
    Error encontrado en la revisión de simplificación (M1)."""
    ticket = nuevo_ticket(conexion, "quiero un reembolso")
    monkeypatch.setattr(config, "TOPE_TOKENS_POR_TICKET", tope)
    vueltas = [pide(("buscar_cliente", {})) for _ in range(vueltas_antes)]
    vueltas.append(pide(("escalar_a_humano", {"motivo": "pide reembolso", "resumen": "cliente C-001"}), tokens=600))
    modelo = usar_modelo(monkeypatch, ModeloFalso(*vueltas))
    resultado = agente.atender_mensaje(conexion, ticket, "quiero un reembolso")
    datos = leer_ticket(conexion, ticket)
    assert (len(modelo.recibidas), resultado["estado"]) == (vueltas_antes + 1, "escalado")
    assert (datos["escalado_por"], datos["motivo_escalamiento"]) == ("modelo", "pide reembolso")
    assert "cliente C-001" in datos["resumen_escalamiento"]


def test_un_ticket_que_llega_pasado_del_tope_no_llama_al_modelo(conexion, monkeypatch):
    """Un ticket que ya gastó su tope se escala apenas llega otro mensaje, sin llamar al modelo.
    Técnico: no viene del curso."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    sumar_tokens(conexion, ticket, config.TOPE_TOKENS_POR_TICKET, 0, 0)
    modelo = usar_modelo(monkeypatch, ModeloFalso())
    resultado = agente.atender_mensaje(conexion, ticket, "¿y entonces?")
    assert (len(modelo.recibidas), resultado["estado"]) == (0, "escalado")


def test_si_no_termina_en_el_maximo_de_llamadas_escala(conexion, monkeypatch):
    """Un modelo que nunca responde no deja el bucle girando: al llegar al máximo, escala por regla.
    Técnico: no viene del curso (rag.md, patrón 08)."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    vueltas = [pide(("buscar_cliente", {})) for _ in range(agente.MAXIMO_LLAMADAS_POR_MENSAJE)]
    modelo = usar_modelo(monkeypatch, ModeloFalso(*vueltas))
    resultado = agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña")
    assert (len(modelo.recibidas), resultado["estado"]) == (agente.MAXIMO_LLAMADAS_POR_MENSAJE, "escalado")
    assert "no terminó" in leer_ticket(conexion, ticket)["motivo_escalamiento"]


def test_si_el_modelo_falla_escala(conexion, monkeypatch):
    """Si no se puede hablar con el modelo, el cliente no queda sin respuesta: se escala por regla.
    Curso: protocolos de escalamiento ante errores detectados (Módulo 2, sección 2.2);
    escalar por una falla del modelo es una regla del proyecto."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    modelo = usar_modelo(monkeypatch, ModeloFalso(TimeoutError("60 segundos sin respuesta")))
    resultado = agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña")
    assert (len(modelo.recibidas), resultado["estado"]) == (1, "escalado")
    assert "no se pudo hablar con el modelo" in leer_ticket(conexion, ticket)["motivo_escalamiento"]


def test_si_falla_una_herramienta_escala(conexion, monkeypatch):
    """Si la búsqueda falla (por ejemplo, sin red para el embedding), se escala por regla y el
    mensaje y los tokens ya gastados quedan guardados. Técnico: no viene del curso (decisión D11)."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")

    def buscar_que_falla(*argumentos, **opciones):
        raise ConnectionError("sin red")

    monkeypatch.setattr(herramientas, "buscar", buscar_que_falla)
    modelo = usar_modelo(monkeypatch, ModeloFalso(pide(("buscar_solucion", {"consulta": "contraseña"}))))
    resultado = agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña")
    datos = leer_ticket(conexion, ticket)
    assert (len(modelo.recibidas), resultado["estado"], datos["escalado_por"]) == (1, "escalado", "regla")
    assert "buscar_solucion falló" in datos["motivo_escalamiento"]
    assert datos["tokens_entrada"] == 100


@pytest.mark.parametrize("fin, texto", [("stop", "  "), ("length", "1. Entrar a la pág"), ("content_filter", "")])
def test_una_respuesta_vacia_o_incompleta_escala(conexion, monkeypatch, fin, texto):
    """Una respuesta vacía, cortada por largo o bloqueada por un filtro no llega al cliente: se escala por regla.
    Técnico: no viene del curso (revisión de la etapa 3, m3)."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    modelo = usar_modelo(monkeypatch, ModeloFalso(responde(texto, fin=fin)))
    resultado = agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña")
    assert (len(modelo.recibidas), resultado["estado"]) == (1, "escalado")
    assert leer_ticket(conexion, ticket)["escalado_por"] == "regla"


def test_un_ticket_escalado_no_vuelve_al_agente(conexion, monkeypatch):
    """Si una persona ya atiende el caso, el agente no llama al modelo; el mensaje y el aviso
    quedan en la conversación para ella. Curso: equipo híbrido (Módulo 4, sección 4.1) y punto
    de handoff (sección 4.3)."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    guardar_escalamiento(conexion, ticket, "prueba", "contexto", "regla")
    modelo = usar_modelo(monkeypatch, ModeloFalso())
    resultado = agente.atender_mensaje(conexion, ticket, "¿hay novedades?")
    assert resultado["respuesta"] == agente.MENSAJE_YA_ESCALADO
    assert modelo.recibidas == []
    assert leer_mensajes(conexion, ticket)[-2:] == [("cliente", "¿hay novedades?"), ("agente", agente.MENSAJE_YA_ESCALADO)]


def test_un_ticket_que_no_existe_da_un_error_claro(conexion):
    """Un número de ticket inexistente da un error que dice cuál. Técnico: no viene del curso."""
    with pytest.raises(ValueError, match="no existe"):
        agente.atender_mensaje(conexion, -1, "hola")


# --- Etapa 4: reglas en código, auditoría y kill switch ---

def test_cada_paso_queda_en_la_auditoria_con_la_version_y_la_huella(conexion, monkeypatch):
    """Cada paso del ticket queda en el registro de auditoría, numerado, con la versión y la huella de
    las instrucciones, el proveedor, el modelo y los fragmentos con la huella de su documento.
    Curso: audit trail con los criterios de decisión de cada caso (Módulo 1, pregunta 9); la huella es D15."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    usar_modelo(monkeypatch, ModeloFalso(
        pide(("buscar_solucion", {"consulta": "contraseña"})), responde("1. Entrar.\nFuente: restablecer-contrasena.md > Pasos")))
    agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña")
    pasos = leer_auditoria(conexion, ticket)
    assert [(numero, tipo, decision) for numero, tipo, decision, *_ in pasos] == [
        (1, "modelo", "pide herramientas"), (2, "herramienta", 'buscar_solucion("contraseña")'), (3, "modelo", "responde")]
    version = agente.leer_version_prompt(config.RUTA_PROMPT.read_text(encoding="utf-8"))
    assert all(paso[5] == version and len(paso[3]["huella_instrucciones"]) == 64 for paso in pasos)
    assert pasos[0][3]["proveedor"] == config.LLM_PROVEEDOR and "proveedor" not in pasos[1][3]  # solo en los del modelo
    assert pasos[1][3]["fragmentos"] == [["restablecer-contrasena.md", "Pasos", 0.8, "abc123"]]
    # El segundo mensaje sigue la numeración del ticket.
    usar_modelo(monkeypatch, ModeloFalso(responde("Pruebe otro navegador.")))
    agente.atender_mensaje(conexion, ticket, "sigue igual")
    assert leer_auditoria(conexion, ticket)[-1][0] == 4


def test_con_el_agente_detenido_el_ticket_pasa_a_una_persona(conexion, monkeypatch):
    """Con el kill switch activo, el agente no llama al modelo: el ticket pasa a una persona con el motivo.
    Curso: kill switch (Módulo 1, sección 1.2) y circuit breaker (Módulo 4, sección 4.5)."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    cambiar_detencion(conexion, agente.leer_agente(conexion)["id"], True, "prueba de detención")
    modelo = usar_modelo(monkeypatch, ModeloFalso())
    resultado = agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña")
    datos = leer_ticket(conexion, ticket)
    assert (len(modelo.recibidas), resultado["estado"], datos["escalado_por"]) == (0, "escalado", "regla")
    assert "agente detenido (prueba de detención)" == datos["motivo_escalamiento"]


def test_la_cancelacion_escala_sin_llamar_al_modelo(conexion, monkeypatch):
    """La cancelación la escala el código, sin depender de que el modelo la reconozca.
    Curso: el cliente que menciona cancelación pasa a una persona (Módulo 2, sección 2.5)."""
    ticket = nuevo_ticket(conexion, "quiero cancelar mi cuenta")
    modelo = usar_modelo(monkeypatch, ModeloFalso())
    resultado = agente.atender_mensaje(conexion, ticket, "quiero cancelar mi cuenta")
    assert (len(modelo.recibidas), resultado["estado"]) == (0, "escalado")
    assert leer_ticket(conexion, ticket)["motivo_escalamiento"] == "el cliente menciona cancelación"
    assert leer_auditoria(conexion, ticket)[0][1:3] == ("regla", "escalar_a_humano: el cliente menciona cancelación")


def test_una_respuesta_con_descuento_no_llega_al_cliente(conexion, monkeypatch):
    """Si el modelo ofrece un descuento, la respuesta no se envía: el ticket pasa a una persona, sin reintentos.
    Curso: "no ofrecer descuentos no autorizados" (Módulo 2, sección 2.5)."""
    ticket = nuevo_ticket(conexion, "la factura sale cortada")
    usar_modelo(monkeypatch, ModeloFalso(responde("Le ofrezco un 30% de descuento por las molestias.")))
    resultado = agente.atender_mensaje(conexion, ticket, "la factura sale cortada")
    assert resultado["estado"] == "escalado"
    assert "descuento" not in resultado["respuesta"]
    assert all("descuento" not in texto for _, texto in leer_mensajes(conexion, ticket))
    assert leer_ticket(conexion, ticket)["motivo_escalamiento"] == "respuesta bloqueada: la respuesta ofrece un descuento"


def test_si_pasa_el_tiempo_maximo_escala(conexion, monkeypatch):
    """Con el límite de tiempo vencido, el mensaje se escala por regla antes de llamar al modelo.
    Curso: escalar si el tiempo de resolución supera 8 minutos (Módulo 2, sección 2.5)."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    monkeypatch.setattr(config, "MINUTOS_MAXIMOS_ANTES_DE_ESCALAR", -1)  # bajo cero: sin depender del reloj
    modelo = usar_modelo(monkeypatch, ModeloFalso())
    resultado = agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña")
    assert (len(modelo.recibidas), resultado["estado"]) == (0, "escalado")
    assert "superó -1 minutos" in leer_ticket(conexion, ticket)["motivo_escalamiento"]


def test_sin_el_archivo_del_prompt_escala_sin_perder_el_mensaje(conexion, monkeypatch, tmp_path):
    """Si falta el archivo de instrucciones, el ticket se escala por regla y el mensaje queda guardado
    (revisión del prompt maestro, M6). Técnico: no viene del curso (decisión D11)."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    monkeypatch.setattr(config, "RUTA_PROMPT", tmp_path / "no-existe.md")
    modelo = usar_modelo(monkeypatch, ModeloFalso())
    resultado = agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña")
    assert (len(modelo.recibidas), resultado["estado"]) == (0, "escalado")
    assert leer_mensajes(conexion, ticket)[0] == ("cliente", "olvidé mi contraseña")


def test_detener_y_reactivar_quedan_en_la_auditoria(conexion):
    """Detener y reactivar el agente quedan en la auditoría como intervenciones, con quién y por qué,
    sin ticket. Curso: kill switch (Módulo 1, sección 1.2) y circuit breaker (Módulo 4, sección 4.5);
    registrarlo así es decisión del proyecto (D16)."""
    reglas.cambiar_kill_switch(conexion, True, "usuario-de-prueba", "deriva detectada")
    assert agente.leer_agente(conexion)["detenido"] is True
    reglas.cambiar_kill_switch(conexion, False, "usuario-de-prueba", "instrucciones corregidas")
    assert agente.leer_agente(conexion)["detenido"] is False
    cursor = conexion.cursor()
    cursor.execute("SELECT decision, motivo, quien FROM registro_auditoria WHERE ticket_id IS NULL ORDER BY id DESC LIMIT 2")
    assert list(cursor.fetchall())[::-1] == [["agente detenido", "deriva detectada", "usuario-de-prueba"],
                                       ["agente reactivado", "instrucciones corregidas", "usuario-de-prueba"]]


def test_escalar_vencidos(conexion):
    """Un mensaje del cliente sin respuesta por más de 8 minutos se escala; un ticket respondido que el
    cliente no confirmó en 24 horas queda 'resuelto_sin_confirmar'.
    Curso: los 8 minutos (Módulo 2, sección 2.5); no contar como resuelto lo que nadie confirmó es una
    regla del proyecto, inspirada en la tasa de resolución autónoma (Módulo 3, sección 3.2)."""
    reciente = nuevo_ticket(conexion, "no imprime")  # un mensaje reciente no se escala
    guardar_mensaje(conexion, reciente, "cliente", "no imprime")
    abandonado = nuevo_ticket(conexion, "no sincroniza")
    guardar_mensaje(conexion, abandonado, "cliente", "no sincroniza")
    sin_confirmar = nuevo_ticket(conexion, "factura cortada")
    guardar_mensaje(conexion, sin_confirmar, "cliente", "factura cortada")
    guardar_mensaje(conexion, sin_confirmar, "agente", "1. Elegir tamaño carta.")
    guardar_respuesta(conexion, sin_confirmar, "1. Elegir tamaño carta.")
    cursor = conexion.cursor()  # se envejecen los mensajes a mano: es una prueba, no código del agente
    cursor.execute("UPDATE mensajes SET creado_en = now() - interval '10 minutes' WHERE ticket_id = %s", (abandonado,))
    cursor.execute("UPDATE mensajes SET creado_en = now() - interval '25 hours' WHERE ticket_id = %s", (sin_confirmar,))
    escalados, marcados = reglas.escalar_vencidos(conexion)
    assert escalados >= 1 and marcados >= 1
    assert leer_ticket(conexion, abandonado)["estado"] == "escalado"
    assert leer_ticket(conexion, sin_confirmar)["estado"] == "resuelto_sin_confirmar"
    assert leer_ticket(conexion, reciente)["estado"] == "nuevo"
    # Revisar otra vez no vuelve a escalar el mismo ticket ni repite el aviso al cliente.
    avisos = len(leer_mensajes(conexion, abandonado))
    reglas.escalar_vencidos(conexion)
    assert len(leer_mensajes(conexion, abandonado)) == avisos


def test_el_kill_switch_a_mitad_del_mensaje_detiene_el_agente(conexion, monkeypatch):
    """Si alguien detiene el agente mientras atiende, la siguiente vuelta lo nota y escala con el motivo.
    Curso: kill switch (Módulo 1, sección 1.2)."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")

    def modelo_que_detiene(mensajes, definiciones, temperatura=None):  # simula a la persona que lo detiene a mitad
        cambiar_detencion(conexion, agente.leer_agente(conexion)["id"], True, "deriva detectada")
        return pide(("buscar_cliente", {}))

    monkeypatch.setattr(agente, "conversar_con_herramientas", modelo_que_detiene)
    resultado = agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña")
    assert resultado["estado"] == "escalado"
    assert leer_ticket(conexion, ticket)["motivo_escalamiento"] == "agente detenido (deriva detectada)"


@pytest.mark.parametrize("respuesta, motivo", [
    ("Listo, he cambiado tu plan a Empresa.", "cambio en la cuenta"),
    ("El cliente C-002 tuvo el mismo problema.", "otro cliente (C-002)"),
])
def test_una_respuesta_bloqueada_queda_en_la_auditoria(conexion, monkeypatch, respuesta, motivo):
    """Una respuesta que afirma un cambio de cuenta o nombra a otro cliente no llega al cliente del
    ticket (C-001) y su texto queda en la auditoría, para revisar después si fue un falso positivo.
    Curso: restricciones del SOP (Módulo 2, sección 2.5)."""
    ticket = nuevo_ticket(conexion, "no puedo entrar")
    usar_modelo(monkeypatch, ModeloFalso(responde(respuesta)))
    resultado = agente.atender_mensaje(conexion, ticket, "no puedo entrar")
    paso = leer_auditoria(conexion, ticket)[-1]
    assert resultado["estado"] == "escalado" and motivo in paso[4]
    assert paso[3]["texto_bloqueado"] == respuesta
    assert all(texto != respuesta for _, texto in leer_mensajes(conexion, ticket))


def test_un_error_de_la_base_en_una_herramienta_igual_escala(conexion, monkeypatch):
    """Si la base falla dentro de una herramienta, se vuelve al punto de retorno y el ticket se escala
    con el mensaje, los tokens y la auditoría guardados. Técnico: no viene del curso (D11)."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")

    def buscar_con_error(con, consulta):
        con.cursor().execute("SELECT 1 / 0")  # un error de PostgreSQL que aborta la transacción

    monkeypatch.setattr(herramientas, "buscar", buscar_con_error)
    usar_modelo(monkeypatch, ModeloFalso(pide(("buscar_solucion", {"consulta": "clave"}))))
    resultado = agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña")
    datos = leer_ticket(conexion, ticket)
    assert (resultado["estado"], datos["escalado_por"], datos["tokens_entrada"]) == ("escalado", "regla", 100)
    assert "buscar_solucion falló" in datos["motivo_escalamiento"]


def test_las_reglas_previas_al_modelo_llevan_version_y_huella(conexion, monkeypatch):
    """Un escalamiento por regla antes de llamar al modelo (la cancelación) también queda con la versión
    y la huella de las instrucciones, y sin proveedor ni modelo, porque no se llamó. D15."""
    ticket = nuevo_ticket(conexion, "quiero cancelar mi cuenta")
    usar_modelo(monkeypatch, ModeloFalso())
    agente.atender_mensaje(conexion, ticket, "quiero cancelar mi cuenta")
    paso = leer_auditoria(conexion, ticket)[0]
    assert paso[5] is not None and len(paso[3]["huella_instrucciones"]) == 64 and "modelo" not in paso[3]


def test_el_mensaje_guardado_antes_no_se_repite(conexion, monkeypatch):
    """Si quien llama ya guardó y confirmó el mensaje (para no perderlo si el programa se cae), el
    agente no lo guarda de nuevo. Técnico: no viene del curso (D11)."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    guardar_mensaje(conexion, ticket, "cliente", "olvidé mi contraseña")
    usar_modelo(monkeypatch, ModeloFalso(responde("1. Entrar.")))
    agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña", mensaje_ya_guardado=True)
    assert [quien for quien, _ in leer_mensajes(conexion, ticket)] == ["cliente", "agente"]

