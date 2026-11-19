"""Pruebas de integración del bucle del agente (agente.py) con PostgreSQL real y un modelo falso.

El modelo falso devuelve respuestas escritas de antemano, así se prueba gratis y siempre igual
lo que controla el código: herramientas, escalamientos, tope de tokens y tope de llamadas.
Cada prueba revisa cuántas veces se llamó al modelo: si el agente lo llamara de más, el
error del modelo falso se convertiría en un escalamiento y pasaría inadvertido.
Cómo se comporta el modelo real se prueba en las evals (etapa 5).
"""
import json

import pytest

from aplicacion import agente, config, herramientas
from aplicacion.base_de_datos import (
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

    def __call__(self, mensajes, definiciones):
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
        ("restablecer-contrasena.md", "Pasos", "1. Entrar a la página de inicio de sesión.", 0.8)])


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
    ticket = nuevo_ticket(conexion, "quiero cancelar")
    modelo = usar_modelo(monkeypatch, ModeloFalso(
        pide(("buscar_cliente", {})),
        pide(("escalar_a_humano", {"motivo": "pide cancelar", "resumen": "quiere cancelar su cuenta"}))))
    resultado = agente.atender_mensaje(conexion, ticket, "quiero cancelar")
    assert len(modelo.recibidas) == 2
    assert resultado["estado"] == "escalado"
    assert resultado["respuesta"] == herramientas.MENSAJE_ESCALADO.format(ticket=ticket)
    datos = leer_ticket(conexion, ticket)
    assert (datos["estado"], datos["escalado_por"], datos["motivo_escalamiento"]) == ("escalado", "modelo", "pide cancelar")
    for parte in ("C-001", "Ana Torres", "quiere cancelar su cuenta", "buscar_cliente, escalar_a_humano", "Cliente: quiero cancelar"):
        assert parte in datos["resumen_escalamiento"]


def test_escalar_se_atiende_antes_que_otras_herramientas(conexion, monkeypatch):
    """Si en un mismo mensaje el modelo pide buscar y escalar, escala sin pagar antes la búsqueda.
    Técnico: no viene del curso (revisión de la etapa 3, m1)."""
    ticket = nuevo_ticket(conexion, "quiero cancelar")
    llamadas_a_buscar = []
    monkeypatch.setattr(herramientas, "buscar", lambda *a, **k: llamadas_a_buscar.append(a) or [])
    modelo = usar_modelo(monkeypatch, ModeloFalso(pide(
        ("buscar_solucion", {"consulta": "cancelar"}), ("escalar_a_humano", {"motivo": "cancelación", "resumen": "x"}))))
    resultado = agente.atender_mensaje(conexion, ticket, "quiero cancelar")
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
    Técnico: no viene del curso (buenas-practicas.md, patrón 08)."""
    ticket = nuevo_ticket(conexion, "quiero cancelar")
    modelo = usar_modelo(monkeypatch, ModeloFalso(
        pide(("escalar_a_humano", {"motivo": "cancelación"})),
        pide(("escalar_a_humano", {"motivo": "cancelación", "resumen": "pide cancelar"}))))
    resultado = agente.atender_mensaje(conexion, ticket, "quiero cancelar")
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
    Técnico: no viene del curso (buenas-practicas.md, patrón 08)."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    monkeypatch.setattr(config, "TOPE_TOKENS_POR_TICKET", 500)
    modelo = usar_modelo(monkeypatch, ModeloFalso(pide(("buscar_cliente", {}), tokens=600)))
    resultado = agente.atender_mensaje(conexion, ticket, "olvidé mi contraseña")
    datos = leer_ticket(conexion, ticket)
    assert (len(modelo.recibidas), resultado["estado"], datos["escalado_por"]) == (1, "escalado", "regla")
    assert "tope de 500 tokens" in datos["motivo_escalamiento"]
    assert "Herramientas usadas: ninguna" in datos["resumen_escalamiento"]


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
    Técnico: no viene del curso (buenas-practicas.md, patrón 08)."""
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


def test_la_respuesta_no_pisa_un_ticket_escalado(conexion):
    """guardar_respuesta() no devuelve a 'respondido' un ticket que ya tomó una persona.
    Técnico: no viene del curso (revisión de la etapa 3, m8)."""
    ticket = nuevo_ticket(conexion, "olvidé mi contraseña")
    guardar_escalamiento(conexion, ticket, "prueba", "contexto", "regla")
    guardar_respuesta(conexion, ticket, "respuesta tardía")
    assert leer_ticket(conexion, ticket)["estado"] == "escalado"


def test_un_ticket_que_no_existe_da_un_error_claro(conexion):
    """Un número de ticket inexistente da un error que dice cuál. Técnico: no viene del curso."""
    with pytest.raises(ValueError, match="no existe"):
        agente.atender_mensaje(conexion, -1, "hola")
