"""Pruebas de integración de base_de_datos.py con el PostgreSQL de desarrollo, sin llamar al modelo.
Los vectores se escriben a mano y todo se deshace al final de cada prueba (fixture `conexion`)."""
from aplicacion import config
from aplicacion.base_de_datos import (
    buscar_fragmentos,
    contar_fragmentos,
    crear_ticket,
    guardar_fragmento,
    guardar_mensaje,
    leer_agente,
    leer_cliente,
    leer_mensajes,
    leer_ticket,
    sumar_tokens,
)

MODELO_DE_PRUEBA = "modelo-de-prueba"  # así la búsqueda solo ve los fragmentos de esta prueba (D8)


def vector(posicion):
    """Un vector de 768 números con un 1 en la posición indicada: dos vectores con el 1 en
    distinto lugar no se parecen nada. Técnico: no viene del curso."""
    numeros = [0.0] * 768
    numeros[posicion] = 1.0
    return numeros


def test_buscar_trae_primero_el_fragmento_mas_parecido(conexion, monkeypatch):
    """buscar_fragmentos() ordena por parecido y solo compara vectores del mismo modelo.
    Curso: responder con la solución documentada que corresponde (Módulo 2, sección 2.5)."""
    monkeypatch.setattr(config, "LLM_MODELO_EMBEDDINGS", MODELO_DE_PRUEBA)
    guardar_fragmento(conexion, "a.md", "Pasos", 0, "texto A", vector(0), "huella")
    guardar_fragmento(conexion, "b.md", "Pasos", 0, "texto B", vector(1), "huella")
    assert contar_fragmentos(conexion) == 2
    resultados = buscar_fragmentos(conexion, vector(1), cantidad=2)
    assert [fila[0] for fila in resultados] == ["b.md", "a.md"]
    assert round(resultados[0][3], 4) == 1.0


def test_el_registro_tiene_al_agente_con_lo_que_no_atiende(conexion):
    """El agente está en el registro con su lista de lo que no atiende y sin detener.
    Curso: registro de agentes (Módulo 2, sección 2.7)."""
    agente = leer_agente(conexion)
    assert agente["nombre"] == "Agente de Soporte N1"
    assert "Cancelaciones" in agente["fuera_de_alcance"]
    assert agente["detenido"] is False


def test_leer_cliente_por_codigo_o_por_id(conexion):
    """El CRM simulado se lee por el código que da el cliente o por el id interno.
    Curso: el agente lee el CRM, sin poder cambiarlo (Módulo 2, sección 2.3)."""
    cliente = leer_cliente(conexion, codigo="C-001")
    assert cliente["nombre"] == "Ana Torres"
    assert leer_cliente(conexion, cliente_id=cliente["id"]) == cliente
    assert leer_cliente(conexion, codigo="C-999") is None


def test_un_ticket_guarda_su_conversacion_y_sus_tokens(conexion):
    """Un ticket nuevo empieza en 'nuevo', guarda sus mensajes en orden y acumula tokens y costo.
    Curso: indicadores y costo por caso (Módulo 3, sección 3.2)."""
    agente = leer_agente(conexion)
    cliente = leer_cliente(conexion, codigo="C-002")
    ticket_id = crear_ticket(conexion, agente["id"], cliente["id"], "no sincroniza")
    guardar_mensaje(conexion, ticket_id, "cliente", "no sincroniza")
    guardar_mensaje(conexion, ticket_id, "agente", "pruebe esto")
    sumar_tokens(conexion, ticket_id, 100, 10, 0.5)
    sumar_tokens(conexion, ticket_id, 200, 20, 0.25)
    ticket = leer_ticket(conexion, ticket_id)
    assert ticket["estado"] == "nuevo"
    assert (ticket["tokens_entrada"], ticket["tokens_salida"], float(ticket["costo_tokens"])) == (300, 30, 0.75)
    assert leer_mensajes(conexion, ticket_id) == [("cliente", "no sincroniza"), ("agente", "pruebe esto")]
