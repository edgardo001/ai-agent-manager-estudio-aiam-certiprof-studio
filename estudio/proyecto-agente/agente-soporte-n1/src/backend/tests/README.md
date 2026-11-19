# Pruebas

Cinco tipos de prueba, cada uno en su carpeta. La estrategia completa está en `docs/estrategia-de-pruebas.md`.

| Carpeta | Tipo | Costo | Cómo se corre (desde `src/backend`) |
|---|---|---|---|
| `unitarias/` | una función sola, con datos fijos | gratis | `.venv/Scripts/python.exe -m pytest tests/unitarias` |
| `integracion/` | el código con PostgreSQL real, sin modelo | gratis; necesita PostgreSQL levantado | `.venv/Scripts/python.exe -m pytest tests/integracion` |
| `adversariales/` | robustez con entradas extrañas (Hypothesis) | gratis | `.venv/Scripts/python.exe -m pytest tests/adversariales` |
| `evals/` | comportamiento del agente con el modelo real | llamadas al modelo | `.venv/Scripts/python.exe -m pytest tests/evals` |
| `e2e/` | el recorrido completo por la API | llamadas al modelo | `.venv/Scripts/python.exe -m pytest tests/e2e` |

Se corren con `python -m pytest` desde `src/backend`, para que las pruebas encuentren los paquetes `aplicacion` y `scripts` (`from aplicacion import config`; ver `docs/decisiones.md`, D10). Las gratis se corren a cada cambio; evals y e2e, antes de aprobar una versión del prompt o al cerrar una etapa. Todavía no hay pruebas escritas: llegan desde la etapa 3 (ver “Cuándo se escribe cada tipo” en la estrategia).
