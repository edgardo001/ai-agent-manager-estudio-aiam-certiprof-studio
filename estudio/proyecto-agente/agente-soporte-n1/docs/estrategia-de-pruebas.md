# Estrategia de pruebas

Decisión del usuario (2026-11-18): el proyecto tiene varios tipos de pruebas, y todos deben estar documentados y separados, para que sea fácil entender qué prueba cada uno y qué parte del curso cubre. Este documento es el punto de partida; los tipos con más detalle tienen su propio documento.

## Los cinco tipos de prueba

| Tipo | Qué prueba | ¿Usa el modelo? | ¿Usa la base de datos? | Costo | Carpeta | Detalle |
|---|---|---|---|---|---|---|
| **Unitarias** | una función sola, con datos fijos: trocear un texto, convertir un vector, leer una variable, las reglas en código | no | no | gratis, en segundos | `tests/unitarias/` | este documento |
| **De integración** | dos piezas juntas: el código con PostgreSQL real (guardar y buscar fragmentos, registrar un paso de auditoría) | no; los vectores son fijos | sí | gratis | `tests/integracion/` | este documento |
| **Adversariales de robustez** | que ni las reglas ni la API se caigan con entradas extrañas generadas automáticamente | no | no | gratis | `tests/adversariales/` | `pruebas-adversariales.md` |
| **Evals del modelo** | que el agente se comporte como dicen sus instrucciones: las 5 dimensiones de la sección 2.6 y las metas de la 2.5 | sí | sí | algunas llamadas al modelo | `tests/evals/` | `evals-del-llm.md` |
| **De punta a punta (e2e)** | el recorrido completo, como lo vive un usuario: crear un ticket por la API, que el agente lo atienda, confirmarlo, calificarlo y verlo reflejado en el dashboard | sí | sí | algunas llamadas al modelo | `tests/e2e/` | este documento |

Todas usan `pytest` (licencia MIT). Las rutas son relativas a `src/backend/`.

## Cómo se relacionan con el curso

- **Unitarias e integración:** comprueban las piezas con que se cumplen las reglas del curso. Por ejemplo, que `revisar_entrada()` escale siempre ante una cancelación (sección 2.5), o que `registrar_paso()` guarde qué decidió el agente y por qué (audit trail, Módulo 1, pregunta 9).
- **Adversariales de robustez:** no vienen del curso; son buena práctica de programación. No se confunden con la dimensión adversarial de la sección 2.6, que se prueba en las evals.
- **Evals:** son la validación previa a producción del curso (sección 2.6) y la condición para aprobar cada versión del prompt.
- **De punta a punta:** comprueban que el flujo completo de 14 pasos del plan funciona junto, incluido lo que el AI Agent Manager mira después: los indicadores (3.2), el muestreo (3.3) y el dashboard (3.5).

## Cómo se ve cada tipo, con un ejemplo

**Unitaria** (`tests/unitarias/test_cargar_conocimiento.py`):

```python
from scripts.cargar_conocimiento import SOLAPE, TAMANO_FRAGMENTO, trocear


def test_trocear_un_texto_largo_se_solapa():
    """Un texto más largo que un fragmento se corta en partes que repiten SOLAPE caracteres.
    Técnico: no viene del curso; prueba el corte de los documentos (decisión D8)."""
    texto = "a" * 2000
    fragmentos = trocear(texto)
    assert len(fragmentos) == 2
    assert fragmentos[0][-SOLAPE:] == fragmentos[1][:SOLAPE]
```

**De integración** (`tests/integracion/test_base_de_conocimiento.py`): guarda dos fragmentos con vectores fijos en PostgreSQL y comprueba que `buscar_fragmentos()` devuelve primero el más parecido. No llama al modelo: los vectores se escriben a mano.

**De punta a punta** (`tests/e2e/test_ticket_completo.py`): con PostgreSQL levantado y la base de conocimiento cargada, crea un ticket “olvidé mi contraseña” por la API, espera la respuesta del agente, lo confirma y lo califica, y comprueba que el ticket quedó `resuelto`, que la auditoría tiene sus pasos y que los indicadores del dashboard lo cuentan. Son pocos casos, porque cada uno llama al modelo.

## Reglas para todas las pruebas

1. **Un tipo, una carpeta.** Cada carpeta tiene un `README.md` corto que dice qué prueba, cómo se corre y cuánto cuesta.
2. **Cada prueba se explica sola.** Su nombre dice qué comprueba (`test_cancelacion_siempre_escala`), y su docstring, en lenguaje simple, dice por qué importa y a qué parte del curso responde, como el resto del código (regla 4 del plan).
3. **Las gratis primero.** Se corren a cada cambio: `pytest tests/unitarias tests/integracion tests/adversariales`. Las que llaman al modelo, evals y e2e, se corren antes de aprobar una versión del prompt o al cerrar una etapa.
4. **Cada tipo se puede correr por separado:** `pytest tests/unitarias`, `pytest tests/e2e`, etc.
5. **Los resultados que importan quedan registrados** en `docs/pruebas/`, con la fecha, la versión del prompt y el modelo.
6. **Ninguna librería de pruebas sin revisar su licencia** (regla 13 del plan). Hoy: `pytest` (MIT) e `hypothesis` (MPL 2.0, aceptada como excepción).

## Cuándo se escribe cada tipo

| Tipo | Cuándo |
|---|---|
| Unitarias | junto con el código de cada etapa, desde la etapa 3; las del código de las etapas 0 a 2 se escriben al empezar la etapa 3 |
| De integración | junto con el código que usa la base de datos, desde la etapa 3 |
| Adversariales | etapa 5 para las reglas y etapa 6 para la API |
| Evals | etapa 5 |
| De punta a punta | etapa 6 (por la API) y etapa 7 (con el dashboard) |

## Estructura de carpetas

```text
src/backend/tests/
├── README.md                     # cómo correr cada tipo y cuánto cuesta
├── conftest.py                   # preparación común: avisar si falta el .env o si PostgreSQL no responde
├── unitarias/                    # funciones solas, sin red ni base de datos
├── integracion/                  # el código con PostgreSQL real, sin modelo
├── adversariales/                # robustez con Hypothesis (ver pruebas-adversariales.md)
├── evals/                        # comportamiento del agente con el modelo (ver evals-del-llm.md)
│   └── casos.jsonl               # el golden dataset
└── e2e/                          # el recorrido completo por la API
```
