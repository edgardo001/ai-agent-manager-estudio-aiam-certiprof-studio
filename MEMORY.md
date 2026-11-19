# MEMORY.md: memoria del proyecto

Lo que un agente necesita saber para continuar sin depender de conversaciones anteriores: contexto, decisiones, estado, consultas del curso y pendientes. Las reglas están en `AGENTS.md`; aquí va el “qué pasó y dónde estamos”. Lo del proyecto de agente vive en su propia documentación, y aquí solo queda su estado con enlaces. Se actualiza según “Mantenimiento y reglas transversales” de `AGENTS.md`.

## Contexto del usuario

- Estudia el curso AI Agent Manager (AIAM™) de Certiprof escuchándolo con un lector text-to-speech, y necesita que nada del contenido se pierda.
- Quiere buscar rápido los términos y dudas que consulta, con respuestas breves: ni poco ni mucho texto.
- Escribe en español; todo va en español con tildes correctas.
- Es programador (Python, C#, Java y Node) y usa Docker, Gemini (Google AI Studio) y OpenRouter.
- Prefiere que se le consulte cuando hay dudas reales, en lugar de suponer.
- Le preocupa que el repositorio crezca en archivos (2026-11-19). Criterio vigente: antes de crear un archivo se pregunta si ayuda a entender un concepto del curso o a operar el agente, y se prefiere ampliar uno existente.

## Decisiones tomadas

- Las decisiones que ya son reglas (cuestionarios, omisiones del PDF, Glosario y Preguntas frecuentes, git, Conventional Commits, rayas largas, límite de líneas, carpeta `estudio/`, términos del curso, claves, lo del proyecto en el proyecto) están en `AGENTS.md`.
- 2026-11-17: El PDF fuente se renombró a `certiprof-ai-agent-manager-aiam-guia-de-autoestudio-es.pdf` (antes `document.pdf`).
- 2026-11-17: Derechos: el PDF no trae aviso de copyright ni licencia, solo el de marca registrada; `README.md` lleva una nota de autoría que atribuye el contenido y la marca a Certiprof, LLC.
- 2026-11-17: Repositorio público `edgardo001/ai-agent-manager-estudio-aiam-certiprof-studio`, con todo el contenido (incluidos el PDF y la conversión); se recreó con un historial limpio sin firmas ni menciones del asistente.
- 2026-11-17: Se corrigen erratas evidentes y se traducen las oraciones completas en inglés (inicio de la sección 4.3); el usuario puede pedir restaurar el original.
- 2026-11-17: Material impreso: apuntes visuales tipo “apuntes de clase” (diagramas, poco texto, letra manuscrita), no fichas de pregunta y respuesta. Aprobó el estilo del Módulo 1 tras pedir menos texto.
- 2026-11-17: El documento del curso se separó en cinco archivos por módulo sin cambiar el contenido; el archivo único `AI-Agent-Manager.md` se eliminó.
- 2026-11-17: Resúmenes por módulo solo en párrafos, en carpeta propia, validados por varios agentes contra alucinaciones y omisiones.
- 2026-11-18: Sin frontmatter en los archivos de estudio (el lector de voz lo lee y el índice ya cubre la navegación).

## Estado actual

- Curso convertido y completo en `estudio/modulos/` (cinco archivos, 50 preguntas con sus respuestas), auditado contra el PDF.
- Material de estudio completo: resúmenes, apuntes (un PDF por módulo y `apuntes-completos.pdf`), plantillas con su guía, glosario, preguntas frecuentes y dos diagramas del curso (sistema agentic y caso UPS ORION, vistos como flujos de n8n). Los conteos están en `estudio/indice.md`.
- Proyecto de agente: etapas 0 a 3 terminadas, probadas por el usuario y revisadas con EGM; decisiones hasta D15; simplificación del 2026-11-19 aplicada (en `docs/`, de 13 a 9 documentos; AGENTS.md de 198 a 152 líneas y este archivo de 123 a 68), con commit. Etapa 4 (reglas en código, auditoría y kill switch, D16) escrita, revisada con EGM y fidelidad (pedido del usuario) y corregida el 2026-11-19: el mensaje del cliente se confirma antes de atenderlo y la cancelación exige intención u objeto (decisiones del usuario); 89 pruebas. El usuario la probó y aprobó el mismo día. Consulta del usuario: si la base guarda los costos por consulta o por embedding; respuesta: chat por ticket (tickets) y por llamada (auditoría), embeddings no (menos del 1% y Gemini no informa sus tokens); se decidió no agregar código, documentado en docs/modelos-y-costos.md, sección 7. Etapa 5 iniciada el 2026-11-19 con el chat de vuelta en Gemini; a pedido del usuario, example.env lista los modelos de chat y de embeddings de Gemini y OpenRouter (el nombre cambia según el proveedor). Pruebas adversariales de las reglas hechas (docs/pruebas/2026-11-19-etapa-5.md); decisión del usuario: arreglar los trucos de caracteres y al otro cliente por su nombre, y dejar a las evals lo que un patrón no ve. Juez elegido por el usuario: gemini-3.5-flash. Consulta del usuario sobre la enumeración de códigos de cliente y tickets: se documentó en D4 (identidad desde el token, comprobar dueño del ticket, UUID solo como capa extra, límite de pedidos), sin cambiar el esquema. A pedido del usuario se creó docs/seguridad-owasp.md (OWASP Top 10 para LLM, edición 2025, y para APIs, 2023; varios sitios secundarios citan una edición LLM 2026 que la página oficial no mostraba el 2026-11-19) y la regla 18 del plan: usarlo para mejorar el código sin perder la simpleza; próxima revisión 2027-05-19. Sigue: golden dataset, búsqueda sola, juez y aprobación del prompt. Estado y reglas en el [plan](estudio/proyecto-agente/agente-soporte-n1/docs/plan-del-proyecto.md), decisiones en [decisiones.md](estudio/proyecto-agente/agente-soporte-n1/docs/decisiones.md), lo aprendido en [lecciones-aprendidas.md](estudio/proyecto-agente/agente-soporte-n1/docs/lecciones-aprendidas.md) y los informes en [revisiones/](estudio/proyecto-agente/agente-soporte-n1/docs/revisiones/).

## Consultas del usuario

Solo las del curso. Las del proyecto de agente están en su documentación (ver “Proyecto de agente” más abajo).

- 2026-11-17: “Accountability”, “RPA”, “C-suite”, “PwC” y “CSAT”. Agregados al Glosario.
- 2026-11-17: “¿Qué es un AI Agent Manager?”: con ella se creó Preguntas frecuentes.
- 2026-11-17: “¿Cómo traduzco objetivos en gobernanza de agentes?”. Preguntas frecuentes (seis pasos, con el ejemplo de soporte B2B de la sección 2.5).
- 2026-11-17: “Necesito ejemplos de métricas de valor” y “¿Cuáles son las métricas de éxito?”. Unidas en una sola pregunta frecuente por no redundancia; los ejemplos por área no vienen en el curso y están marcados.
- 2026-11-17: “¿Qué es un audit trail? ¿Cómo se hace?”. Respuesta en Preguntas frecuentes y entrada corta en el Glosario; gran parte del “cómo” está marcada como externa al curso.
- 2026-11-17: “¿Cómo hago gestión estratégica?”. Preguntas frecuentes: siete prácticas que sintetizan los cinco módulos (síntesis marcada como propia).
- 2026-11-17: “Onboarding agentic”, “SOP”, “Boundary testing” y “Vendor”. Agregados al Glosario.
- 2026-11-17: “Ejemplos de auditoría de seguridad como Agent Manager”. Preguntas frecuentes; los ejemplos concretos están marcados como externos.
- 2026-11-17: “Agent sprawl” (Glosario) y “Dame ejemplos de agent sprawl” (Preguntas frecuentes, con la pregunta 5 del Módulo 2 y tres ejemplos externos marcados); la entrada del Glosario remite a la pregunta.
- 2026-11-17: Diagramas pedidos: el sistema agentic visto como flujo de n8n y el caso UPS ORION (sección 5.5), donde el agente recomienda y el conductor decide. En `estudio/diagramas.md`, con la analogía de n8n marcada como externa.
- 2026-11-17: “Taxonomía” en las plantillas: creyó que era un error; al saber que es término del curso, se revirtió el cambio y se agregó “Taxonomía de tareas” al Glosario.
- 2026-11-17: “¿Qué es el framework JD+SOP?”. Explicación completa en Preguntas frecuentes; la entrada SOP remite a ella.
- 2026-11-18: “No sé qué es un JD+SOP”. Se complementó esa pregunta frecuente y se agregó “JD” al Glosario. “Ejemplos de JD+SOP”: se agregó a la plantilla 05 el ejemplo como system prompt, con lo externo marcado.
- 2026-11-18: Pidió que todo quede referenciado entre sí: se creó `estudio/indice.md` con su generador.
- 2026-11-18: “¿Por qué Soporte N1? ¿Qué es N1?” y “¿También estaríamos creando un RAG?”. Agregados al Glosario N1 (nivel 1 de soporte, no un nivel de autonomía) y RAG, ambos marcados como términos que no vienen del curso.

## Proyecto de agente

- Desde el 2026-11-18, el usuario construye el Agente de Soporte N1 de la sección 2.5 en `estudio/proyecto-agente/agente-soporte-n1/` (Python, FastAPI, PostgreSQL con pgvector y Docker Compose), con el principio “todos los conceptos del curso, a escala pequeña”.
- Cada pedido, decisión y consulta técnica del proyecto quedó en su documentación: el registro de cambios del plan, `decisiones.md` (D1 a D15), `lecciones-aprendidas.md`, `pruebas/` y `revisiones/`.
- Proveedores: desde el 2026-11-19 el chat volvió a Gemini (`gemini-3.1-flash-lite`) y los embeddings siguen en Gemini; OpenRouter queda probado como alternativa (D13 y D14, detalle en `docs/modelos-y-costos.md`).
- Guardarraíl de claves en la configuración global de la herramienta del usuario, fuera del repositorio (regla en `AGENTS.md`).
- 2026-11-19: las dos copias de respaldo de la configuración local en src/docker/ ya no existen (las borró el usuario); pendiente cerrado. Cada uso de revisar_env --ordenar vuelve a crear una copia, ignorada por git, que el usuario puede borrar.

## Pendientes y temas abiertos

**Lista temporal de la etapa 5 (pedido del usuario, 2026-11-19): se trabaja de a uno, el usuario decide cada paso, y la lista se borra al cerrar la etapa.**

1. ~~Commits atómicos de lo hecho el 2026-11-19~~: hechos y subidos el mismo día (seis commits, de cfd3730 a 145b14f).
2. ~~El usuario instala Hypothesis y corre las pruebas gratis~~: hecho el 2026-11-19 en su equipo, 111 pasan y 13 fallan como se espera (16 segundos).
3. ~~Consulta de modelos~~: el usuario decidió dejarla como `scripts/listar_modelos.py`; hecho y probado el 2026-11-19.
4. ~~Variables nuevas~~: agregadas el 2026-11-19 (`LLM_JUEZ_PROVEEDOR`, `LLM_MODELO_JUEZ=gemini-3.5-flash`, `EXIGIR_PROMPT_APROBADO=false`); el juez responde JSON pero tarda de 22 a 39 segundos por llamada. Falta que el usuario corra `revisar_env --ordenar`.
5. ~~Golden dataset~~: `tests/evals/casos.jsonl` con 40 casos aprobados por el usuario el 2026-11-19 (22 de mezcla realista y 18 casos borde; la propuesta decía 38 por un error de suma). Falta que el usuario corra `revisar_env --ordenar` (pendiente 4).
6. ~~Búsqueda sola~~: `tests/evals/test_busqueda.py`, 2026-11-19: recall@5 93% (pasa el 90%), MRR 0,89; `limites-del-soporte.md` casi nunca aparece en las búsquedas (dos casos fallidos); el parecido no separa lo que tiene solución de lo que no.
7. El juez y las evals con el modelo real: código escrito y probado con un modelo falso el 2026-11-19 (61 pruebas; la base quedó sin tickets). Falta la corrida real (unas 150 llamadas, de 30 a 40 minutos): el usuario pidió lanzarla el 2026-11-19, pero se detuvo a los pocos minutos porque debía apagar el equipo; no quedó resultado. Al retomar: relanzarla con `python -m pytest tests/evals` desde src/backend. Todo lo de los pendientes 3 a 7 está sin commit.
8. `aprobar_prompt.py`, la columna de la huella aprobada y la barrera de D15.
9. Cierre: pendientes de seguridad-owasp.md (regla 18), revisión con EGM y de fidelidad, prueba del usuario y commits.

Cerrados antes de la etapa 4 (2026-11-19): sandbox, activarlo al cambiar a un modelo o herramienta en que confíe menos; claves gratuitas sin tope ni restricción; no agregar más claves (detalle en `docs/modelos-y-costos.md`, sección 4b).

**Otros:**

- Decidir si borrar la copia previa de su configuración global (`settings.json.antes-guardarrail`).
- Opcional: comparar las respuestas del agente con y sin RAG.
- Plantillas 01, 03 y 11: describen el agente de ejemplo en Nivel 2 y el proyecto lo reclasificó a Nivel 3 (2026-11-18); falta corregirlas y revisar si las menciones a Nivel 2 de las plantillas 04, 08 y 15 se refieren al agente. También siguen pendientes de aprobación las correcciones que propuso la revisión de las plantillas por agentes.
- Inconsistencias del curso ya anotadas, por revisar con el usuario: 84% frente a 83% de completitud en el Módulo 5; dos listas distintas de universidades de la AI Agent Index 2025; “módulo anterior” en la sección 4.3 cuando la taxonomía está en la 4.2.
- Ofrecido y sin respuesta: poblar de antemano el Glosario con los términos técnicos principales del curso.
