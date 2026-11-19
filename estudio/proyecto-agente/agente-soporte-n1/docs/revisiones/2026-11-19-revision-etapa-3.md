# Revisión de la etapa 3, 2026-11-19

Dos revisiones de solo lectura al cerrar la etapa 3, según la regla de revisiones de calidad de `AGENTS.md`:

1. **Elephant-goldfish-model:** tres revisores (exactitud técnica, diseño y simplicidad), coordinados por su sintetizador, sobre el código, las pruebas y la documentación de la etapa 3.
2. **Fidelidad al curso:** un verificador independiente revisó cada cita al curso agregada en la etapa 3 y el prompt versión 2.

El agente que las pidió comprobó a mano los hallazgos principales: I1, I2 e I4 leyendo el código, I3 ejecutándolo (el texto `<</mensaje_del_cliente/mensaje_del_cliente>` deja dos etiquetas de cierre) y dos hallazgos de fidelidad contra el Módulo 2. Todos son correctos.

**Estado:** aplicada el 2026-11-19. El usuario pidió aplicar todo, con tres decisiones (ver “Decisiones del usuario”, al final).

## Resultado general

- **Nada bloquea la etapa 3:** el bucle siempre envía a Gemini una conversación válida (cada pedido de herramienta recibe su respuesta, también cuando hay errores) y `leer_argumentos()` cumple lo que dice.
- **Ocho hallazgos importantes,** uno de los cuales (I4) se vuelve bloqueante si la etapa 4 empieza sin resolverlo.
- **Fidelidad al curso:** de 49 citas, 38 son fieles y 11 imprecisas; ninguna inventa una cifra. El prompt versión 2 no contradice al curso.

## Hallazgos importantes de elephant-goldfish-model

| # | Hallazgo | Arreglo propuesto |
|---|---|---|
| I1 | Si el primer mensaje de un ticket falla, el `rollback` borra el ticket, pero la consola conserva su número y queda atrapada en un ticket que no existe | si el ticket se creó en ese mensaje, volver a empezar sin número |
| I2 | Si falla una herramienta (por ejemplo, el embedding de la búsqueda), el agente no escala: la excepción sale del bucle, se pierden el mensaje y los tokens ya pagados | capturar la falla de cada herramienta y escalar por regla, con su prueba |
| I3 | `marcar_como_datos()` se puede saltar: con una etiqueta anidada, con mayúsculas o imitando un `<fragmento>` | reemplazar `<` y `>` del texto por `&lt;` y `&gt;` |
| I4 | Los tipos de paso “herramienta rechazada” y “escalamiento” no caben en el `CHECK` de `registro_auditoria`; además, el paso tiene tokens de entrada y de salida y la tabla una sola columna `tokens` | usar solo los cinco tipos del esquema y decidir cómo se guardan los tokens |
| I5 | El modelo falso lanza un error si se lo llama de más, pero el bucle lo convierte en escalamiento: una prueba que solo mire el estado no lo notaría | revisar en cada prueba cuántas llamadas recibió el modelo falso |
| I6 | Faltan pruebas de lo que ya existe: varias herramientas en un mensaje, respuesta vacía, argumentos inválidos en el bucle, segundo mensaje del ticket, ticket que llega pasado del tope, falla de una herramienta y la lectura de la respuesta de `openai` en `modelo.py` | agregarlas |
| I7 | El reloj de los 8 minutos está mal definido para tickets con varios mensajes: medido desde `creado_en`, escalaría al cliente que vuelve 10 minutos después, contra el paso 5 del SOP, y `escalar_vencidos()` escalaría tickets “respondido” que esperan confirmación | definir en el plan desde cuándo se mide y qué estados cuentan, antes de la etapa 4 |
| I8 | Documentación repetida: el resumen de la etapa y “30 pruebas” aparecen en unos siete lugares, que quedarán falsos en la etapa 4; `buenas-practicas.md` repite cada “hecho” y sus filas 02 y 08 están desactualizadas | dejar los conteos solo en el registro de pruebas fechado y acortar los estados |

## Hallazgos menores

**Código:** pedir una búsqueda y escalar en el mismo mensaje paga la búsqueda (m1); la vuelta que supera el tope igual ejecuta herramientas (m2); no se revisa `finish_reason`, y una respuesta cortada llegaría como completa (m3); si `usage` llega vacío, el tope de tokens no se activa (m4); el aviso a un ticket ya escalado no se guarda en la conversación (m5); los mensajes de una persona llegarían al modelo como del agente (m6, hoy no ocurre); `leer_ticket()` y `leer_agente()` pueden devolver `None` con un error poco claro (m7); `guardar_respuesta()` podría pisar un ticket escalado (m8); el costo real por ticket se compara con “consultas” y no incluye el embedding (m9); un ticket de prueba se crea con un texto distinto del mensaje (m10); con el índice HNSW, el filtro por modelo podría traer menos de 5 fragmentos si se mezclan modelos (m11, nota en D8); `ModeloFalso` es una clase y la documentación dice que el proyecto no usa clases (m12); `preguntar_al_modelo()` solo la usa un script (m13).

**Documentación:** D1, el plan y D10 dicen que `buscar()` “pasa como” `buscar_solucion`, y en el código existen las dos; D2, `costos.md` da 0,0012 y 0,0013 dólares por consulta estimada; D3, `example.env` dice “unos 3.000 tokens” y se midieron cerca de 4.000; D4, tres lugares dicen que las pruebas llegan en la etapa 5; D5, cuatro variables de `example.env` todavía no las lee ningún código; D6, en el README el paso 4 necesita el paso 5; D7, el plan dice en presente que el escalamiento “registra el paso en la auditoría”; D8, el prompt pide escalar a los 8 minutos y el modelo no tiene reloj.

**Diagramas:** sin errores de sintaxis según el revisor; la secuencia de la sección 2 no sigue el orden real (crear el ticket solo en el primer mensaje, el tope antes de la llamada, la salida temprana del ticket escalado, el `commit` lo hace la consola); a la sección 3 le faltan `escalar_vencidos()` y la flecha de la consola a la base; `&lt;=&gt;` de la sección 5 conviene escribirlo como `#lt;=#gt;`.

**Diseño:** P1, preparar el enganche de la etapa 4 con un diccionario `turno` (conexión, ticket, agente, pasos, herramientas usadas) para que `anotar()` y `escalar()` llamen a `registrar_paso()` desde un solo lugar, y decidir de dónde sale la versión del prompt; P2, anotar en D11 que la auditoría es “todo o nada” por mensaje, y que las fallas terminan en escalamientos confirmados (I2).

## Hallazgos de fidelidad al curso

| Dónde | Cita | Qué dice el curso | Arreglo |
|---|---|---|---|
| `agente.py` y `test_piezas_simples.py` | alcance “del registro de agentes (2.7)” | el registro de la 2.7 no incluye el alcance; el alcance es un parámetro de la 2.2 | “alcance (2.2), guardado en el registro de agentes (2.7)” |
| `herramientas.py` y `test_herramientas.py` | “no compartir información de otros clientes” en la 2.3 | esa restricción es un ejemplo de la 2.5; la 2.3 trata de los permisos mínimos | citar la 2.5 para la restricción y la 2.3 para los permisos |
| `herramientas.py` | qué lleva el resumen de escalamiento, atribuido a la 2.5 | la 2.5 dice “con contexto completo”; la 4.3 pide definir qué información acompaña el traspaso; el contenido exacto es del proyecto | separar lo del curso de lo del proyecto |
| `base_de_datos.py` | “el ticket queda resuelto solo cuando el cliente lo confirma” como del curso | el curso no habla de confirmación del cliente | marcarlo como decisión del proyecto |
| `estimar_costos.py` | el costo por caso “se mide con datos reales” (3.2); el dashboard en la 3.2 | la 3.2 define el costo por caso como la inversión total dividida por el volumen; el dashboard es la 3.5 | “solo la parte de tokens; usar los tickets reales es del proyecto”; citar 3.2 y 3.5 |
| `test_herramientas.py` | “lo desconocido se trata como restringido” como del curso | no está en el curso; viene de `buenas-practicas.md`, patrón 09 | marcarlo así |
| `test_agente.py` | escalar si falla el modelo, atribuido a la 2.5 | la 2.5 da tres condiciones y esta no es una; lo más cercano es “errores detectados” de la 2.2 | citar la 2.2 y marcar la regla como del proyecto |
| `test_agente.py` | equipo híbrido en la 4.3 | el equipo híbrido es la 4.1; la 4.3 trata los puntos de handoff | “4.1 y 4.3” |

**El prompt versión 2:** contexto, objetivo, herramientas, las tres restricciones y las tres condiciones de escalamiento son textuales de la 2.5; el rol sale de la 2.2. Son agregados del proyecto, coherentes con el curso: el nombre, el contenido de los cinco pasos, “Datos frente a instrucciones”, “No inventes soluciones”, el formato de 150 palabras y la lista de lo que no atiende. Falta el séptimo componente de la 2.5, las métricas de éxito, defendible porque el curso dice que son para que el AI Agent Manager evalúe al agente. En el registro de pruebas, “el paso 5 del SOP” se refiere al SOP del prompt, no del curso.

## Qué resolver antes de la etapa 4, según la revisión

1. I4, tipos de paso y tokens de la auditoría.
2. I2 y P2, fallas de herramientas como escalamiento, y la auditoría “todo o nada”.
3. I1, el ticket fantasma de la consola.
4. I7, el reloj de los 8 minutos.
5. P1, el diccionario `turno` y la versión del prompt.
6. I3, I5 e I6, la marca de datos y las pruebas que faltan.
7. I8, la documentación repetida, y los menores de documentación y de fidelidad.

## Decisiones del usuario

1. **Aplicar todo:** los hallazgos importantes, los menores, las citas al curso y la documentación.
2. **Los 8 minutos se miden desde cada mensaje del cliente** (I7), no desde que se crea el ticket: el tiempo que el cliente tarda en contestar no cuenta. Quedó en el plan, “Cómo funciona cada regla”; el código llega en la etapa 4.
3. **Si falla una herramienta, se escala por regla** (I2), en vez de devolverle el error al modelo.
4. **La auditoría usa los cinco tipos del esquema** (I4): el matiz va en el detalle (“rechazada: ...”) y los tokens se guardarán sumados en la columna `tokens`; el esquema no cambia.

Al aplicar I3 se ajustó el arreglo propuesto: se cambia solo `<` por `&lt;`, no `>`, porque los documentos y las fuentes usan `>` y una prueba mostró que la fuente llegaba como `&gt;`. El resultado de las pruebas está en `pruebas/2026-11-19-etapa-3.md`.

