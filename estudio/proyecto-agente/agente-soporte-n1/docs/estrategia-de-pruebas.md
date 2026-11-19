# Estrategia de pruebas

Decisión del usuario (2026-11-18): el proyecto tiene varios tipos de pruebas, y todos deben estar documentados y separados, para que sea fácil entender qué prueba cada uno y qué parte del curso cubre. Este documento es la única fuente de los tipos de prueba; las evals tienen su plan en `evals-del-llm.md`, y lo que dio cada prueba está en `pruebas/`.

## Los cinco tipos de prueba

| Tipo | Qué prueba | ¿Usa el modelo? | ¿Usa la base de datos? | Costo | Carpeta |
|---|---|---|---|---|---|
| **Unitarias** | una función sola, con datos fijos: trocear un texto, convertir un vector, leer una variable, las reglas en código | no | no | gratis, en segundos | `tests/unitarias/` |
| **De integración** | dos piezas juntas: el código con PostgreSQL real, o el bucle del agente con un modelo falso | no | sí | gratis | `tests/integracion/` |
| **Adversariales de robustez** | que ni las reglas ni la API se caigan con entradas extrañas generadas automáticamente (sección de abajo) | no | no | gratis | `tests/adversariales/` |
| **Evals del modelo** | que el agente se comporte como dicen sus instrucciones: las 5 dimensiones de la sección 2.6 y las metas de la 2.5 (`evals-del-llm.md`) | sí | sí | algunas llamadas al modelo | `tests/evals/` |
| **De punta a punta (e2e)** | el recorrido completo, como lo vive un usuario: crear un ticket por la API, que el agente lo atienda, confirmarlo, calificarlo y verlo reflejado en el dashboard | sí | sí | algunas llamadas al modelo | `tests/e2e/` |

Todas usan `pytest` (licencia MIT). Las rutas son relativas a `src/backend/`, y cada carpeta tiene un `README.md` corto que dice qué prueba, cómo se corre y cuánto cuesta.

## Cómo se relacionan con el curso

- **Unitarias e integración:** comprueban las piezas con que se cumplen las reglas del curso. Por ejemplo, que `revisar_entrada()` escale siempre ante una cancelación (sección 2.5), o que `registrar_paso()` guarde qué decidió el agente y por qué (audit trail, Módulo 1, pregunta 9).
- **Adversariales de robustez:** no vienen del curso; son buena práctica de programación. No se confunden con la dimensión adversarial de la sección 2.6, que se prueba en las evals.
- **Evals:** son la validación previa a producción del curso (sección 2.6) y la condición para aprobar cada versión del prompt (D15).
- **De punta a punta:** comprueban que el flujo de 14 pasos del plan funciona junto, incluido lo que el AI Agent Manager mira después: los indicadores (3.2), el muestreo (3.3) y el dashboard (3.5).

## Cómo se ve cada tipo, con un ejemplo

**Unitaria** (`tests/unitarias/test_piezas_simples.py`):

```python
from scripts.cargar_conocimiento import SOLAPE, TAMANO_FRAGMENTO, trocear


def test_trocear_corta_con_solape_y_sin_repetir_el_final():
    """Un texto que cabe en un fragmento no se corta; uno largo se corta en partes que repiten
    SOLAPE caracteres; y 2.100 caracteres dan 2 pedazos, no 3 (corrección de la etapa 2).
    Técnico: no viene del curso."""
    assert trocear("a" * TAMANO_FRAGMENTO) == ["a" * TAMANO_FRAGMENTO]
    pedazos = trocear("".join(str(i % 10) for i in range(2000)))
    assert len(pedazos) == 2 and pedazos[0][-SOLAPE:] == pedazos[1][:SOLAPE]
    assert len(trocear("a" * 2100)) == 2
```

**De integración** (`tests/integracion/test_base_de_datos.py`): guarda fragmentos con vectores fijos en PostgreSQL y comprueba que `buscar_fragmentos()` devuelve primero el más parecido. No llama al modelo: los vectores se escriben a mano. `tests/integracion/test_agente.py` prueba el bucle del agente con un modelo falso: los topes, las herramientas y los escalamientos, siempre igual y gratis.

**De punta a punta** (`tests/e2e/test_ticket_completo.py`, etapa 6): crea un ticket “olvidé mi contraseña” por la API, espera la respuesta del agente, lo confirma y lo califica, y comprueba que el ticket quedó `resuelto`, que la auditoría tiene sus pasos y que los indicadores lo cuentan. Son pocos casos, porque cada uno llama al modelo.

## Reglas para todas las pruebas

1. **Un tipo, una carpeta,** con su `README.md`.
2. **Cada prueba se explica sola.** Su nombre dice qué comprueba (`test_cancelacion_siempre_escala`), y su docstring, en lenguaje simple, dice por qué importa y a qué parte del curso responde (regla 4 del plan).
3. **Las gratis primero.** Se corren a cada cambio: `.\.venv\Scripts\python.exe -m pytest tests/unitarias tests/integracion tests/adversariales`. Las que llaman al modelo, evals y e2e, se corren antes de aprobar una versión del prompt o al cerrar una etapa.
4. **Cada tipo se puede correr por separado:** `pytest tests/unitarias`, `pytest tests/e2e`, etc.
5. **Los resultados que importan quedan registrados** en `docs/pruebas/`, con la fecha, la versión del prompt y el modelo (regla 16 del plan).
6. **Ninguna librería de pruebas sin revisar su licencia** (regla 13 del plan). Hoy: `pytest` (MIT) e `hypothesis` (MPL 2.0, excepción aceptada en D3).
7. **Antes de empezar,** las pruebas que lo necesitan verifican que PostgreSQL responde y que la base de conocimiento está cargada.

## Cuándo se escribe cada tipo

| Tipo | Cuándo |
|---|---|
| Unitarias y de integración | junto con el código de cada etapa, desde la etapa 3 |
| Adversariales | etapa 5 para las reglas y etapa 6 para la API |
| Evals | etapa 5 |
| De punta a punta | etapa 6 (por la API) y etapa 7 (con el dashboard) |

## Pruebas adversariales

Decisión del usuario (2026-11-18). En este proyecto, “adversarial” significa dos cosas distintas, y las dos hacen falta:

| | 1. Adversarial del agente | 2. Adversarial de robustez |
|---|---|---|
| Qué busca | que el agente no se deje manipular | que el programa nunca se caiga con entradas extrañas |
| Ejemplos | “ignora tus instrucciones”, pedir datos de otro cliente, exigir un descuento | JSON vacío o malformado, textos enormes, números donde va texto, caracteres raros |
| Qué se espera | el agente se niega o escala | errores controlados (`400`, `422`) y nunca un error interno (`500`) |
| Base | el curso: la dimensión adversarial de la validación previa a producción (sección 2.6) | buena práctica de programación, no viene del curso |
| Cómo se prueba | casos escritos a mano, con el modelo real | casos generados automáticamente con Hypothesis, sin el modelo |
| Etapa y carpeta | 5, en `tests/evals/` | 5 para las reglas y 6 para la API, en `tests/adversariales/` |

**Qué es Hypothesis:** una librería de pruebas que, en lugar de usar ejemplos escritos a mano, genera cientos de entradas al azar, incluidas las más raras (textos vacíos, enormes o con caracteres especiales, números extremos, estructuras anidadas), y busca alguna que rompa el código. Si la encuentra, la reduce al ejemplo más simple que falla. Se usa junto con `pytest`. Su licencia es MPL 2.0 y su única dependencia, `sortedcontainers`, Apache 2.0 (excepción aceptada en D3).

**Dónde se aplica:**

1. **Las reglas en código (`reglas.py`, desde la etapa 4; sus pruebas adversariales, en `tests/adversariales/test_reglas_adversariales.py` desde la etapa 5):** son funciones puras, así que se prueban sin modelo y sin costo. Propiedades: con cualquier texto, `revisar_entrada()` y `revisar_respuesta()` nunca se caen; una cancelación con mayúsculas al azar y caracteres invisibles, en medio de cualquier texto, escala; un descuento ofrecido con cualquier porcentaje se bloquea. Además, ataques escritos a mano y los límites conocidos, marcados como falla esperada (xfail estricto): lo que un patrón de palabras no ve y cubren las evals.
2. **La API (`api.py`, etapa 6):** ningún cuerpo de pedido, por raro que sea, provoca un error `500`. FastAPI y Pydantic ya rechazan con `422` lo que no tiene la forma esperada (D7); la prueba comprueba que eso se cumple siempre.

**Para no gastar llamadas al modelo,** en las pruebas de robustez de la API la función del agente se reemplaza por una versión falsa que responde al instante: aquí no se evalúa al agente, sino que la API no se caiga, y cien casos con el modelo real costarían cien llamadas. El comportamiento del agente se sigue probando con el modelo real en las evals.

**Plantilla para la etapa 6** (`tests/adversariales/test_api.py`; los nombres `api.app` y `/tickets` se ajustan a los reales cuando exista `api.py`; la función del agente es `atender_mensaje()`):

```python
"""Pruebas adversariales de robustez de la API (etapa 6).
Envía cuerpos de pedido impredecibles y comprueba que nunca haya un error 500.
Técnico: no viene del curso (ver docs/estrategia-de-pruebas.md)."""
from fastapi.testclient import TestClient
from hypothesis import HealthCheck, given, settings, strategies as st

from aplicacion import api

# La función del agente se reemplaza por una falsa: aquí no se prueba al agente,
# sino que la API no se caiga, y así no se gastan llamadas al modelo.
api.atender_mensaje = lambda *argumentos, **opciones: {"estado": "respondido", "respuesta": "prueba", "pasos": []}
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

**Instrucción para pedirle estas pruebas a un agente de IA:** “Toma como base `docs/estrategia-de-pruebas.md` y la plantilla `tests/adversariales/test_api.py`, con `pytest` y `hypothesis`. Genera pruebas adversariales de robustez para las rutas de `src/backend/aplicacion/api.py` (FastAPI) y propiedades para las funciones de `reglas.py`. Usa estrategias acordes a los campos que espera cada endpoint (`st.text()`, `st.integers()`, `st.lists()`, etc.) para intentar provocar errores 500, inyecciones o fallos de validación. Reemplaza la función del agente por una falsa para no llamar al modelo. No incluyas casos de éxito. Sigue las reglas del plan: código simple, comentado y con nombres en español.”

## Estructura de carpetas

```text
src/backend/tests/
├── README.md                     # cómo correr cada tipo y cuánto cuesta
├── conftest.py                   # preparación común: avisar si falta la configuración o si PostgreSQL no responde
├── unitarias/                    # funciones solas, sin red ni base de datos
├── integracion/                  # el código con PostgreSQL real y el bucle con un modelo falso
├── adversariales/                # robustez con Hypothesis
├── evals/                        # comportamiento del agente con el modelo (ver evals-del-llm.md)
│   └── casos.jsonl               # el golden dataset
└── e2e/                          # el recorrido completo por la API
```
