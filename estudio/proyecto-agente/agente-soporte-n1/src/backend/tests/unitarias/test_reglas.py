"""Pruebas unitarias de las reglas en código (aplicacion/reglas.py): lo que el agente cumple siempre,
sin depender del modelo. No usan la red ni la base de datos."""
import time

import pytest

from aplicacion import config, reglas


@pytest.mark.parametrize("texto", [
    "quiero cancelar mi cuenta", "Necesito la CANCELACIÓN del servicio", "quiero darme de baja",
    "por favor, anular mi suscripción", "voy a terminar el contrato", "quiero cerrar mi cuenta",
    "no quiero renovar", "quiero desuscribirme", "¿cómo hago para cancelar?"])
def test_la_cancelacion_siempre_escala(texto):
    """Cualquier forma de pedir la cancelación escala, con o sin tildes y mayúsculas.
    Curso: el cliente que menciona cancelación pasa a una persona (Módulo 2, sección 2.5)."""
    assert reglas.revisar_entrada(texto) == "el cliente menciona cancelación"


def test_un_mensaje_normal_pasa_y_uno_demasiado_largo_escala():
    """Un problema técnico pasa al modelo; un mensaje más largo que el máximo no se envía.
    Técnico: el largo máximo no viene del curso (rag.md, guardrails de entrada)."""
    assert reglas.revisar_entrada("olvidé mi contraseña") is None
    assert "supera" in reglas.revisar_entrada("a" * (reglas.MAXIMO_CARACTERES_MENSAJE + 1))


@pytest.mark.parametrize("respuesta, motivo", [
    ("Como compensación le ofrezco un 20% de descuento.", "descuento"),
    ("Le damos un mes gratis.", "descuento"),
    ("Te aplicamos una rebaja en la próxima factura.", "descuento"),
    ("Listo, he cambiado tu plan a Empresa.", "cambio en la cuenta"),
    ("Ya cancelé tu suscripción.", "cambio en la cuenta"),
    ("Su cuenta fue actualizada.", "cambio en la cuenta"),
    ("He procesado el reembolso.", "cambio en la cuenta"),
    ("El cliente C-002 tuvo el mismo problema.", "otro cliente (C-002)"),
    ("El cliente c 003 también.", "otro cliente (C-003)"),
])
def test_la_respuesta_no_puede_romper_las_restricciones(respuesta, motivo):
    """Una respuesta que ofrece descuentos, afirma un cambio de cuenta o nombra a otro cliente no se envía.
    Curso: restricciones del SOP (Módulo 2, sección 2.5); revisar la salida antes de que llegue al
    cliente está inspirado en los puntos de verificación obligatoria (Módulo 3, sección 3.3)."""
    assert motivo in reglas.revisar_respuesta(respuesta, "C-001")


@pytest.mark.parametrize("texto", [
    "Hola, C-001. 1. Entre a la página de inicio de sesión.\nFuente: restablecer-contrasena.md > Pasos",
    "1. Actualice su aplicación. 2. Elimine su caché. 3. Cambie su contraseña desde Configuración.",
    "No ofrecemos descuentos ni reembolsos; una persona revisará el cobro.",
    "Si la aplicación se ha actualizado, reinicie el equipo.",
    "Hola C001, siga estos pasos.",
])
def test_una_respuesta_normal_pasa(texto):
    """Las indicaciones al cliente (“Actualice su aplicación”), una negación (“no ofrecemos
    descuentos”) o el código del propio cliente no se bloquean: la regla busca ofrecer o afirmar,
    no mencionar. Curso: el agente resuelve con soluciones documentadas (Módulo 2, sección 2.5)."""
    assert reglas.revisar_respuesta(texto, "C-001") is None


@pytest.mark.parametrize("texto", ["Ya cancelé la factura pero sigue pendiente", "se canceló la impresión",
                                   "olvidé mi contraseña"])
def test_cancelar_sin_intencion_de_baja_no_escala(texto):
    """“Ya cancelé la factura” es haberla pagado (Chile y buena parte de Latinoamérica), y “se canceló
    la impresión” no es pedir la baja: pasan al modelo, que igual puede escalar (decisión del usuario, D16)."""
    assert reglas.revisar_entrada(texto) is None


def test_tiempo_excedido(monkeypatch):
    """Con el límite bajo cero, cualquier atención ya se pasó; con 8, una recién empezada no.
    Curso: escalar si el tiempo de resolución supera 8 minutos (Módulo 2, sección 2.5)."""
    inicio = time.monotonic() - 1
    monkeypatch.setattr(config, "MINUTOS_MAXIMOS_ANTES_DE_ESCALAR", -1)
    assert reglas.tiempo_excedido(inicio) is True
    monkeypatch.setattr(config, "MINUTOS_MAXIMOS_ANTES_DE_ESCALAR", 8)
    assert reglas.tiempo_excedido(inicio) is False


def test_agente_detenido():
    """El kill switch es la columna detenido del registro de agentes.
    Curso: kill switch (Módulo 1, sección 1.2) y circuit breaker (Módulo 4, sección 4.5)."""
    assert reglas.agente_detenido({"detenido": True}) is True
    assert reglas.agente_detenido({"detenido": False}) is False
