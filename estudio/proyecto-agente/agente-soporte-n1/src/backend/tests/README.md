# Pruebas

Cinco tipos de prueba, cada uno en su carpeta. La estrategia completa (qué prueba cada tipo, cuánto cuesta y cuándo se escribe) está en `docs/estrategia-de-pruebas.md`.

Todas se corren desde `src/backend` con `.\.venv\Scripts\python.exe -m pytest tests/<carpeta>`, para que encuentren los paquetes `aplicacion` y `scripts` (decisión D10). Las gratis se corren a cada cambio: `.\.venv\Scripts\python.exe -m pytest tests/unitarias tests/integracion`. Las que llaman al modelo, antes de aprobar una versión del prompt o al cerrar una etapa.

| Carpeta | Tipo | Costo | Desde |
|---|---|---|---|
| `unitarias/` | una función sola, con datos fijos, sin red ni base de datos | gratis, menos de un segundo | etapa 3 |
| `integracion/` | el código con el PostgreSQL de desarrollo, con un modelo falso | gratis; necesita PostgreSQL levantado (`start-dev.bat`); si no responde, se omiten | etapa 3 |
| `adversariales/` | robustez con entradas extrañas (Hypothesis) | gratis | etapas 5 y 6 |
| `evals/` | comportamiento del agente con el modelo real | llamadas al modelo | etapa 5 |
| `e2e/` | el recorrido completo por la API | llamadas al modelo | etapa 6 |

## Qué hay hoy

| Archivo | Qué prueba |
|---|---|
| `unitarias/test_piezas_simples.py` | configuración y proveedores, costo, vector, instrucciones del agente, corte de documentos y revisión de la configuración local |
| `unitarias/test_reglas.py` | las reglas en código (D16): cancelación, largo, lo que una respuesta no puede decir, 8 minutos y kill switch, con casos que deben pasar |
| `unitarias/test_herramientas.py` | las tres herramientas, el rechazo de herramientas y argumentos inválidos y la marca de datos |
| `unitarias/test_modelo.py` | cómo se lee la respuesta de la librería `openai` (D11), la temperatura y el proveedor del chat y de los embeddings (D13) |
| `integracion/test_base_de_datos.py` | búsqueda por parecido, registro del agente, clientes y tickets |
| `integracion/test_agente.py` | el bucle del agente con un **modelo falso**: cada salida (resolver, escalar, topes, fallas), las reglas, la auditoría y el kill switch; cada prueba cuenta las llamadas al modelo |

**No dejan datos:** la fixture `conexion` de `conftest.py` deshace al final de cada prueba de integración todo lo que escribió, porque el código del agente no confirma los cambios; lo hace quien llama (D11). El modelo falso prueba gratis y siempre igual lo que controla el código; cómo se comporta el modelo real se prueba en las evals.
