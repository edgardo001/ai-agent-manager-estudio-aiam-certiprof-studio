# Costos: cuánto cuesta cargar documentos y atender consultas

Cómo estimar lo que gasta el proyecto en el modelo, antes de saber cuánto lo usarán los clientes. Pedido del usuario del 2026-11-18: poder estimar el costo de los embeddings de X documentos de X tamaño y el de cada consulta, con una demanda que no se conoce con certeza ni se sabe cómo se concentrará en el tiempo.

**Relación con el curso:** el curso pide medir el costo por caso (Módulo 3, sección 3.2) y el valor y el ROI (Módulo 5), con datos reales de operación, en el dashboard (etapa 7). Esta estimación es previa a la operación y es una práctica del proyecto: no viene en el curso.

## 1. La herramienta: `estimar_costos.py`

No llama al modelo, así que es gratis y se puede correr cuantas veces se quiera. Desde la carpeta `src/backend` (es un script de asistencia, ver `src/backend/scripts/README.md`):

```powershell
# Mide los documentos reales de src/base-de-conocimiento/ y usa los escenarios por defecto
.\.venv\Scripts\python.exe -m scripts.estimar_costos

# Caso hipotético de documentos, y escenarios propios: consultas al día (baja, esperada y alta)
# y el porcentaje de las consultas del día que llega en la hora más cargada
.\.venv\Scripts\python.exe -m scripts.estimar_costos --documentos 10000 --caracteres 50000 --consultas 100 1000 5000 --hora-pico 25
```

Entrega tres resultados:

1. **Embeddings de una carga completa:** de la base de conocimiento actual y, si se piden, de un caso hipotético.
2. **Una consulta del cliente:** tokens y costo.
3. **Escenarios de uso:** costo por día y por mes con la demanda baja, la esperada y la alta, más el pico de uso frente al límite de la cuenta.

## 2. Resultado del 2026-11-18

Con los precios de `gemini-3.1-flash-lite` (0,25 y 1,50 dólares por millón de tokens de entrada y de salida) y de `gemini-embedding-001` (0,15):

| Qué | Estimación |
|---|---|
| Carga de los 8 documentos actuales (23 fragmentos, 6.091 caracteres, unos 1.523 tokens) | 0,000228 dólares |
| Carga hipotética de 10.000 documentos de 50.000 caracteres (125 millones de tokens) | 18,75 dólares |
| Una consulta (3 llamadas al modelo, unos 2.979 tokens de entrada y 300 de salida) | 0,0012 dólares |
| 50 consultas al día | 1,80 dólares al mes |
| 300 consultas al día | 10,82 dólares al mes |
| 1.000 consultas al día | 36,07 dólares al mes |
| 1.000 consultas al día, con el 20% en la hora más cargada | 3,3 consultas y 10 llamadas al modelo por minuto |

## 3. De qué depende cada costo

**Los embeddings** se cobran solo por los tokens de entrada (no tienen salida) y dependen del **total de texto**, no de la cantidad de documentos: un documento de 10.000 caracteres cuesta lo mismo que diez de 1.000. Se pagan de nuevo en cada recarga completa, porque `cargar_conocimiento.py` borra y recalcula todo; con miles de documentos conviene la carga incremental (en la tabla de lo postergado del plan). Detalle en `embeddings-y-vectores.md`, sección 7.

**Cada consulta** tiene tres partes:

| Parte | Por qué cuesta | Peso |
|---|---|---|
| El embedding de la pregunta | la búsqueda convierte la pregunta en vector | casi nada |
| La entrada del modelo de chat | **cada llamada reenvía todo:** el prompt, la descripción de las herramientas, la pregunta y lo que ya pasó; los fragmentos encontrados se suman una vez | la mayor parte |
| La salida del modelo de chat | las decisiones de herramientas y la respuesta (máximo 150 palabras, según el prompt) | cara por token (1,50), pero pocos tokens |

Lo que más mueve el costo por consulta: **el largo del prompt** (se paga en cada llamada), **la cantidad de llamadas** por consulta y **los mensajes de ida y vuelta**: si el cliente responde y el agente vuelve a pensar, es otra consulta que reenvía toda la conversación.

## 4. Demanda incierta: escenarios, no un número

No se puede saber con certeza cuántas consultas habrá. Por eso la herramienta no da un número, sino tres escenarios (baja, esperada y alta), y se planifica con el alto. Tres ideas:

- **El costo depende del total de consultas, no de cuántas llegan juntas.** Mil consultas cuestan lo mismo repartidas en el día que en una hora.
- **Lo que llega junto afecta otra cosa: el límite de uso del proveedor.** Cada cuenta tiene un máximo de llamadas y de tokens por minuto. Si un pico lo supera, hay esperas o errores, no más costo. El parámetro `--hora-pico` dice qué parte de las consultas del día llega en la hora más cargada; un 20% es un supuesto razonable para soporte en horario laboral. El límite de la cuenta se ve en Google AI Studio y se anota en `LIMITE_LLAMADAS_POR_MINUTO`.
- **Para acotar el riesgo:** fijar un tope de gasto o alertas de presupuesto en la consola de facturación del proveedor, y un tope de tokens por ticket en el agente (`TOPE_TOKENS_POR_TICKET`, 20.000 por defecto, desde la etapa 3: si se supera, el ticket se escala).

## 5. Supuestos y cómo afinarlos

| Supuesto | Valor | Dónde se cambia | Cómo se afina |
|---|---|---|---|
| Caracteres por token | 4 | `estimar_costos.py` | en español suele haber algo más de tokens: para no quedarse corto, use 3 |
| Llamadas al modelo por consulta | 3 (buscar al cliente, buscar la solución y responder, según el SOP) | `LLAMADAS_POR_CONSULTA` en el `.env` | con el promedio real desde la etapa 3 |
| Tokens de las tres herramientas | 300 | `estimar_costos.py` | con la definición real de la etapa 3 |
| Largo de la pregunta del cliente | 200 caracteres | `estimar_costos.py` | con los tickets reales |
| Tokens de salida por consulta | 300 | `estimar_costos.py` | con los tickets reales |
| Precios | los del `.env` | `PRECIO_MILLON_TOKENS_*` | cuando cambie el modelo o el precio (D5) |

**Desde la etapa 3, con datos reales:** cada ticket guarda `tokens_entrada`, `tokens_salida` y `costo_tokens` (lo informa el modelo de chat en cada respuesta), y el script usa esos promedios en vez de los supuestos cuando PostgreSQL está levantado y hay tickets. Primera medición, el 2026-11-19: un ticket resuelto con 3 llamadas usó 3.774 tokens de entrada y 200 de salida, 0,0012 dólares, lo mismo que la estimación de la tabla de arriba (`pruebas/2026-11-19-etapa-3.md`). El costo real es por ticket, que puede tener varios mensajes, y no incluye el embedding de la consulta. Si el proveedor no informara los tokens de una respuesta, se cuentan 0 y el tope de tokens no se activaría; queda el máximo de 6 llamadas por mensaje (con Gemini se comprobó que sí los informa). Los tokens de los embeddings no se pueden medir así: el punto de acceso compatible con OpenAI no los informa (`usage` llega vacío, comprobado el 2026-11-18); se estiman por caracteres o se ven en el panel de uso de Google AI Studio.
