# AGENTS.md — Conversión de `certiprof-ai-agent-manager-aiam-guia-de-autoestudio-es.pdf` a Markdown legible por text-to-speech

Este archivo contiene las reglas que deben seguir todos los agentes que participan en la conversión. Se actualiza a medida que aparecen casos nuevos (ver "Registro de cambios" al final).

> **Antes de empezar y al terminar cada tarea:** lea “Mantenimiento de los archivos del proyecto”. Al cerrar cualquier cambio se actualizan `AGENTS.md`, `MEMORY.md` y `README.md`, sin esperar a que el usuario lo pida, y no se hace commit sin su autorización.

## Objetivo

Convertir `certiprof-ai-agent-manager-aiam-guia-de-autoestudio-es.pdf` (programa "AI Agent Manager — AIAM™", 97 páginas, 5 módulos) en `estudio/AI-Agent-Manager.md`, un documento en prosa continua, fácil de escuchar con un lector text-to-speech, **sin perder ningún concepto, dato, cifra, fuente ni ejemplo**.

## Contexto del usuario

El usuario estudia este material escuchándolo con un programa text-to-speech; por eso el documento debe leerse bien en voz alta. Quiere poder buscar rápido los términos y dudas que va consultando: antes de responder cualquier consulta sobre el contenido, lee la sección “Preguntas del usuario: Preguntas frecuentes y Glosario” de este archivo y sigue su formato y su largo estándar.

## Fuentes de trabajo

Nota: las rutas de abajo eran temporales (carpeta scratchpad de una sesión) y pueden haber desaparecido. Si hace falta volver a consultar el PDF página por página, se regeneran desde `certiprof-ai-agent-manager-aiam-guia-de-autoestudio-es.pdf` con Python: el texto con `pypdf` (`PdfReader(...).pages[i].extract_text()`) y las imágenes con `pypdfium2` (`page.render(scale=1.4).to_pil().save(...)`). El documento final ya está completo y no depende de esos archivos.

- Texto extraído por página: `<scratchpad>/pages/pNNN.txt` (ej. `p007.txt`).
- Imagen renderizada por página: `<scratchpad>/img/pNNN.png`. Úsala para entender la estructura visual (cards, tablas, cifras destacadas, columnas) cuando el texto extraído quede desordenado o ambiguo.
- `<scratchpad>` = carpeta temporal de la sesión de trabajo en que se hizo la conversión (ya no existe; al regenerar los archivos se usa cualquier carpeta temporal).

## Mapa de páginas

| Módulo | Páginas | Título |
|---|---|---|
| Portada | 1 | Se omite |
| Módulo 1 | 2–19 | El Nuevo Rol del Manager: De Supervisar Personas a Orquestar Agentes |
| Módulo 2 | 20–40 | Diseñar y Activar Agentes: El Arte del Onboarding Agentic |
| Módulo 3 | 41–59 | Supervisión, Auditoría y Performance del Agente |
| Módulo 4 | 60–75 | Rediseño de Procesos: Equipos Híbridos Humanos + Agentes |
| Módulo 5 | 76–92 | Impacto al Negocio: Medir, Comunicar y Escalar Resultados |
| Cierre / Certiprof | 93–97 | Se omite |

## Reglas de contenido

1. **No perder nada.** Todo concepto, definición, cifra, porcentaje, fuente citada (autor, institución, año), ejemplo, caso real y advertencia debe aparecer en el resultado. Ante la duda, se incluye.
2. **Ir página por página, en orden.** El orden del contenido en el `.md` debe seguir el orden del PDF. El texto que continúa de una página a la siguiente se une en un solo párrafo sin cortes (los saltos de página no existen en el `.md`).
3. **Eliminar cabeceras y pies de página:** logo/“certiprof”, `www.certiprof.com`, número de página, “CERTIPROF® is a registered trademark…”, “AIAM™ VERSIÓN 052026”.
4. **Eliminar metadatos de módulo:** “Duración estimada” y “Nivel”. (Los objetivos de aprendizaje y demás contenido sí se conservan.)
5. **Tablas → párrafos.** Cada fila de una tabla se convierte en una o varias oraciones completas que nombren explícitamente lo que dicen las columnas. Ej.: tabla de competencias → “La primera competencia es la Dirección Estratégica, que en la práctica implica definir qué debe lograr el agente…”. Si la tabla tiene título, ese título introduce el párrafo. Nunca se omite una fila ni una celda.
6. **Cards, recuadros, cifras destacadas, citas y cajas de “¿Qué dice la investigación?” → párrafos.** Se integra el contenido como prosa. Una cifra destacada (ej. “280%” + texto) se redacta como oración: “La demanda del skill cluster Agentic AI creció un 280% en un solo año…”. Se conserva la fuente y el título de la card cuando aporta contexto (ej. “Según Harvard Business Review, en el artículo de Srinivasan y Wei de febrero de 2026, titulado …”).
7. **Listas y viñetas → párrafos.** Se redactan como oraciones encadenadas (“En primer lugar…, en segundo lugar…”) o como enumeración dentro de una oración. No se usan viñetas ni listas numeradas en el resultado.
8. **Checklists de autoevaluación (☐ / ✓)** → párrafo en prosa que enumere todas las capacidades (“Al terminar este módulo, usted debería ser capaz de…”), sin perder ningún ítem.
9. **Casos reales, Reflexión Estratégica Final, Responsabilidades del AIAM™** → se conservan como subsecciones con prosa.
10. **Preguntas de validación:** por cada pregunta se escribe el enunciado completo (escenario + pregunta), luego “Respuesta correcta:” seguido del **texto completo** de la alternativa correcta (sin la letra), y luego “Por qué:” con la justificación de la respuesta correcta. **Se eliminan** las alternativas incorrectas y cualquier comentario sobre por qué las otras opciones son incorrectas (frases tipo “A es incorrecta porque…”, “C borra la distinción”). Si la justificación de la correcta no hace referencia a las otras, se mantiene íntegra.
11. **No inventar ni resumir.** Se puede reformular la sintaxis para convertir tablas/cards/listas en prosa, pero no se agrega información que no esté en el PDF ni se condensa contenido. El texto que ya es prosa en el PDF se copia fiel, solo corrigiendo cortes de extracción (palabras partidas como “tal ento” → “talento”, guiones de corte de línea, espacios sobrantes).
12. **Emojis y símbolos decorativos** (💡, ⏱, 🎯, ❌, ✓, ☐, 📋, flechas como “→” usadas en cifras) se eliminan o se reemplazan por palabras (“2024→2025” → “de 2024 a 2025”). Las siglas y marcas (AIAM™, HBR, CSAT, NPS, ROI…) se conservan.

## Reglas de formato

1. El documento final usa un `#` para el título general, `##` para cada módulo (“## Módulo 1. El Nuevo Rol del Manager: De Supervisar Personas a Orquestar Agentes”), `###` para cada sección numerada del PDF (“### 1.2 Agentes de IA, Chatbots y Automatización…”) y `####` para subsecciones (casos, cards con título propio y cada pregunta como “#### Pregunta 1”). Las secciones sin número, como “Preguntas de validación”, van como `###` (ver regla 5).
2. Mismo orden y misma numeración de secciones que el PDF.
3. Sin tablas Markdown, sin viñetas, sin listas numeradas, sin bloques de cita (`>`), sin negritas decorativas excesivas. Solo encabezados y párrafos.
4. Párrafos separados por una línea en blanco. Codificación UTF-8 con tildes correctas.
5. **Jerarquía fija:** las secciones sin número que cuelgan del módulo (Objetivo de aprendizaje, Responsabilidades, Checklist o Lista de Competencias, Reflexión Estratégica, Preguntas de validación) van como `###`, con el título que tenga en el PDF (ver regla adicional 32). “Preguntas de validación” se escribe igual en los cinco módulos. Las cards o recuadros con título propio dentro de una sección (Regla práctica, ¿Qué dice la investigación?, Caso X…) van como `####`. Cada pregunta va como `#### Pregunta N`.

## Reglas adicionales (incorporadas a partir del trabajo de los agentes)

1. **Navegación entre módulos** (“Módulo 2 Completado. Continúe al Módulo 3…”) se elimina.
2. **“Por qué” de las preguntas:** se elimina la frase que nombra la letra (“C es correcto porque…”, “B establece…”) y se reformula como “Esta respuesta…” o empezando directo por la razón. Toda mención a otras letras se elimina.
3. **Erratas evidentes del PDF** (p. ej. “el enemy número uno” por “el enemigo número uno”) se corrigen, porque el lector de voz las pronunciaría mal. Los términos técnicos en inglés usados intencionalmente (agent sprawl, guardrails, onboarding…) se mantienen.
4. **Notación de cifras para voz:** decimales con coma (“2.3 millones” → “2,3 millones”); “$40M” → “40 millones de dólares”; “40%+” → “más del 40%”; “≥80%” → “mayor o igual al 80%”; “4.2/5” → “4,2 sobre 5”; enumeraciones “(a) (b) (c)” o “(1) (2) (3)” → “primero, segundo, tercero”.
5. **Tablas comparativas de dos columnas** (antes/después, humano/agente): un párrafo por fila o dimensión contrastando ambas columnas, o dos bloques paralelos con todos los ítems en orden.
6. **Checklists** se redactan en tercera persona formal (“usted debería ser capaz de…”), no en primera persona.
7. **Cards de caso:** “Industria” y “Resultado medible” pasan a un párrafo introductorio; “Lección para el AI Agent Manager” → “La lección para el AI Agent Manager es la siguiente: …”.
8. **Formato numérico único (español):** decimales con coma (“1,3 segundos”, “4,4”), miles con punto (“55.000 rutas”, “1.200”). Moneda: “$4.4T” → “4,4 billones de dólares”; “$400M” → “400 millones de dólares”. Esta normalización se aplica a todo el documento final.
9. **Rangos y fórmulas:** “12-24 meses” → “de 12 a 24 meses”; “18+ meses” → “más de 18 meses”; “(Beneficio – Inversión) / Inversión” → “el beneficio menos la inversión, dividido por la inversión”.
10. **Cards de pares de ejemplo** (lenguaje técnico frente a directivo, etc.): subsección `####` con un párrafo por par (“En lenguaje técnico: … Traducido al lenguaje directivo: …”).
11. **Referencias académicas destacadas:** subsección `#### Referencia académica N`, con la fuente en prosa (autor, año, título, editorial) y la cita textual entre comillas.
12. **Respuestas que empiezan con raya** (“Nivel 1 — Exploración, porque…”) → se reemplaza la raya por coma.
13. En el “Por qué” se conservan las frases de razonamiento que no nombran letras de alternativas (p. ej. “No hay que retroceder al Nivel 1 ni saltar al Nivel 3…”), porque forman parte de la explicación.
14. **Símbolos para voz:** “±2 semanas” → “más o menos 2 semanas”; “3+ días” → “3 o más días”; “5-10%” → “entre el 5% y el 10%”; “tokens/min” → “tokens por minuto”; “verde/amarillo/rojo” → “verde, amarillo o rojo”; “1-a-1” → “1 a 1”; “vs.” → “frente a”; las rayas (—) que separan incisos → comas o dos puntos.
15. **Tablas con celda “N/A”:** se explica en prosa (“aquí no aplica dejar correr, porque…”), no se omite la fila.
16. **Cards de tipos (p. ej. tipos de error):** un `####` por tipo, con párrafos que empiezan por “Qué son:”, “Ejemplo:”, “Señal de detección:”.
17. **Responsabilidades numeradas (01, 02…)** → “La primera responsabilidad es…”, un párrafo por responsabilidad.
18. **Encabezado de las preguntas de validación:** se conserva la descripción (“Diez preguntas de práctica basadas en rol”), pero se elimina la instrucción “Seleccione la opción que mejor aplique”, porque ya no hay alternativas.
19. Una cifra que solo aparece en una alternativa incorrecta se pierde legítimamente al eliminar esa alternativa.
20. El **Objetivo de aprendizaje** del inicio de cada módulo va como `###` (ver regla de formato 5).
21. **Conceptos dentro de comentarios sobre alternativas incorrectas (prioridad sobre la regla 2):** si un comentario sobre una opción incorrecta contiene un concepto, criterio o dato que se aprende (p. ej. “el problema real es el criterio de evaluación, no el volumen de datos”; “el Nivel 1 tiene a los humanos como control”; “todos los niveles requieren gestión”), ese concepto **se conserva** en el “Por qué”, redactado como afirmación general y sin nombrar la letra ni describir la alternativa incorrecta. Solo se elimina lo que es pura descalificación de la opción (“A es irrelevante”, “B es negligencia”).
22. **Enunciados que terminan en “…es:”** se reformulan como pregunta directa, porque las alternativas ya no los completan.
23. **Fidelidad de cifras:** si el propio PDF da cifras distintas para el mismo dato en lugares diferentes (p. ej. McKinsey 4,4 billones en una card y “2,6 a 4,4 billones” en una pregunta), se conservan ambas tal como aparecen en cada lugar.
24. **Encabezados de checklist y similares:** se respeta el título del PDF (“1.6 Checklist de Competencias, Módulo 1” si va numerado como `###`; “Lista de Competencias del Módulo 4” como `###` aunque no tenga número).
25. **Checklists en primera persona** (“Puedo…”, “Soy capaz…”, “Entiendo…”): cada ítem se convierte a infinitivo dentro de “usted debería ser capaz de…”, y los posesivos “mi” pasan a “su”.
26. **Ampliación de la regla 21:** cuando un comentario descalifica una alternativa por un motivo con contenido (“es un argumento operativo, no estratégico”, “es una falacia de apelación a la mayoría”, “es una sobre-reacción que destruye valor”, “confunde la eficiencia con la transformación”), ese motivo se conserva como afirmación general sobre la acción o idea errónea. Solo se descarta la etiqueta sin criterio (“es negligencia”, “es irrelevante”).
27. **“Por qué” sin sujeto:** al quitar la letra, la frase no puede empezar con un verbo suelto (“aplica…”); se pone sujeto explícito: “Esta respuesta aplica…”, o “Esta conducta es…” cuando la pregunta pide identificar lo que debe evitarse.
28. **Signo “+”** entre instituciones o conceptos (“MIT SMR + BCG”) → “y” o “más”. “24/7” → “las 24 horas, los 7 días de la semana”; “1:1” → “1 a 1”.
29. **No agregar glosas que no están en el PDF** (p. ej. “4.4 trillion, en la notación anglosajona”).
30. **Oraciones completas en inglés dentro de prosa en español** (restos sin traducir del original) se traducen fielmente para que el lector de voz en español las lea bien. Los términos técnicos en inglés usados a propósito se mantienen.
31. **Tablas comparativas sin título:** se puede usar un `####` construido con los encabezados de columna (“Organización sin… frente a organización con…”), sin agregar información.
32. Se respeta el título exacto del PDF en secciones finales (“Reflexión Estratégica” sin “Final” si así aparece). Una card con título que aparece antes de esas secciones (“Lo que este programa te ha dado”) va como `####`.

## Preguntas del usuario: Preguntas frecuentes y Glosario

Cuando el usuario haga una pregunta sobre el contenido, se responde en la conversación **y además** se agrega a uno de estos dos archivos independientes (no al documento del curso):

1. **`estudio/glosario.md`**: cuando la consulta es por una palabra, sigla o término específico (p. ej. “¿qué es agent sprawl?”). Cada entrada lleva el término como encabezado `## <Término>`. Las entradas se mantienen **en orden alfabético**.
2. **`estudio/preguntas-frecuentes.md`**: cuando la consulta es conceptual o de comprensión (p. ej. “¿cuál es la diferencia entre un chatbot y un agente?”). Cada entrada lleva la pregunta como encabezado `## <Pregunta>`. Se agregan en el orden en que el usuario las hace.

**Sin redundancia (decisión del usuario):** antes de agregar una entrada, se revisa si ya existe una pregunta o un término parecido en los dos archivos. Si existe, no se crea una entrada nueva: se edita la existente para complementarla con lo que aporta la nueva consulta (y, si hace falta, se ajusta su título para que cubra ambas), respetando el largo estándar. En la conversación se le avisa al usuario qué entrada se complementó.

**Largo estándar (decisión del usuario):**
- **Glosario, entre 80 y 120 palabras, un párrafo:** qué es (sigla completa y traducción), para qué sirve en el curso con un dato o ejemplo, y dónde aparece (módulo y sección principal, sin listar todo).
- **Preguntas frecuentes, entre 150 y 250 palabras, dos o tres párrafos:** respuesta directa en una o dos oraciones; de tres a cinco ideas clave, una oración cada una (“Primero…, segundo…”); un ejemplo o cifra del curso; y dónde profundizar.
- Si una consulta mezcla término y “cómo se hace”, la respuesta va en Preguntas frecuentes y el Glosario lleva una entrada corta que remite a ella.

Las respuestas siguen las mismas reglas de formato del documento: solo encabezados y párrafos, sin tablas, viñetas ni emojis, y con números y símbolos escritos para voz. Si la respuesta usa información externa al PDF, se indica explícitamente con una frase corta (“esto no viene en el curso”), para no confundirla con el contenido del curso. Si un término ya está en el Glosario, se amplía su entrada en vez de duplicarla.

## Mantenimiento de los archivos del proyecto

**Actualización periódica obligatoria (regla del usuario):** `AGENTS.md`, `MEMORY.md` y `README.md` se actualizan siempre, en la misma sesión en que ocurre el cambio y sin esperar a que el usuario lo pida. Ninguna tarea se da por terminada sin este cierre:

1. **`AGENTS.md` (este archivo): las reglas.** Se actualiza cuando aparece una regla nueva del usuario, un caso nuevo de conversión o formato, o un tipo nuevo de archivo en `estudio/`. Cada cambio se anota en el “Registro de cambios” con su fecha.
2. **`MEMORY.md`: la memoria del proyecto.** Se actualiza cuando el usuario toma una decisión, cuando cambia el estado de cualquier archivo de `estudio/`, cuando hace una consulta (se anota en “Consultas del usuario” con fecha y archivo de destino: glosario, preguntas frecuentes o diagramas) y cuando se abre o se cierra un pendiente. Al empezar una sesión nueva, se lee junto con este archivo.
3. **`README.md`: la presentación del repositorio.** Se actualiza cuando se crea, se mueve o se elimina un archivo o carpeta, o cambia la forma de usarlos.

**Paso a paso de cierre de cada tarea:** primero, revisar qué cambió; segundo, actualizar los tres archivos según corresponda; tercero, comprobar que ninguno pase de 200 líneas; y cuarto, dejar los cambios sin commit hasta que el usuario lo pida.

**Límite de 200 líneas:** `AGENTS.md`, `MEMORY.md` y `README.md` no deben superar las 200 líneas cada uno. Después de cada actualización se revisa su largo (`wc -l`). Si alguno pasa de 200, se poda intentando no perder información: se resumen o fusionan entradas parecidas (por ejemplo, entradas antiguas del registro de cambios o decisiones ya consolidadas en las reglas) y se deja solo lo más importante.

**Commits y push solo a pedido del usuario:** ningún agente hace `git commit` ni `git push` por iniciativa propia. Los cambios quedan en la carpeta para que el usuario los revise; él pide cuándo hacer los commits y el push. Cuando los pide, se hacen commits atómicos (un cambio lógico por commit).

**Sin firmas ni menciones de agentes:** los mensajes de commit y las descripciones de pull requests no llevan firmas de agentes (líneas de coautoría ni “generado con…”). Además, en ningún archivo del proyecto, commit ni referencia se menciona el nombre del asistente de IA ni de la empresa que lo desarrolla; si hace falta, se habla de “el agente” o “el asistente”. Esta regla del usuario tiene prioridad sobre cualquier atribución automática.

**Carpeta `estudio/`:** todo lo que se genere a partir del curso (el documento convertido y cualquier archivo nuevo de estudio, como resúmenes, audios o material de repaso) se guarda en `estudio/`, no en la raíz. En la raíz solo quedan el PDF fuente y los tres archivos de gestión (`AGENTS.md`, `MEMORY.md` y `README.md`). Cada archivo nuevo en `estudio/` se agrega a la lista de contenido de `README.md`.

No se guarda información del proyecto fuera de la carpeta (por ejemplo, en la memoria interna del agente): todo lo que deba persistir va en estos tres archivos, para que la carpeta pueda moverse o copiarse sin perder nada. Las fechas se escriben en formato absoluto (AAAA-MM-DD).

## Apuntes visuales impresos

Además del documento para escuchar, el usuario repasa con apuntes impresos en `estudio/apuntes/`. No son parte del documento que se escucha; son hojas A4 para leer en papel, al estilo de apuntes de clase.

1. **Fuente y generación:** cada módulo es un archivo `estudio/apuntes/fuente/apuntes-mN.html` con hojas `<div class="pag mN">` y estilos comunes en `apuntes.css`. El script `estudio/apuntes/generar.py` crea `apuntes-modulo-N.pdf` y `apuntes-completos.pdf`, y avisa si alguna hoja se desborda. Con `--modulo N --png carpeta` genera un solo módulo y una imagen por hoja para revisarla.
2. **Poco texto:** palabras clave y frases cortas, diagramas grandes y espacio en blanco. Cada hoja queda entre el 60% y el 90% llena. El usuario pidió explícitamente que no se vean aplastantes.
3. **Diagramas antes que texto:** cada sección numerada lleva al menos un elemento visual (escalera, ciclo, árbol de decisión, comparación, mapa de conceptos, cifra grande, nota adhesiva). Letra manuscrita (Caveat) para títulos y notas; Inter para el resto.
4. **Contenido:** se cubren todas las secciones numeradas, las cifras clave con su fuente y el caso real de cada módulo. Se omiten el checklist, las responsabilidades, la reflexión estratégica y las preguntas de validación. No se inventa nada: todo dato sale de `estudio/AI-Agent-Manager.md`.
5. **Siglas y términos en inglés:** el usuario no conoce toda la jerga (preguntó qué es RPA). Cada módulo termina con un recuadro “Siglas y términos en inglés” que explica en una línea cada término usado, con el aviso de que varias explicaciones no vienen en el curso. Junto a un término difícil dentro de un diagrama se puede poner una aclaración corta en gris.
6. **Técnica:** las flechas (`<marker>`) llevan color en hexadecimal e id con prefijo del módulo (`m2-fc`), porque los cinco módulos se unen en un solo PDF. El CSS propio de un módulo va dentro de `<body>` con selectores que empiezan por `.mN`.

## Diagramas Mermaid a pedido

Cuando el usuario pida un diagrama, se agrega a `estudio/diagramas.md`, en el orden en que lo pide. Cada diagrama lleva un encabezado `## <Tema>`, una o dos oraciones que dicen qué muestra y de qué módulo y sección sale, y el bloque de código Mermaid. Las etiquetas van en español y son cortas. Todo dato sale de `estudio/AI-Agent-Manager.md`; lo que no venga del curso se marca. Antes de agregarlo, se valida que la sintaxis Mermaid sea correcta (por ejemplo, comillas en etiquetas con paréntesis, dos puntos o acentos problemáticos).

## Plantillas de gestión

`estudio/plantillas/` tiene 15 plantillas numeradas por fase del ciclo de vida (decidir, diseñar y activar, integrar al equipo, supervisar y gobernar, demostrar valor y escalar) y una guía de uso, `00-guia.md`. Toda plantilla nueva o modificada mantiene la misma estructura: un bloque inicial (para qué sirve, cuándo llenarla, quién la llena y la aprueba, con qué se llena, base en el curso, se conecta con), “Cómo llenarla”, “Plantilla”, “Ejemplo lleno” y “Errores comunes”. Los campos salen de lo que pide el curso; lo agregado se marca “(no viene en el curso)” y los datos inventados, “datos ficticios de ejemplo”. Los ejemplos usan como hilo conductor el “Agente de Soporte N1” (agente de soporte B2B de la sección 2.5), en Nivel 2, con personas ficticias. Cada sigla en inglés se explica la primera vez que aparece en cada plantilla. Se mantienen los términos del curso (por ejemplo, “taxonomía de tareas”) aunque suenen técnicos; no se reemplazan por sinónimos.

## Flujo de trabajo de los agentes

- Cada agente procesa **un módulo completo** y escribe su resultado en `<scratchpad>/out/moduloN.md` (empezando por el encabezado `## Módulo N. …`).
- Antes de escribir cada página, el agente lee `pNNN.txt` **y** `pNNN.png`.
- Al terminar, el agente relee las páginas fuente y verifica que cada cifra, fuente y concepto aparezca en su salida.
- El agente informa en su respuesta final: (a) casos nuevos o ambiguos que encontró y cómo los resolvió, para incorporarlos a este archivo; (b) cualquier contenido que no pudo leer.
- El orquestador une los módulos en `estudio/AI-Agent-Manager.md` y actualiza este archivo.

## Registro de cambios

- 2026-11-17 — Versión inicial. Decisiones del usuario: en preguntas se conserva pregunta + respuesta correcta + justificación de la correcta; se omiten duración/nivel; se incluyen checklists, reflexiones y responsabilidades en prosa; se omiten portada (p.1) y cierre/Certiprof (p.93–97); el archivo final se llama `AI-Agent-Manager.md`.
- 2026-11-17 — Reglas adicionales 1 a 24, a partir de los informes de los agentes de cada módulo (formato numérico, símbolos, jerarquía, navegación, conceptos dentro de comentarios sobre alternativas incorrectas).
- 2026-11-17 — Segunda pasada de auditoría por módulo contra el PDF: conceptos rescatados de los comentarios de alternativas incorrectas, formato unificado, reglas 25 a 32. Documento final unido: 5 módulos, 50 preguntas con 50 respuestas, sin tablas, listas ni citas.
- 2026-11-17 — Se crean `README.md` y `MEMORY.md` y se agrega la sección “Mantenimiento de los archivos del proyecto”: los tres archivos se actualizan periódicamente y no se guarda información del proyecto fuera de la carpeta.
- 2026-11-17 — Se agregó “Contexto del usuario” y la nota sobre fuentes temporales, para que la carpeta pueda moverse sin depender de memoria externa. Primera entrada del Glosario: Accountability.
- 2026-11-17 — Nueva regla del usuario: las preguntas que haga se agregan al final del documento, en “Preguntas frecuentes” (preguntas conceptuales) o en “Glosario” (términos específicos, en orden alfabético).
- 2026-11-17 — Nueva regla del usuario: los commits y pull requests no llevan firmas de agentes (sección “Mantenimiento de los archivos del proyecto”).
- 2026-11-17 — Nueva regla del usuario: no se menciona el nombre del asistente de IA en ninguna parte (archivos, commits, referencias). Se quitaron las menciones existentes, incluida la ruta temporal de `<scratchpad>`.
- 2026-11-17 — El PDF fuente se renombró de `document.pdf` a `certiprof-ai-agent-manager-aiam-guia-de-autoestudio-es.pdf`; se actualizaron las referencias en `AGENTS.md` y `README.md`.
- 2026-11-17 — Revisión de consistencia: regla adicional 13 movida a su lugar; reglas de formato 1 y 5 alineadas (“Preguntas de validación” va como `###`). En `AI-Agent-Manager.md` se unificaron los encabezados “Preguntas de validación” de los cinco módulos y el de responsabilidades del Módulo 2, según el PDF.
- 2026-11-17 — Decisión del usuario: el documento convertido se movió de la raíz a la carpeta `estudio/` (`estudio/AI-Agent-Manager.md`).
- 2026-11-17 — Nueva regla del usuario: `estudio/` es la carpeta de todos los archivos generados a partir del curso; la raíz queda solo para el PDF y los archivos de gestión.
- 2026-11-17 — Nueva sección “Apuntes visuales impresos”: apuntes A4 por módulo en `estudio/apuntes/`, con poco texto, diagramas y un recuadro final de siglas y términos en inglés. Nueva entrada del Glosario: RPA.
- 2026-11-17 — Nueva regla del usuario: `AGENTS.md`, `MEMORY.md` y `README.md` no superan las 200 líneas; si pasan el límite, se podan resumiendo sin perder lo importante. Primera pregunta en “Preguntas frecuentes” (¿Qué es un AI Agent Manager?) y nueva entrada del Glosario: C-suite.
- 2026-11-17 — Decisión del usuario: Preguntas frecuentes y Glosario pasan a archivos independientes (`estudio/preguntas-frecuentes.md` y `estudio/glosario.md`) y se fija su largo estándar (80 a 120 palabras por término; 150 a 250 por pregunta). Las 13 entradas existentes se reescribieron con ese estándar.
- 2026-11-17 — Se crea `estudio/diagramas.md` para diagramas Mermaid a pedido del usuario (sección “Diagramas Mermaid a pedido”).
- 2026-11-17 — Nueva regla del usuario: no se hacen commits ni push hasta que él revise y los pida.
- 2026-11-17 — Nueva regla del usuario: sin redundancia en Preguntas frecuentes y Glosario; si ya existe una consulta parecida, se complementa la entrada existente en vez de crear otra.
- 2026-11-17 — Se crean las 15 plantillas de gestión y su guía en `estudio/plantillas/` (sección “Plantillas de gestión”).
- 2026-11-17 — A pedido del usuario, la regla de actualización periódica de `AGENTS.md`, `MEMORY.md` y `README.md` se hace explícita y obligatoria, con un paso a paso de cierre de cada tarea y un aviso al inicio de este archivo.
