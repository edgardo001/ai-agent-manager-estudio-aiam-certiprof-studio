# RAG: embeddings, vectores y buenas prácticas

Cómo busca el agente las soluciones documentadas que pide el curso (Módulo 2, sección 2.5) y qué prácticas de ingeniería sigue para eso. Un RAG (generación aumentada por recuperación) es lo que forman los pasos 4 y 8 del flujo del plan: la base de conocimiento y la herramienta `buscar_solucion`. **Nada de esto viene en el curso:** es la técnica con que el proyecto cumple lo que el curso pide. Las decisiones están en `decisiones.md` (D2, D8 y D9) y el código, en `src/backend/aplicacion/modelo.py` (`crear_embedding()`) y `base_de_datos.py` (`buscar_fragmentos()`). El costo de calcular los embeddings está en `modelos-y-costos.md`.

El material de referencia que aporta el usuario no se sube al repositorio ni se cita: lo relevante se resume aquí, con qué se adopta, en qué etapa y por qué (regla 17 del plan).

## 1. Qué es un embedding

Un embedding (vector semántico) es la lista de números con que un modelo representa el **significado** de un texto. El modelo corta el texto en tokens (trozos de palabras), los procesa todos juntos y al final resume el texto completo en **un solo punto** de un espacio de muchas dimensiones: cada número es una coordenada de ese punto, como (x, y) en un plano, pero con 768 ejes. Los textos de significado parecido quedan cerca. La búsqueda mide esa cercanía con la distancia de coseno (`<=>` en pgvector): 1 es idéntico y, mientras más bajo, menos se parecen.

Un número suelto no significa nada por sí solo (no hay un eje “contraseñas”): lo que importa es la posición del punto completo frente a los demás.

## 2. El largo no depende del texto: prueba real

Prueba hecha el 2026-11-18 con `gemini-embedding-001`:

| Texto | Caracteres | Números del vector |
|---|---|---|
| “hola” | 4 | 768 |
| un párrafo sobre contraseñas | 1.275 | 768 |
| “olvidé mi clave” | 15 | 768 |
| “mi impresora corta las facturas” | 31 | 768 |

“Olvidé mi clave” frente al párrafo de contraseñas dio un parecido de 0,86; frente a “mi impresora corta las facturas”, 0,55. Para repetirla, desde `src\backend`, con `.\.venv\Scripts\python.exe`:

```python
from aplicacion.modelo import crear_embedding
import math

textos = ["hola", "No puedo entrar a mi cuenta, olvidé la contraseña. " * 25,
          "olvidé mi clave", "mi impresora corta las facturas"]
vectores = crear_embedding(textos)
for texto, vector in zip(textos, vectores):
    print(len(texto), "caracteres ->", len(vector), "números")

def coseno(a, b):
    return sum(x * y for x, y in zip(a, b)) / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))

print("clave frente a contraseñas:", round(coseno(vectores[2], vectores[1]), 2))
print("clave frente a impresora:", round(coseno(vectores[2], vectores[3]), 2))
```

## 3. No es relleno, cifrado ni Base64

| | Base64 | Cifrado | Huella SHA-256 | Embedding |
|---|---|---|---|---|
| ¿Guarda el texto? | sí, solo lo recodifica | sí, oculto con una clave | no | no |
| ¿Se puede volver al texto? | sí | sí, con la clave | no | no |
| ¿El largo depende del texto? | sí | sí | no: siempre 64 caracteres | no: siempre 768 números |
| ¿Usa relleno? | sí (`=`) | según el algoritmo | no | no |
| ¿Textos parecidos dan resultados parecidos? | no | no | no: cambiar una letra cambia toda la huella | **sí: es su propósito** |

Lo más parecido es la huella SHA-256 (largo fijo, no reversible), con la diferencia clave de la última fila. Un embedding es un **resumen del significado, con pérdida**.

## 4. Qué cambia el tamaño del fragmento

El tamaño del fragmento y su solape **no cambian el largo del vector, pero sí su calidad.** Un fragmento grande mezcla temas y su punto queda en un “promedio” borroso que no se parece mucho a ninguna consulta: por eso el proyecto corta por secciones (D8). Un fragmento chico pierde contexto (“haga clic en Guardar”, ¿de qué pantalla?): por eso cada fragmento lleva antepuesto “Título - Sección”. El solape solo evita que una idea quede partida en el corte. Cada modelo acepta un máximo de tokens de entrada; los 1.200 caracteres del proyecto (unos 300 tokens) quedan muy por debajo.

## 5. Por qué 768

Esta es la única explicación del 768; los demás documentos la enlazan.

- `gemini-embedding-001` entrega **3.072 números** si no se le pide otra cosa, y acepta el parámetro `dimensions` para pedir menos.
- Está entrenado para que **los primeros números concentren lo más importante** (técnica conocida como Matryoshka Representation Learning, por las muñecas rusas): una versión corta pierde poca calidad.
- **Espacio:** pgvector guarda cada número en 4 bytes; 768 números ocupan unos 3 KB por fragmento, frente a unos 12 KB con 3.072.
- **Índice:** el índice HNSW de pgvector admite vectores de hasta 2.000 dimensiones; 3.072 no se podría indexar con el tipo `vector`.
- 768 no es un estándar: es una elección del proyecto. Queda fijo en dos lugares, `DIMENSIONES_EMBEDDING` en `modelo.py` y `vector(768)` en `01_esquema.sql`; la base no lo guarda en otra columna (D9). Los vectores no se normalizan, porque la distancia de coseno no lo necesita.

## 6. Si se cambia de modelo o de proveedor

Cada modelo fija su propio tamaño: por ejemplo, 1.536 o 3.072 en los de OpenAI (que también aceptan `dimensions`), y 384, 768 o 1.024 en varios modelos abiertos, muchos de tamaño fijo. Con otro proveedor, primero hay que confirmar que ofrezca embeddings para el modelo elegido.

Qué hacer al cambiar de modelo de embeddings:

1. Revisar el tamaño que entrega el modelo nuevo y si acepta `dimensions`.
2. Si el tamaño cambia, **no hay que reconstruir la base ni las otras tablas:** se borran los vectores del modelo anterior y se cambia el tipo de la columna; PostgreSQL rehace solo el índice HNSW. Además, se actualizan `DIMENSIONES_EMBEDDING` en `modelo.py` y `vector(768)` en `01_esquema.sql`, para que una base nueva se cree con el tamaño correcto. Probado el 2026-11-18 dentro de una transacción deshecha al final: el tipo quedó en `vector(384)`, el índice siguió existiendo y las demás tablas no se tocaron.

    ```sql
    BEGIN;
    DELETE FROM fragmentos_conocimiento;            -- los vectores del modelo anterior
    ALTER TABLE fragmentos_conocimiento ALTER COLUMN embedding TYPE vector(384);  -- el tamaño nuevo
    COMMIT;
    ```

3. Cambiar `LLM_MODELO_EMBEDDINGS` (y, si hace falta, `LLM_EMBEDDINGS_PROVEEDOR`) en el archivo de configuración y recargar con `scripts.cargar_conocimiento`.

Si el modelo nuevo acepta `dimensions` y permite 768 o más, basta con pedirle 768 y recargar (paso 3).

**Nunca se mezclan vectores de modelos distintos, aunque tengan el mismo tamaño:** cada modelo ubica los significados en un espacio propio, y comparar puntos de dos espacios no tiene sentido. Por eso cada fragmento guarda `modelo_embedding` y la búsqueda solo compara vectores del mismo modelo que la consulta (D8). Por la misma razón, el chat y los embeddings tienen cada uno su proveedor (D13 y D14): el chat se cambia sin recargar la base.

## 7. La escalera de complejidad

**Construir lo más simple que resuelva el problema.** Para los agentes, se sube por esta escalera y se detiene en el primer nivel que resuelve bien el caso (estos “niveles” son de complejidad técnica; no son los niveles de autonomía del curso):

1. Una sola llamada al modelo, con un buen prompt.
2. Un modelo aumentado: con RAG, herramientas o memoria.
3. Un flujo fijo de pasos (workflow).
4. Un agente: el modelo decide los pasos.

Y una regla que resume todo: **el modelo decide lo que requiere razonamiento; el código controla lo que requiere garantías.** Es la decisión del plan: las reglas graves (cancelación, descuentos, cambios de cuenta, tiempo, kill switch) las revisa el código, no el modelo.

**El Agente de Soporte N1 está entre el nivel 2 y el 4 de esta escalera:** es un modelo aumentado con RAG y tres herramientas, y decide en pocos pasos cuándo buscar al cliente, cuándo buscar una solución y cuándo escalar. Que el modelo decida esos pasos es lo que el curso llama Nivel 3 de autonomía (sección 1.2). Por eso el bucle se mantiene corto y con límites.

## 8. Prácticas de RAG

| Práctica | Cómo está en el proyecto | Estado |
|---|---|---|
| El trabajo no es el modelo, sino darle contexto, controlar lo que sale y medir calidad, costo y demora | RAG, reglas en código, evals y costo por caso | ya está |
| Un modelo cobra por token, tiene una ventana limitada, responde distinto cada vez y no conoce los datos propios | tokens y costo por ticket, `temperature=0` en las evals, base de conocimiento | ya está |
| Lo que queda en medio de un contexto largo se aprovecha peor; RAG antes que reentrenar | se envían solo 5 fragmentos cortos; no se reentrena | ya está |
| RAG agéntico: el modelo decide cuándo buscar, con una herramienta | `buscar_solucion`, con k igual a 5 | ya está |
| Indicar la fuente de cada fragmento, responder solo con ese contexto, citar y decir “no lo sé” | cada fragmento llega con “documento > sección” y el agente la cita; “no lo sé” es escalar | hecho en la etapa 3 |
| Clasificar cada falla en búsqueda, contexto con ruido, generación o datos desactualizados | la huella del documento detecta datos viejos (D8) | en las evals (etapa 5) |
| Medir primero el recall: si el documento esperado está entre los 5 (recall@5) y en qué posición | el golden dataset tiene `documento_esperado` | en las evals (etapa 5) |
| Búsqueda híbrida (significado más palabras clave, BM25, fusionadas con RRF) | se puede hacer en PostgreSQL o en memoria, sin servicios extra | postergada (plan, tabla de lo postergado) |

**Nota sobre el tipo de RAG:** los 8 documentos de Nubesoft suman unos 8.000 caracteres y cabrían completos en cada petición, que sería lo más simple. El proyecto usa igual una búsqueda porque su objetivo es aprender cómo funciona un RAG y porque una base de conocimiento real crece.

## 9. Patrones de agentes

La numeración se mantiene porque el código la cita (“patrón 08”).

| Patrón | Cómo está en el proyecto | Estado |
|---|---|---|
| 01 Router (enviar cada petición al agente adecuado) | un solo agente; “si no hay seguridad, a una persona” ya es la regla de escalamiento | no aplica |
| 02 Guardrails de entrada (validar, autorizar, separar datos de instrucciones) | el cliente sale del ticket (2.3); el texto del cliente y lo que devuelven las herramientas van marcados como datos (`marcar_como_datos()`) | hecho en la etapa 3; `revisar_entrada()` y un largo máximo del ticket, en la etapa 4 |
| 03 Guardrails de salida (política, fuentes, reglas de negocio) | `revisar_respuesta()` bloquea descuentos, cambios de cuenta y datos de otros clientes; si falla, se escala en vez de reintentar | etapa 4; el respaldo en las fuentes se mide en las evals, por costo |
| 04 Cadena de prompts y 06 Orquestador y workers | el agente no tiene pasos fijos ni reparte trabajo | no aplica |
| 05 Paralelización (votar varias veces) | cada eval se repite 3 veces y vale la mayoría | en las evals |
| 07 Evaluador y optimizador | el modelo juez de las evals, no en cada respuesta | en las evals |
| 08 Bucle agéntico con herramientas (el sistema controla pasos, tiempo y costo) | 60 segundos por llamada, 6 llamadas por mensaje, `TOPE_TOKENS_POR_TICKET`, parámetros estrictos (`leer_argumentos()`) | hecho en la etapa 3; los 8 minutos en código, en la etapa 4 |
| 09 Persona en el circuito (lo no clasificado es de riesgo alto) | las acciones de riesgo se escalan; una herramienta desconocida se rechaza | hecho en la etapa 3 |
| 10 Memoria | la conversación del ticket y el historial del CRM; los tickets son cortos | ya está |
| Capacidades transversales (trazas, evaluaciones, presupuestos, versionado) | audit trail, evals, topes de tiempo y costo, versión del prompt y del modelo de embeddings | presupuesto desde la etapa 3; audit trail en la etapa 4 |

## 10. Ideas de un RAG de ejemplo

Ideas tomadas de un RAG de ejemplo, sin frameworks, que compartió el usuario; solo las ideas, sin su código.

- **Cortar por secciones con el título antepuesto:** adoptada en la etapa 2 (D8).
- **Avisar si la base no tiene fragmentos del modelo de embeddings en uso,** y qué script correr: hecho en la etapa 3 (la consola).
- **Ver por dentro cada paso** (fragmentos, parecido, tokens, costo y segundos): hecho en la etapa 3, con `aplicacion.consola --detallado`.
- **Evaluar la búsqueda sola,** sin el modelo de chat (recall@k, precision@k, tasa de acierto y MRR); **datos esperados con alternativas** antes del juez; **casos con varios documentos;** comprobar que el golden set no cite documentos inexistentes; y pruebas unitarias de las fórmulas de las métricas: en las evals (etapa 5), detalle en `evals-del-llm.md`.
- **Búsqueda por palabras clave en memoria fusionada con RRF:** anotada como la forma simple para cuando haga falta la búsqueda híbrida.
- **Responder la misma pregunta con y sin RAG,** para ver en vivo cuánto inventa el modelo sin documentos (la alucinación de la sección 3.3): opcional, pendiente hasta que el usuario lo pida.

## 11. Lo que queda pendiente

1. **Etapa 4:** `revisar_entrada()` y un largo máximo para el texto del ticket, con las entradas bloqueadas en la auditoría; los 8 minutos en código; si una respuesta no pasa `revisar_respuesta()`, el ticket se escala, sin reintentos.
2. **Etapa 5 (evals):** recall@5 y posición del documento esperado, causa de cada falla, la búsqueda evaluada sola, datos esperados con alternativas, casos con varios documentos y el golden set verificado.
3. **Opcional, sin etapa:** comparar en la consola una respuesta con y sin RAG.

Lo que no se adopta (router, cadenas de prompts, orquestador, memoria a largo plazo, evaluación en cada respuesta) no hace falta para un agente de este tamaño: sumaría complejidad sin enseñar nada nuevo del curso.
