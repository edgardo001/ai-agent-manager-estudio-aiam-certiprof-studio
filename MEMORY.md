# MEMORY.md — Memoria del proyecto

Este archivo guarda lo que un agente de IA necesita saber para continuar el trabajo sin depender de conversaciones anteriores: contexto, decisiones, estado actual, consultas realizadas y pendientes. Las reglas de cómo hacer el trabajo están en `AGENTS.md`; aquí va el “qué pasó y dónde estamos”. Se actualiza periódicamente (ver `AGENTS.md`, sección “Mantenimiento de los archivos del proyecto”).

## Contexto del usuario

- Estudia el curso AI Agent Manager (AIAM™) de Certiprof escuchándolo con un lector text-to-speech.
- Necesita que nada del contenido se pierda: todo concepto, cifra, fuente y ejemplo debe estar en el documento.
- Quiere buscar rápido los términos y dudas que va consultando; por eso las respuestas se guardan en `estudio/glosario.md` y `estudio/preguntas-frecuentes.md`. Las prefiere breves: ni poco ni mucho texto.
- Escribe en español; todas las respuestas y documentos van en español con tildes correctas.
- Prefiere que se le consulte cuando hay dudas reales, en lugar de suponer.

## Decisiones tomadas

- 2026-11-17 — Cuestionarios: se conserva la pregunta, el texto completo de la respuesta correcta y la justificación de por qué es correcta. Se eliminan las alternativas incorrectas, pero se rescatan los conceptos que se explicaban al descartarlas.
- 2026-11-17 — Se omiten duración y nivel de cada módulo. Se conservan en prosa los checklists, las reflexiones estratégicas y las responsabilidades del AIAM™.
- 2026-11-17 — Se omiten la portada (página 1) y el cierre y las páginas de Certiprof (páginas 93 a 97).
- 2026-11-17 — El archivo final se llama `AI-Agent-Manager.md` y está en la carpeta `estudio/`, no en la raíz del repositorio (decisión del usuario). La carpeta `estudio/` irá acumulando todos los archivos que se generen a partir del curso.
- 2026-11-17 — Se corrigen erratas evidentes del PDF y se traducen al español las oraciones completas que habían quedado en inglés (inicio de la sección 4.3); los términos técnicos en inglés se mantienen. El usuario puede pedir restaurar el original en inglés.
- 2026-11-17 — Las consultas del usuario se guardan en archivos propios: `estudio/preguntas-frecuentes.md` (dudas conceptuales) y `estudio/glosario.md` (términos, en orden alfabético). Antes estaban al final del documento del curso. Largo estándar: de 80 a 120 palabras por término y de 150 a 250 por pregunta, porque las primeras respuestas le resultaron demasiado largas.
- 2026-11-17 — Se crean `README.md` y `MEMORY.md`, que junto con `AGENTS.md` se mantienen actualizados.
- 2026-11-17 — Los commits de git (y las descripciones de pull requests) no llevan firmas de agentes, y no se menciona el nombre del asistente de IA en ninguna parte del proyecto. Regla registrada en `AGENTS.md`.
- 2026-11-17 — El usuario renombró el PDF fuente: ahora se llama `certiprof-ai-agent-manager-aiam-guia-de-autoestudio-es.pdf` (antes `document.pdf`).
- 2026-11-17 — Derechos: el PDF no trae aviso de copyright ni licencia, solo el aviso de marca registrada de Certiprof. El aviso de `README.md` se cambió de “debe mantenerse privado” a una nota de autoría que atribuye el contenido y la marca a Certiprof, LLC.
- 2026-11-17 — Repositorio: carpeta y repositorio de GitHub `edgardo001/ai-agent-manager-estudio-aiam-certiprof-studio`, público y con todo el contenido (incluidos el PDF y la conversión), por decisión del usuario. Se recreó desde cero, con un historial limpio sin firmas ni menciones del asistente de IA.
- 2026-11-17 — Material de repaso impreso: el usuario eligió apuntes visuales tipo “apuntes de clase” (diagramas, poco texto, letra manuscrita en títulos y notas), no fichas de pregunta y respuesta separadas. Aprobó el estilo del Módulo 1 tras pedir menos texto. Cada módulo lleva un recuadro de siglas y términos en inglés.
- 2026-11-17 — `AGENTS.md`, `MEMORY.md` y `README.md` no deben superar las 200 líneas cada uno; si pasan el límite, se podan resumiendo sin perder lo importante. Regla registrada en `AGENTS.md`.
- 2026-11-17 — El usuario pidió un archivo de diagramas Mermaid (`estudio/diagramas.md`) al que se irán agregando los que pida.

## Estado actual

- `estudio/AI-Agent-Manager.md` completo: 5 módulos, unas 26.500 palabras, 50 preguntas de validación con 50 respuestas. Sin tablas, viñetas, citas en bloque ni emojis. Termina en el Módulo 5. Encabezados de sección unificados según el PDF (revisión del 2026-11-17).
- Proceso usado: un agente por módulo para la conversión y una segunda pasada de auditoría por módulo contra el PDF, página por página.
- `estudio/preguntas-frecuentes.md`: 7 preguntas. `estudio/diagramas.md`: 2 diagramas (sistema agentic genérico y caso UPS ORION, ambos vistos como flujo de n8n). `estudio/glosario.md`: 9 términos (Accountability, Audit trail, Boundary testing, C-suite, CSAT, Onboarding agentic, PwC, RPA y SOP).
- Apuntes visuales en `estudio/apuntes/` completos: 28 hojas A4 (Módulo 1, 4 hojas; módulos 2 a 5, 6 hojas cada uno), cada módulo con su recuadro de siglas y términos en inglés. Hay un PDF por módulo y `apuntes-completos.pdf`. Subidos a GitHub el 2026-11-17; `estudio/fichas/` queda fuera del repositorio por ahora.

## Consultas del usuario

- 2026-11-17 — “Accountability” (a raíz de “accountability principal”, Módulo 1, sección 1.2). Agregado al Glosario.
- 2026-11-17 — “RPA” (Módulo 1, sección 1.2, comparación entre RPA, chatbot y agente). Agregado al Glosario.
- 2026-11-17 — “C-suite” (aparece en los módulos 1, 2 y 3). Agregado al Glosario.
- 2026-11-17 — “¿Qué es un AI Agent Manager?”. Pregunta conceptual: con ella se creó la sección “Preguntas frecuentes”.
- 2026-11-17 — “¿Cómo traduzco objetivos en gobernanza de agentes?”. Agregada a Preguntas frecuentes (seis pasos, con el ejemplo de soporte B2B de la sección 2.5).
- 2026-11-17 — “PwC” (fuente citada en el Módulo 1, sección 1.4). Agregado al Glosario.
- 2026-11-17 — “Necesito ejemplos de métricas de valor”. Agregada a Preguntas frecuentes (KPI set de 3.2, ejemplo de 2.5, horizontes de 5.2, capas de 4.6, casos reales y traducción de 5.4).
- 2026-11-17 — “CSAT” (métrica de satisfacción del cliente, módulos 2 y 3). Agregado al Glosario.
- 2026-11-17 — “¿Qué es un audit trail? ¿Cómo se hace, cómo se ejecuta?”. Respuesta completa en Preguntas frecuentes y entrada corta en el Glosario que remite a ella. Gran parte del “cómo” es práctica general y está marcada como externa al curso.
- 2026-11-17 — “¿Cómo hago gestión estratégica?”. Agregada a Preguntas frecuentes: siete prácticas que sintetizan los cinco módulos (síntesis marcada como propia).
- 2026-11-17 — “Onboarding agentic” y “SOP”. Agregados al Glosario.
- 2026-11-17 — “¿Cuáles son las métricas de éxito? Ejemplos para aplicarlos en la realidad”. Agregada a Preguntas frecuentes; los ejemplos por área (cobranza, recursos humanos, ventas) no vienen en el curso y están marcados.
- 2026-11-17 — “Ejemplos de cómo hacer auditoría de seguridad como Agent Manager”. Agregada a Preguntas frecuentes; los ejemplos de pruebas concretas no vienen en el curso y están marcados.
- 2026-11-17 — Diagrama pedido: “qué debe tener un sistema agentic, como si lo hubiéramos desarrollado en n8n”. Agregado a `estudio/diagramas.md`, con la analogía de n8n marcada como externa al curso.
- 2026-11-17 — Pidió otro ejemplo o caso de uso: se agregó el caso real UPS ORION (sección 5.5) como flujo de n8n, donde el agente recomienda y el conductor decide.
- 2026-11-17 — “Boundary testing” con ejemplos. Agregado al Glosario.

## Pendientes y temas abiertos

- Al mover la carpeta, la nota que el agente guardaba en su memoria interna (fuera de esta carpeta, asociada a la ubicación anterior) queda sin uso; su contenido ya está en este archivo y en `AGENTS.md`. Se puede borrar si el usuario lo pide.
- Pendiente de decisión del usuario: qué se sube al repositorio del material de repaso. Además de los apuntes, existen fichas recortables en `estudio/fichas/` (fichas-preguntas.pdf con las 50 preguntas a doble cara, estilos y `generar.py`), creadas antes de que el usuario eligiera el formato de apuntes; el usuario pidió conservarlas por ahora.
- Ofrecido y sin respuesta: poblar de antemano el Glosario con los términos técnicos principales del curso.
