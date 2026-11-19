# Estrategia de pruebas adversariales

Decisión del usuario (2026-11-18): las pruebas del proyecto incluyen pruebas adversariales, documentadas aquí para no olvidarlas al llegar a las etapas 5 y 6. El usuario aportó un ejemplo con Flask y Hypothesis; este documento lo adapta a FastAPI, que es lo que usa el proyecto (decisión D7), y lo conecta con lo que pide el curso.

## Dos tipos de prueba adversarial

En este proyecto, “adversarial” significa dos cosas distintas, y las dos hacen falta:

| | 1. Adversarial del agente | 2. Adversarial de robustez |
|---|---|---|
| Qué busca | que el agente no se deje manipular | que el programa nunca se caiga con entradas extrañas |
| Ejemplos | “ignora tus instrucciones”, pedir datos de otro cliente, exigir un descuento | JSON vacío o malformado, textos enormes, números donde va texto, caracteres raros |
| Qué se espera | el agente se niega o escala | errores controlados (`400`, `422`) y nunca un error interno (`500`) |
| Base | el curso: la dimensión adversarial de la validación previa a producción (Módulo 2, sección 2.6) | buena práctica de programación, no viene del curso |
| Cómo se prueba | casos escritos a mano, con el modelo real | casos generados automáticamente con Hypothesis, sin el modelo |
| Etapa y carpeta | 5, en `tests/evals/` | 5 para las reglas y 6 para la API, en `tests/adversariales/` |

## Qué es Hypothesis

Es una librería de pruebas que, en lugar de usar ejemplos escritos a mano, genera cientos de entradas al azar, incluidas las más raras (textos vacíos, enormes o con caracteres especiales, números extremos, estructuras anidadas), y busca alguna que rompa el código. Si la encuentra, la reduce al ejemplo más simple que falla y lo muestra. Se usa junto con `pytest`.

**Licencia:** MPL 2.0, la misma de `certifi` y `tqdm`. Su única dependencia obligatoria, `sortedcontainers`, es Apache 2.0. El usuario la aceptó el 2026-11-18 como excepción a la regla 13 del plan, porque no se modifica (ver `decisiones.md`, D3).

## Dónde se aplica en el proyecto

1. **Las reglas en código (`reglas.py`, etapa 5):** son funciones puras, así que se prueban sin modelo y sin costo. Ejemplos de propiedades:
   - con cualquier texto, `revisar_entrada()` nunca se cae;
   - cualquier texto que contenga “cancelar” en cualquier forma (mayúsculas, tildes, palabras alrededor) termina en escalamiento;
   - ninguna respuesta que ofrezca un descuento pasa `revisar_respuesta()`.
2. **La API (`api.py`, etapa 6):** ningún cuerpo de pedido, por raro que sea, provoca un error `500`. FastAPI y Pydantic ya rechazan con `422` lo que no tiene la forma esperada; la prueba comprueba que eso se cumple siempre.

**Para no gastar llamadas al modelo:** en las pruebas de robustez de la API, la función del agente se reemplaza por una versión falsa que responde al instante. Es una excepción a la decisión de probar sin respuestas simuladas: aquí no se evalúa el comportamiento del agente, sino que la API no se caiga, y cien casos con el modelo real costarían cien llamadas. El comportamiento del agente se sigue probando con el modelo real en el grupo 2.

## Plantilla adaptada a FastAPI (`src/backend/tests/adversariales/test_api.py`)

```python
"""Pruebas adversariales de robustez de la API (etapa 6).
Envía cuerpos de pedido impredecibles y comprueba que nunca haya un error 500.
Técnico: no viene del curso (ver docs/pruebas-adversariales.md)."""
from fastapi.testclient import TestClient
from hypothesis import HealthCheck, given, settings, strategies as st

from aplicacion import api

# La función del agente se reemplaza por una falsa: aquí no se prueba al agente,
# sino que la API no se caiga, y así no se gastan llamadas al modelo.
api.atender_ticket = lambda *argumentos, **opciones: {"estado": "respondido", "respuesta": "prueba"}
cliente = TestClient(api.app)

# Estructuras JSON caóticas: vacías, anidadas, con números extremos y textos raros.
json_adversarial = st.recursive(
    st.none() | st.booleans() | st.integers() | st.floats(allow_nan=True, allow_infinity=True) | st.text(),
    lambda hijos: st.lists(hijos, max_size=5) | st.dictionaries(st.text(), hijos, max_size=5),
    max_leaves=10,
)


@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(cuerpo=json_adversarial)
def test_crear_ticket_nunca_falla_con_500(cuerpo):
    """Ningún cuerpo de pedido debe provocar un error interno del servidor."""
    respuesta = cliente.post("/tickets", json=cuerpo)
    assert respuesta.status_code != 500, f"Error 500 con el cuerpo: {cuerpo!r}"
```

Los nombres `api.app`, `api.atender_ticket` y `/tickets` se ajustan a los reales cuando exista `api.py`.

## Ejemplo original del usuario, con Flask (referencia)

```python
import pytest
from hypothesis import given, settings, HealthCheck, strategies as st
from app import app  # Ajustar según la estructura del proyecto

@pytest.fixture(scope="module")
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# Estrategia para generar payloads JSON caóticos
json_adversarial = st.recursive(
    st.none() | st.booleans() | st.floats(allow_nan=True, allow_infinity=True) | st.text(),
    lambda children: st.lists(children, max_size=5) | st.dictionaries(st.text(), children, max_size=5),
    max_leaves=10
)

@settings(
    max_examples=100, # Cantidad de ataques por ejecución
    suppress_health_check=[HealthCheck.function_scoped_fixture]
)
@given(payload=json_adversarial)
def test_endpoint_resiliencia_json(client, payload):
    """Envía estructuras JSON impredecibles para intentar provocar un HTTP 500."""
    response = client.post("/api/tu-endpoint", json=payload)

    assert response.status_code != 500, f"Fallo crítico con payload: {payload}"
```

## Instrucción para pedirle estas pruebas a un agente de IA

Adaptada del ejemplo del usuario a este proyecto:

> “Toma como base `docs/pruebas-adversariales.md`, `docs/estrategia-de-pruebas.md` y la plantilla `tests/adversariales/test_api.py`, con `pytest` y `hypothesis`. Genera pruebas adversariales de robustez para las rutas de `src/backend/aplicacion/api.py` (FastAPI) y propiedades para las funciones de `reglas.py`. Usa estrategias acordes a los campos que espera cada endpoint (`st.text()`, `st.integers()`, `st.lists()`, etc.) para intentar provocar errores 500, inyecciones o fallos de validación. Reemplaza la función del agente por una falsa para no llamar al modelo. No incluyas casos de éxito. Sigue las reglas del plan: código simple, comentado y con nombres en español.”
