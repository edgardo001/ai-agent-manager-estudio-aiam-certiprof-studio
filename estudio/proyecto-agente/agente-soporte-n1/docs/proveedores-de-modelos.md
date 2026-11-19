# Proveedores de modelos: cambiar, mezclar y tener respaldo

Documento técnico a partir de las preguntas del usuario del 2026-11-19: probar el agente con OpenRouter antes de seguir, y más adelante con Ollama, mezclar embeddings de un proveedor con el chat de otro y tener respaldo si un proveedor se cae. **Nada de esto viene en el curso.** Las decisiones están en `decisiones.md` (D5, D8, D11 y D13).

## Lo que ya se puede hacer

El código habla con los modelos con la librería `openai`, y Gemini, OpenRouter y Ollama aceptan ese mismo formato. Por eso cambiar de proveedor es cambiar el `.env`, sin tocar el código.

Desde el 2026-11-19, el **chat** y los **embeddings** tienen cada uno su proveedor (decisión D13), elegido por nombre (D14). Cada proveedor tiene en el `.env` su dirección y su clave, con nombre propio (`GEMINI_BASE_URL` y `GEMINI_API_KEY`, `OPENROUTER_BASE_URL` y `OPENROUTER_API_KEY`; Ollama no pide clave y tiene `OLLAMA_BASE_URL`). Las direcciones son las públicas de cada servicio y están a la vista para poder cambiarlas sin tocar el código:

| Qué | Variables | Qué pasa si se cambia |
|---|---|---|
| Chat (el agente que conversa y usa herramientas) | `LLM_PROVEEDOR` (`gemini`, `openrouter` u `ollama`), `LLM_MODEL`, `LLM_MAXIMO_TOKENS_SALIDA` y los precios `PRECIO_MILLON_TOKENS_ENTRADA` y `PRECIO_MILLON_TOKENS_SALIDA` | nada más: el siguiente mensaje ya usa el modelo nuevo |
| Embeddings (los vectores del RAG) | `LLM_EMBEDDINGS_PROVEEDOR`, `LLM_MODELO_EMBEDDINGS` y `PRECIO_MILLON_TOKENS_EMBEDDINGS` | si cambia el **modelo**, hay que recargar la base (`python -m scripts.cargar_conocimiento`), porque los vectores de modelos distintos no se pueden comparar (D8); si cambia solo el proveedor del mismo modelo, ver “Respaldo para los embeddings” |

Si `LLM_EMBEDDINGS_PROVEEDOR` queda vacío, usa el proveedor del chat. Si `example.env` cambia, `python -m scripts.revisar_env --ordenar` deja el `.env` igual a la plantilla, con sus valores (D14).

## Cómo saber si un modelo sirve para el agente: que acepte herramientas

El agente necesita un modelo que sepa **usar herramientas** (tool calling o function calling): en vez de solo escribir texto, el modelo responde “quiero llamar a `buscar_solucion` con estos datos”. Sin eso, no puede buscar al cliente, ni buscar la solución, ni escalar. No todos los modelos lo traen, sobre todo los pequeños y algunos locales.

| Proveedor | Cómo saberlo |
|---|---|
| OpenRouter | en https://openrouter.ai/models, filtrar por “Tools”; en su lista pública (`https://openrouter.ai/api/v1/models`), cada modelo trae `"tools"` en `supported_parameters` si lo acepta |
| Ollama | en https://ollama.com/search, los modelos que lo aceptan llevan la etiqueta “tools” |
| Gemini | la página de cada modelo en la documentación de Google dice si acepta “function calling”; los modelos de chat actuales lo aceptan |

**La forma segura es probarlo:** `python -m scripts.prueba_conexion`, desde `src/backend`, hace tres pruebas con lo que diga el `.env`: un saludo, un pedido de una herramienta inventada (“¿qué hora es en Santiago?”) y un embedding. Dice si el modelo pidió la herramienta y si el vector tiene 768 números. Cuesta una fracción de centavo.

Que acepte herramientas no basta: también tiene que **usarlas bien** (elegir la correcta, no inventar pasos, escalar cuando corresponde). Eso lo miden las evals de la etapa 5, que permitirán comparar modelos con los mismos casos.

## Probar el chat con OpenRouter

1. Crear una clave en https://openrouter.ai/keys y cargar algo de saldo, o usar un modelo gratuito (los que terminan en `:free`). En la capa gratuita, los modelos gratuitos comparten un cupo entre todos los usuarios y tienen un límite diario bajo: sirven para probar, no para correr las evals.
2. En `src/docker/.env`, poner la clave en `OPENROUTER_API_KEY` y cambiar dos líneas: `LLM_PROVEEDOR=openrouter` y `LLM_MODEL` con el nombre del modelo en OpenRouter. `LLM_EMBEDDINGS_PROVEEDOR` sigue en `gemini`, así que la base no se recarga. Para volver, `LLM_PROVEEDOR=gemini` y su modelo.
3. Ajustar los precios del chat si se elige otro modelo (están en su página de OpenRouter).
4. Desde `src/backend`: `python -m scripts.prueba_conexion`, luego `python -m aplicacion.consola --detallado` y `python -m pytest tests/unitarias tests/integracion`.

**Probado el 2026-11-19** (`pruebas/2026-11-19-openrouter.md`): con `nvidia/nemotron-3-ultra-550b-a55b:free`, el agente se comportó igual que con Gemini en los cuatro casos de la etapa 3 y respondió más rápido. Ese día `google/gemma-4-31b-it:free` estaba saturado (error 429). Sin el tope de salida (`LLM_MAXIMO_TOKENS_SALIDA`), OpenRouter reserva saldo para la salida máxima del modelo (65.536 tokens) y, con poco saldo, rechaza el pedido (error 402).

Dos modelos de pago útiles para comparar, ambos con herramientas (precios por millón de tokens de entrada y de salida, según la lista pública de OpenRouter del 2026-11-19):

- **`google/gemini-3.1-flash-lite`** (0,25 y 1,50 dólares): el mismo modelo de hoy por otro camino. Prueba la integración sin cambiar el comportamiento.
- **`anthropic/claude-haiku-5.5`** (0,10 y 0,50 dólares): otra familia de modelos, para tener una segunda evaluación del agente.

OpenRouter agrega a veces un campo propio, `reasoning_details`, que hay que devolver intacto en la llamada siguiente, igual que la firma de Gemini. El código ya lo hace, porque devuelve el mensaje del modelo tal cual (D11).

## Posibilidades para más adelante

Ninguna está construida. Quedan anotadas en la tabla de lo postergado del plan, con cuándo conviene agregarlas.

### Ollama: modelos en el propio equipo

Ollama (licencia MIT) corre modelos abiertos en el equipo y expone el mismo formato en `http://localhost:11434/v1` (la clave puede ser cualquier texto). Se agregaría como un servicio más del `docker-compose.yml` (imagen `ollama/ollama`) o instalado en Windows.

- **Para el chat:** hace falta un modelo que acepte herramientas, y en un equipo sin tarjeta gráfica las respuestas tardan bastante más; hay que medirlo contra los 8 minutos del curso.
- **Para los embeddings:** por ejemplo `nomic-embed-text` (licencia Apache 2.0), que entrega 768 números, el mismo tamaño de la columna `vector(768)`. Con D13 ya se puede combinar con el chat de Gemini u OpenRouter: se cambian las tres variables de embeddings y se recarga la base. Falta comprobar si respeta el parámetro `dimensions`.
- **Ventaja:** sin costo por token y los datos no salen del equipo (útil con la anonimización de `anonimizacion-de-datos.md`). **Costo:** memoria y disco del equipo, y otro servicio que mantener.

### Respaldo si un proveedor se cae

El 2026-11-19, con Gemini, en un mismo día hubo dos llamadas que pasaron los 60 segundos y un error 503 (“el modelo tiene alta demanda”). Hoy el agente escala esos tickets por regla (etapa 3): el cliente no queda sin respuesta, pero el caso pasa a una persona. Hay tres formas de reducirlo, de la más simple a la más compleja:

1. **Respaldo dentro de OpenRouter, sin código.** OpenRouter puede enviar el pedido a otro proveedor del mismo modelo si uno falla (enrutamiento de proveedores), y acepta una lista de modelos en orden (`models`) que prueba uno tras otro. Basta con usar OpenRouter como proveedor del chat. Depende de un solo intermediario.
2. **Un proveedor de respaldo en el código.** Variables `LLM_RESPALDO_BASE_URL`, `LLM_RESPALDO_API_KEY` y `LLM_RESPALDO_MODEL`; si la llamada al proveedor principal falla por tiempo, por un 503 o por un 429 (límite de uso), `modelo.py` repite esa llamada con el de respaldo. Son pocas líneas, pero hay un cuidado: los campos propios de cada proveedor (la firma de Gemini, los `reasoning_details` de OpenRouter) no sirven en el otro. Lo más simple es cambiar de proveedor solo al empezar un mensaje del cliente, nunca a mitad del bucle, y anotar en la auditoría qué proveedor atendió cada paso.
3. **Balancear entre proveedores** (repartir las llamadas entre los dos aunque ninguno falle). **No se recomienda para este proyecto:** dos modelos distintos responden distinto, así que las evals, el muestreo y la deriva de comportamiento del Módulo 3 mezclarían dos agentes en uno. Para disponibilidad basta el respaldo; el balanceo sirve cuando el volumen supera el límite de uso de una cuenta.

### Respaldo para los embeddings

El respaldo del chat no sirve para los embeddings si cambia el **modelo**: los vectores de otro modelo no se comparan con los guardados (D8). Sí sirve el **mismo modelo por otro proveedor**: OpenRouter ofrece `google/gemini-embedding-001` (0,15 dólares por millón de tokens, como Gemini). Falta resolver un detalle: OpenRouter lo llama con el prefijo `google/`, y el filtro por modelo de `buscar_fragmentos()` lo tomaría como otro modelo; habría que guardar y comparar el nombre sin prefijo. Antes de confiar en ese respaldo, hay que comprobar con unas consultas que los dos caminos entregan los mismos vectores.

### Recomendación

Para esta versión: probar OpenRouter ahora (solo cambia el `.env`) y dejar el respaldo para cuando las evals de la etapa 5 permitan comparar modelos con los mismos casos. Si después de la etapa 6 las caídas siguen siendo frecuentes, empezar por la forma 1 (OpenRouter como proveedor del chat, con su enrutamiento), que no suma código, y pasar a la forma 2 solo si hace falta no depender de un intermediario.
