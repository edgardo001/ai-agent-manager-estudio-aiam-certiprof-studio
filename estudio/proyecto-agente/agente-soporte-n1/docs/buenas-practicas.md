# Buenas prácticas de referencia

Prácticas de ingeniería para construir sistemas con modelos de lenguaje, revisadas contra el proyecto. Para cada una, el documento dice si ya está, si se adopta (y en qué etapa) o si se posterga o no aplica, y por qué. El criterio es el principio rector del plan: todos los conceptos del curso, a escala pequeña, sin complejidad que no ayude a entenderlo. Nada de esto viene del curso AI Agent Manager.

## La idea principal

**Construir lo más simple que resuelva el problema.** Para el RAG significa empezar por lo más simple que funcione; para los agentes, subir por esta escalera y detenerse en el primer nivel que resuelve bien el caso:

1. Una sola llamada al modelo, con un buen prompt.
2. Un modelo aumentado: con RAG, herramientas o memoria.
3. Un flujo fijo de pasos (workflow).
4. Un agente: el modelo decide los pasos.

Y una regla que resume todo: **el modelo decide lo que requiere razonamiento; el código controla lo que requiere garantías.** Es la misma decisión que ya tomó el plan: las reglas graves (cancelación, descuentos, cambios de cuenta, tiempo, kill switch) las revisa el código, no el modelo.

**Dónde está el Agente de Soporte N1 en esa escalera:** entre el nivel 2 y el 4. Es un modelo aumentado con RAG y tres herramientas, y decide en pocos pasos cuándo buscar al cliente, cuándo buscar una solución y cuándo escalar. Que el modelo decida esos pasos es justamente lo que el curso llama Nivel 3 de autonomía (sección 1.2). Por eso el bucle se mantiene corto y con límites.

## Prácticas de RAG

| Práctica | Cómo está en el proyecto | Decisión |
|---|---|---|
| El modelo es la parte fácil; el trabajo es darle contexto, controlar lo que sale y medir calidad, costo y demora | contexto con RAG, reglas en código, evals y costo por caso | ya está |
| Un LLM paga por token, tiene una ventana de contexto limitada, responde distinto cada vez y no conoce los datos propios | tokens y costo por ticket (D5), `temperature=0` en las evals, base de conocimiento | ya está |
| Lo que queda en medio de un contexto largo se aprovecha peor | se envían solo 5 fragmentos cortos, no todos los documentos | ya está |
| RAG antes que reentrenar el modelo para hechos que cambian | el proyecto usa RAG y no reentrena | ya está |
| RAG clásico: cargar, trocear, embeddings, guardar en pgvector; en cada pregunta, buscar los k más cercanos | `cargar_conocimiento.py` y `buscar_fragmentos()`, con k igual a 5 | ya está |
| Armar el contexto **indicando la fuente de cada fragmento**, y pedirle al modelo que responda solo con ese contexto, que cite y que diga “no lo sé” si no está | el prompt ya pide usar solo lo que devuelve `buscar_solucion`; en este agente, “no lo sé” es escalar a una persona | **hecho en la etapa 3 (2026-11-19):** `buscar_solucion` entrega cada fragmento con su fuente (documento > sección), y el agente la cita al final de la respuesta |
| Tipos de RAG: todo el conocimiento en cada petición, RAG clásico, wiki escrita por un LLM, RAG agéntico | el proyecto usa RAG agéntico: el modelo decide cuándo buscar, con una herramienta | ya está; ver la nota de abajo |
| Dónde falla un RAG: la búsqueda (el más común), el contexto con ruido, la generación (mezcla lo que sabía o no cita) y los datos desactualizados | las evals miden la recuperación, la fidelidad y la alucinación; la huella del documento detecta datos viejos (D8) | **adoptar en las evals:** clasificar cada falla en una de esas cuatro causas |
| Precision@k y recall@k, primero el recall; un golden set de 20 a 30 preguntas con sus fragmentos esperados | el golden dataset ya tiene `documento_esperado` y apunta a unos 20 casos | **adoptar en las evals:** medir recall@5 (si el documento esperado está entre los 5) y su posición |
| Búsqueda híbrida: significado más palabras clave (BM25), fusionadas con RRF | postergada en D8 | sigue postergada; D8 ya dice cuándo agregarla |
| Un buen RAG cita sus fuentes y sabe decir “no lo sé” | escalar cuando no hay solución documentada; citar, desde la etapa 3 | ya está: cita la fuente desde la etapa 3 y escala cuando no hay solución |

**Nota honesta sobre el tipo de RAG:** los 8 documentos de Nubesoft suman unos 8.000 caracteres, y cabrían completos en cada petición. Lo más simple sería meterlos todos. El proyecto usa igual un RAG con búsqueda porque su objetivo es aprender cómo funciona uno, y porque una base de conocimiento real crece; si en algún momento se quisiera simplificar al máximo, esa sería la alternativa.

## Patrones de desarrollo de agentes

| Patrón | Qué propone | Cómo está en el proyecto | Decisión |
|---|---|---|---|
| 01 Router | clasificar cada petición y enviarla al agente o modelo adecuado; si la confianza es baja, a una persona | hay un solo agente | no aplica; el principio “si no hay seguridad, a una persona” ya es la regla de escalamiento |
| 02 Guardrails de entrada | validar formato y límites, autorizar, clasificar el riesgo, guardar solo lo necesario, y separar los datos de las instrucciones | el cliente sale del ticket, no del modelo (permisos mínimos, 2.3); desde la etapa 3, el texto del cliente y lo que devuelven las herramientas van marcados como datos (`marcar_como_datos()`, que no deja formar etiquetas) y el prompt lo explica en “Datos frente a instrucciones” | **pendiente para la etapa 4:** `revisar_entrada()` detecta cancelaciones, un largo máximo para el texto del ticket y las entradas bloqueadas quedan en la auditoría |
| 03 Guardrails de salida | validar estructura, política (secretos, datos personales), respaldo en las fuentes y reglas de negocio; si falla, reintentar con un límite o dar una respuesta segura | `revisar_respuesta()` (etapa 4) bloquea descuentos, cambios de cuenta y datos de otros clientes | **adoptar, en su forma simple:** si la respuesta falla, el ticket se escala (la respuesta segura) en vez de reintentar; comprobar el respaldo en las fuentes queda en las evals, no en cada respuesta, por costo |
| 04 Cadena de prompts | dividir una tarea en pasos fijos con controles entre ellos | el agente no tiene pasos fijos | no aplica |
| 05 Paralelización | dividir una revisión en partes, o votar varias veces una decisión | las evals repiten cada caso 3 veces y vale la mayoría | ya está, en las evals |
| 06 Orquestador y workers | un componente divide el trabajo y lo reparte | un solo agente con tres herramientas | no aplica |
| 07 Evaluador y optimizador | generar, evaluar con una rúbrica y mejorar, con un límite de vueltas | el modelo juez de las evals | ya está, en las evals; no se usa en cada respuesta, por costo y demora |
| 08 Bucle agéntico con herramientas | el modelo elige la acción y el sistema controla las herramientas, los permisos, los pasos, el tiempo, el costo y lo que necesita aprobación | desde la etapa 3: 60 segundos por llamada, tres herramientas, permisos mínimos, un máximo de 6 llamadas por mensaje, `TOPE_TOKENS_POR_TICKET` y herramientas con parámetros estrictos y errores que el modelo entiende (`leer_argumentos()`); los cambios de cuenta solo con una persona | **pendiente para la etapa 4:** los 8 minutos, revisados en código |
| 09 Persona en el circuito (human-in-the-loop) | las acciones de alto riesgo esperan una aprobación; lo que no está clasificado se trata como de riesgo alto | el agente no ejecuta acciones de riesgo: las escala a una persona | **hecho en la etapa 3 (2026-11-19):** si el modelo pide una herramienta que no existe, se rechaza (“desconocido significa restringido”) |
| 10 Memoria | separar el contexto de la conversación actual de la memoria a largo plazo, y no guardar “por si acaso” | la conversación del ticket (`mensajes`) y el historial del CRM, de solo lectura | ya está; no hace falta memoria a largo plazo ni resumir conversaciones, porque los tickets son cortos |
| Capacidades transversales | trazas, evaluaciones, presupuestos y versionado | audit trail, evals, límites de tiempo y costo, versión del prompt y del modelo de embeddings | ya está; el presupuesto de tokens está desde la etapa 3 y el audit trail llega en la etapa 4 |

## Ideas de un RAG de ejemplo

Ideas tomadas de un RAG de ejemplo, sin frameworks, que el usuario compartió. Solo se toman las ideas: el código del proyecto se escribe aparte, en Python y con sus propias reglas.

| Idea | Qué aporta | Decisión |
|---|---|---|
| Cortar cada documento por sus secciones (`## `) y anteponer al texto del fragmento el título del documento y de la sección | cada fragmento dice de qué trata aunque se lea solo, y la cita puede ser precisa: “restablecer-contrasena.md > Pasos” | **adoptada el 2026-11-18** (decisión D8): por secciones; si una sección es muy larga, por párrafos; y si un párrafo solo es muy largo, por caracteres con solape |
| Al empezar, comprobar que la base tiene fragmentos del mismo modelo de embeddings que se usa ahora, y si no, avisar qué script correr | evita una búsqueda que no encuentra nada sin explicar por qué | **hecho en la etapa 3 (2026-11-19):** la consola avisa y dice qué script correr |
| Mostrar, paso a paso, qué fragmentos encontró la búsqueda, con su parecido, los tokens, el costo y los segundos de cada fase | deja ver por dentro cómo funciona el RAG; es la consola como herramienta de estudio | **hecho en la etapa 3 (2026-11-19):** `python -m aplicacion.consola --detallado` |
| Responder la misma pregunta con y sin RAG | muestra en vivo cuánto inventa el modelo sin documentos: la alucinación de la sección 3.3 | opcional, **pendiente:** no se hizo en la etapa 3; queda para cuando el usuario lo pida |
| Medir la búsqueda sola, sin llamar al modelo de chat, con recall@k, precision@k, tasa de acierto y MRR (si el correcto sale primero) | es casi gratis y separa los fallos de búsqueda de los de generación | **adoptar en las evals** |
| Comprobar la respuesta con datos esperados y alternativas (“2 años\|dos años”), sin un modelo juez | más barato y fiable que un juez para datos concretos, como plazos o números | **adoptar en las evals,** antes del juez |
| Casos de tres tipos: con un documento, con varios documentos y sin respuesta | los casos con varios documentos prueban que el agente combine fuentes | **adoptar en las evals** |
| Antes de evaluar, comprobar que los documentos esperados del golden set existen en la base | un golden set desactualizado da resultados falsos | **adoptar en las evals** |
| Búsqueda por palabras clave (BM25) en memoria y fusión con RRF, sin servicios extra | la búsqueda híbrida es más simple de lo que parece | sigue postergada (D8), con esta forma simple anotada para cuando haga falta |
| Pruebas unitarias de las métricas, que son funciones puras | las fórmulas de las métricas también pueden estar mal | **adoptar:** van en `tests/unitarias/` |

## Lo que queda pendiente

Lo hecho en las etapas 2 y 3 está marcado en las tablas de arriba. Queda, todo pequeño y en la etapa en que se escribe ese código:

1. **Etapa 4:** `revisar_entrada()` y un largo máximo para el texto del ticket, con las entradas bloqueadas en la auditoría; los 8 minutos en código.
2. **Etapa 4:** si una respuesta no pasa `revisar_respuesta()`, el ticket se escala, sin reintentos.
3. **Evals (etapa 5):** medir recall@5 y la posición del documento esperado, y clasificar cada falla del RAG en búsqueda, contexto, generación o datos; evaluar la búsqueda sola (recall@k, precision@k, tasa de acierto y MRR); comprobar datos esperados con alternativas antes de usar el juez; casos con varios documentos; y verificar que el golden set no cite documentos inexistentes.
4. **Opcional, sin etapa:** comparar en la consola una respuesta con y sin RAG.

Lo que no se adopta (router, cadenas de prompts, orquestador, memoria a largo plazo, evaluación en cada respuesta) no hace falta para un agente de este tamaño: agregarlo sumaría complejidad sin enseñar nada nuevo del curso.
