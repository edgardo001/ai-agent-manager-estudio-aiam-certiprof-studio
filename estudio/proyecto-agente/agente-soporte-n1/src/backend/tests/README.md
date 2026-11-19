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
| `unitarias/test_piezas_simples.py` | configuración y proveedores (D14), costo, vector como texto, instrucciones del agente (lo que no atiende, datos marcados, versión del prompt), corte de documentos (D8) y la revisión del archivo de configuración local |
| `unitarias/test_herramientas.py` | solo existen las tres herramientas; se rechazan las desconocidas y los argumentos inválidos; `buscar_cliente` no acepta otro cliente; los datos marcados no se pueden cerrar desde adentro; cada fragmento lleva su fuente |
| `unitarias/test_modelo.py` | cómo se lee la respuesta de la librería `openai` sin llamar a un proveedor: la firma de pensamiento (D11), los pedidos de herramientas, el motivo de fin, los tokens, la temperatura y que el chat y los embeddings usen cada uno su proveedor (D13) |
| `integracion/test_base_de_datos.py` | búsqueda por parecido con vectores escritos a mano, registro del agente, clientes y tickets con su conversación y sus tokens |
| `integracion/test_agente.py` | el bucle del agente con un **modelo falso** que entrega respuestas escritas de antemano: resolver, escalar con el contexto completo (también en el límite de tokens o de llamadas), varias herramientas en un mensaje, herramientas o argumentos rechazados, el segundo mensaje, los topes, las fallas del modelo o de una herramienta y las respuestas vacías o cortadas. Cada prueba revisa cuántas veces se llamó al modelo |

**No dejan datos:** la fixture `conexion` de `conftest.py` deshace al final de cada prueba de integración todo lo que escribió, porque el código del agente no confirma los cambios; lo hace quien llama (D11). El modelo falso prueba gratis y siempre igual lo que controla el código; cómo se comporta el modelo real se prueba en las evals.
