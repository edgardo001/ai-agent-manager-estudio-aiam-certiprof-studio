# Modelos y costos: proveedores, cambio de modelo y cuánto cuesta

Cómo elegir, cambiar y mezclar los proveedores del modelo, y cuánto cuesta usarlos. Es la única fuente de las cifras de costo del proyecto. **Casi nada de esto viene en el curso:** el curso pide medir el costo por caso (Módulo 3, sección 3.2) y el valor y el ROI (Módulo 5) con datos reales de operación, en el dashboard (etapa 7); estimarlo antes y elegir proveedores es práctica del proyecto. Las decisiones están en `decisiones.md` (D5, D11, D13 y D14).

Todos los comandos se ejecutan en PowerShell desde `src\backend`, con el entorno virtual que crea `start-dev.bat`: `.\.venv\Scripts\python.exe -m <módulo>`.

## 1. Proveedores: chat y embeddings por separado

El código habla con los modelos con la librería `openai`, y Gemini, OpenRouter y Ollama aceptan ese mismo formato: cambiar de proveedor es cambiar el archivo de configuración (`src/docker/example.env` es la plantilla), sin tocar el código. El **chat** y los **embeddings** tienen cada uno su proveedor, elegido por nombre (D13 y D14). Cada proveedor tiene su dirección y su clave con nombre propio (`GEMINI_BASE_URL` y `GEMINI_API_KEY`, `OPENROUTER_BASE_URL` y `OPENROUTER_API_KEY`; Ollama no pide clave y tiene `OLLAMA_BASE_URL`).

| Qué | Variables | Qué pasa si se cambia |
|---|---|---|
| Chat (el agente que conversa y usa herramientas) | `LLM_PROVEEDOR` (`gemini`, `openrouter` u `ollama`), `LLM_MODEL`, `LLM_MAXIMO_TOKENS_SALIDA` y los precios `PRECIO_MILLON_TOKENS_ENTRADA` y `PRECIO_MILLON_TOKENS_SALIDA` | nada más: el siguiente mensaje ya usa el modelo nuevo |
| Embeddings (los vectores del RAG) | `LLM_EMBEDDINGS_PROVEEDOR`, `LLM_MODELO_EMBEDDINGS` y `PRECIO_MILLON_TOKENS_EMBEDDINGS` | si cambia el **modelo**, hay que recargar la base (`scripts.cargar_conocimiento`), porque los vectores de modelos distintos no se comparan (`rag.md`, sección 6) |

Si `LLM_EMBEDDINGS_PROVEEDOR` queda vacío, usa el proveedor del chat. Si la plantilla cambia, `scripts.revisar_env --ordenar` deja el archivo de configuración igual a ella, con sus valores (D14).

## 2. Cómo saber si un modelo sirve: que acepte herramientas

El agente necesita un modelo que sepa **usar herramientas** (tool calling o function calling): en vez de solo escribir texto, responde “quiero llamar a `buscar_solucion` con estos datos”. Sin eso no puede buscar al cliente, ni la solución, ni escalar. No todos los modelos lo traen, sobre todo los pequeños y algunos locales.

| Proveedor | Cómo saberlo |
|---|---|
| OpenRouter | en https://openrouter.ai/models, filtrar por “Tools”; en su lista pública (`https://openrouter.ai/api/v1/models`), cada modelo trae `"tools"` en `supported_parameters` si lo acepta |
| Ollama | en https://ollama.com/search, los modelos que lo aceptan llevan la etiqueta “tools” |
| Gemini | la página de cada modelo en la documentación de Google dice si acepta “function calling”; los modelos de chat actuales lo aceptan |

**La forma segura es probarlo:** `scripts.prueba_conexion` hace tres pruebas con la configuración actual: un saludo, un pedido de una herramienta inventada (“¿qué hora es en Santiago?”) y un embedding. Dice si el modelo pidió la herramienta y si el vector tiene 768 números. Cuesta una fracción de centavo. Que acepte herramientas no basta: también tiene que **usarlas bien**, y eso lo miden las evals de la etapa 5, que permitirán comparar modelos con los mismos casos.

## 3. Probar el chat con OpenRouter

1. Crear una clave en https://openrouter.ai/keys y cargar algo de saldo, o usar un modelo gratuito (los que terminan en `:free`). Los modelos gratuitos comparten un cupo entre todos los usuarios y tienen un límite diario bajo: sirven para probar, no para correr las evals.
2. En el archivo de configuración, poner la clave en `OPENROUTER_API_KEY` y cambiar dos líneas: `LLM_PROVEEDOR=openrouter` y `LLM_MODEL` con el nombre del modelo en OpenRouter. `LLM_EMBEDDINGS_PROVEEDOR` sigue en `gemini`, así que la base no se recarga. Para volver, `LLM_PROVEEDOR=gemini` y su modelo.
3. Ajustar los precios del chat si se elige otro modelo (están en su página de OpenRouter).
4. Correr `scripts.prueba_conexion`, luego `aplicacion.consola --detallado` y `pytest tests/unitarias tests/integracion`.

Lo que dio la prueba del 2026-11-19 está en `pruebas/2026-11-19-openrouter.md`. Sin el tope de salida (`LLM_MAXIMO_TOKENS_SALIDA`, 2.000 por defecto), OpenRouter reserva saldo para la salida máxima del modelo y, con poco saldo, rechaza el pedido.

Dos modelos de pago para comparar, ambos con herramientas (precios por millón de tokens de entrada y de salida, según la lista pública de OpenRouter del 2026-11-19): **`google/gemini-3.1-flash-lite`** (0,25 y 1,50 dólares), el mismo modelo de hoy por otro camino, que prueba la integración sin cambiar el comportamiento; y **`anthropic/claude-haiku-5.5`** (0,10 y 0,50 dólares), otra familia de modelos, para una segunda evaluación del agente.

OpenRouter agrega a veces un campo propio, `reasoning_details`, que hay que devolver intacto en la llamada siguiente, igual que la firma de Gemini. El código ya lo hace, porque devuelve el mensaje del modelo tal cual (D11).

## 4. Posibilidades para más adelante

Ninguna está construida; están en la tabla de lo postergado del plan, con su señal.

**Ollama, modelos en el propio equipo.** Ollama (licencia MIT) corre modelos abiertos en el equipo y expone el mismo formato en `http://localhost:11434/v1`. Se agregaría como un servicio más del `docker-compose.yml` (imagen `ollama/ollama`) o instalado en Windows. Para el chat hace falta un modelo que acepte herramientas, y sin tarjeta gráfica las respuestas tardan bastante más (hay que medirlo contra los 8 minutos del curso). Para los embeddings sirve, por ejemplo, `nomic-embed-text` (Apache 2.0), que entrega 768 números; se combina con el chat de otro proveedor cambiando las tres variables de embeddings y recargando la base; falta comprobar si respeta `dimensions`. Ventaja: sin costo por token y los datos no salen del equipo (útil con `referencia/anonimizacion-de-datos.md`). Costo: memoria y disco del equipo, y otro servicio que mantener.

**Respaldo si el proveedor del chat se cae.** Hoy, si el modelo falla o tarda más de 60 segundos, el agente escala el ticket por regla: el cliente no queda sin respuesta, pero el caso pasa a una persona. Tres formas de reducirlo, de la más simple a la más compleja:

1. **Respaldo dentro de OpenRouter, sin código:** puede enviar el pedido a otro proveedor del mismo modelo si uno falla, y acepta una lista de modelos en orden (`models`). Basta con usar OpenRouter como proveedor del chat. Depende de un solo intermediario.
2. **Un proveedor de respaldo en el código:** si la llamada falla por tiempo, por un 503 o por un 429 (límite de uso), `modelo.py` la repite con otro proveedor. Los campos propios de cada proveedor (la firma de Gemini, los `reasoning_details` de OpenRouter) no sirven en el otro, así que se cambia de proveedor solo al empezar un mensaje, nunca a mitad del bucle, y se anota en la auditoría quién atendió cada paso.
3. **Balancear entre proveedores** (repartir las llamadas aunque ninguno falle). **No se recomienda:** dos modelos responden distinto, así que las evals, el muestreo y la deriva del Módulo 3 mezclarían dos agentes en uno. El balanceo sirve cuando el volumen supera el límite de una cuenta.

**Respaldo para los embeddings.** Si cambia el modelo, no sirve. Sí sirve el mismo modelo por otro proveedor: OpenRouter ofrece `google/gemini-embedding-001` al mismo precio, pero con el prefijo `google/`, que el filtro por modelo de `buscar_fragmentos()` tomaría como otro modelo; habría que comparar el nombre sin prefijo y comprobar antes que los dos caminos entregan los mismos vectores.

**Recomendación:** dejar el respaldo para cuando las evals de la etapa 5 permitan comparar modelos con los mismos casos; si después de la etapa 6 las caídas siguen siendo frecuentes, empezar por la forma 1, que no suma código, y pasar a la 2 solo si hace falta no depender de un intermediario.

## 4b. Cupos de uso y por qué no varias claves

Consulta del usuario del 2026-11-19: ¿y si las claves fueran una lista, con claves de otras cuentas, para que no se acabe el cupo? **Decisión del usuario: no se agregan más claves**, porque arriesga que bloqueen las cuentas.

- **Varias claves de una misma cuenta no suman cupo:** los límites son por cuenta, no por clave.
- **Varias cuentas gratuitas para esquivar los límites** suele estar prohibido por los términos de uso de estos servicios, y pueden suspenderse todas a la vez (los términos exactos de OpenRouter y de Google no se verificaron).
- **Lo legítimo es el respaldo entre proveedores distintos** (sección 4): Gemini y OpenRouter tienen cada uno su propio cupo, y el respaldo cubre además las caídas.

**Los cupos de los modelos gratuitos de OpenRouter** (los que terminan en `:free`), según su documentación oficial, consultada el 2026-11-19, dependen del saldo comprado alguna vez:

| Saldo comprado alguna vez | Pedidos por minuto | Pedidos por día |
|---|---|---|
| menos de 10 dólares | 20 | 50 |
| 10 dólares o más | 20 | 1.000 |

Con 50 pedidos al día alcanza para probar, no para las evals de la etapa 5: unos 20 casos, repetidos 3 veces, con unas 3 llamadas cada uno, son casi 200 llamadas. Para las evals hay tres caminos legítimos: el cupo propio de Gemini, cargar 10 dólares una vez en OpenRouter (sube a 1.000 al día y queda saldo para modelos de pago), o un modelo de pago.

**Dos opciones de OpenRouter que conviene conocer:**

- **Traer la propia clave (BYOK, “bring your own key”):** se asocia la clave de un proveedor, por ejemplo la de Google, a la cuenta de OpenRouter; los pedidos a modelos de ese proveedor usan el cupo propio y no el compartido de los gratuitos. El error 429 de `google/gemma-4-31b-it:free` lo sugería.
- **`openrouter/free`:** un enrutador que elige automáticamente algún modelo gratuito disponible. Para este agente hay que tener cuidado: no garantiza que el modelo elegido sepa usar herramientas, y cambiar de modelo sin aviso es cambiar de agente (D15 lo anota en la auditoría).

**Para saber cuánto cupo queda,** OpenRouter informa en `GET https://openrouter.ai/api/v1/key` los pedidos gratuitos usados y restantes del día (`free_model_daily_requests`). No se agregó al proyecto: el usuario lo puede ver en el panel de su cuenta.

## 5. Cuánto cuesta: `estimar_costos.py`

Estima, sin llamar al modelo (es gratis), el costo de los embeddings de X documentos de X tamaño y el de cada consulta, con una demanda que no se conoce con certeza (pedido del usuario del 2026-11-18):

```powershell
# Mide los documentos reales de src/base-de-conocimiento/ y usa los escenarios por defecto
.\.venv\Scripts\python.exe -m scripts.estimar_costos

# Caso hipotético de documentos y escenarios propios: consultas al día (baja, esperada y alta)
# y el porcentaje de las consultas del día que llega en la hora más cargada
.\.venv\Scripts\python.exe -m scripts.estimar_costos --documentos 10000 --caracteres 50000 --consultas 100 1000 5000 --hora-pico 25
```

Entrega tres resultados: el costo de los embeddings de una carga completa; los tokens y el costo de una consulta; y el costo por día y por mes con la demanda baja, la esperada y la alta, más el pico de uso frente al límite de la cuenta. Desde la etapa 3, si PostgreSQL está levantado y hay tickets atendidos, los escenarios usan el costo real promedio por ticket en vez del supuesto.

## 6. Las cifras

Precios de `gemini-3.1-flash-lite` (0,25 dólares por millón de tokens de entrada y 1,50 de salida, D5) y de `gemini-embedding-001` (0,15 por millón, solo entrada). Salida del script del 2026-11-19, con los precios por defecto:

| Qué | Cifra |
|---|---|
| Carga de los 8 documentos actuales (23 fragmentos, 6.091 caracteres, unos 1.523 tokens) | 0,000228 dólares |
| Carga hipotética de 10.000 documentos de 50.000 caracteres (125 millones de tokens) | 18,75 dólares |
| Una consulta estimada (3 llamadas al modelo, unos 3.467 tokens de entrada y 300 de salida) | 0,0013 dólares |
| Promedio real de los tickets atendidos hasta ese día | 0,0011 dólares por ticket |
| 50, 300 y 1.000 consultas al día, con el costo real | 1,70, 10,23 y 34,09 dólares al mes |
| 1.000 consultas al día, con el 20% en la hora más cargada | 3,3 consultas y 10 llamadas al modelo por minuto |

La primera medición real (`pruebas/2026-11-19-etapa-3.md`): un ticket resuelto con 3 llamadas costó 0,0012 dólares, frente a 0,0013 estimados. Otras referencias de carga, con la misma regla de 4 caracteres por token: 10 documentos de 2.000 caracteres, unos 0,0008 dólares; 10 de 100.000 (unas 30 páginas cada uno), unos 0,04; 1.000 de 20.000, unos 0,75.

## 7. De qué depende cada costo

**Los embeddings** se cobran solo por los tokens de entrada y dependen del **total de texto**, no de la cantidad de documentos: un documento de 10.000 caracteres cuesta lo mismo que diez de 1.000. Suman también el “Título - Sección” antepuesto a cada fragmento (pocos tokens), el solape (hasta un 20% más, solo en párrafos de más de 1.200 caracteres) y cada búsqueda, porque la consulta también se convierte en vector. Se pagan de nuevo en cada recarga completa, porque `cargar_conocimiento` borra y recalcula todo: con miles de documentos, lo que más pesa es recargar, y por eso a esa escala conviene la carga incremental (tabla de lo postergado del plan). Google AI Studio permite usar el modelo gratis con límites de uso; el modo por lotes costaría la mitad, según sitios que comparan precios (confirmarlo en la página de precios de Google).

**Cada consulta** tiene tres partes: el embedding de la pregunta (casi nada); la entrada del modelo de chat, la mayor parte, porque **cada llamada reenvía todo** (el prompt, la descripción de las herramientas, la pregunta y lo que ya pasó), y los fragmentos encontrados se suman una vez; y la salida, cara por token (1,50) pero con pocos tokens (la respuesta tiene un máximo de 150 palabras, según el prompt). Lo que más mueve el costo: **el largo del prompt**, que se paga en cada llamada, **la cantidad de llamadas** por consulta y **los mensajes de ida y vuelta**, porque cada respuesta del cliente reenvía toda la conversación. Calcular los embeddings cuesta mucho menos que conversar.

## 8. Demanda incierta: escenarios, no un número

No se puede saber cuántas consultas habrá; por eso el script da tres escenarios y se planifica con el alto.

- **El costo depende del total de consultas, no de cuántas llegan juntas:** mil consultas cuestan lo mismo repartidas en el día que en una hora.
- **Lo que llega junto afecta el límite de uso del proveedor:** cada cuenta tiene un máximo de llamadas y de tokens por minuto; si un pico lo supera, hay esperas o errores, no más costo. `--hora-pico` dice qué parte de las consultas del día llega en la hora más cargada (un 20% es un supuesto razonable para soporte en horario laboral). El límite de la cuenta se ve en Google AI Studio y se anota en `LIMITE_LLAMADAS_POR_MINUTO`.
- **Para acotar el riesgo:** un tope de gasto o alertas de presupuesto en la consola de facturación del proveedor, y el tope de tokens por ticket del agente (`TOPE_TOKENS_POR_TICKET`, 20.000 por defecto: si se supera, el ticket se escala).

## 9. Supuestos y cómo afinarlos

| Supuesto | Valor | Dónde se cambia | Cómo se afina |
|---|---|---|---|
| Caracteres por token | 4 | `estimar_costos.py` | en español suele haber algo más de tokens: para no quedarse corto, use 3 |
| Llamadas al modelo por consulta | 3 (buscar al cliente, buscar la solución y responder, según el SOP) | `LLAMADAS_POR_CONSULTA` | con el promedio real de los tickets |
| Tokens de las tres herramientas | 300 | `estimar_costos.py` | con la definición real |
| Largo de la pregunta del cliente | 200 caracteres | `estimar_costos.py` | con los tickets reales |
| Tokens de salida por consulta | 300 | `estimar_costos.py` | con los tickets reales |
| Precios | los de la configuración | `PRECIO_MILLON_TOKENS_*` | cuando cambie el modelo o el precio (D5) |

**Con datos reales:** cada ticket guarda `tokens_entrada`, `tokens_salida` y `costo_tokens` (lo informa el modelo de chat en cada respuesta), y el script usa sus promedios. El costo real es por ticket, que puede tener varios mensajes, y no incluye el embedding de la consulta. Si el proveedor no informara los tokens de una respuesta, se cuentan 0 y el tope de tokens no se activaría; queda el máximo de 6 llamadas por mensaje (Gemini sí los informa). Los tokens de los embeddings no se pueden medir así: el punto de acceso compatible con OpenAI no los informa (`usage` llega vacío, comprobado el 2026-11-18); se estiman por caracteres (dividir por 4, o por 3 para ir por arriba, y multiplicar por el precio) o se ven en el panel de uso y facturación de Google AI Studio.
