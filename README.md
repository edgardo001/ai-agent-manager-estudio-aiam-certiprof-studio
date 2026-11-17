# AIAM — Material de estudio en formato para escuchar

Versión en prosa del curso **AI Agent Manager (AIAM™)** de Certiprof, preparada para estudiarla con un lector text-to-speech. El PDF original es difícil de leer en voz alta (tablas, cards, cabeceras, pies de página, cuestionarios con alternativas); este repositorio lo convierte en un documento continuo que se escucha de corrido sin perder ningún concepto.

## Contenido

- `certiprof-ai-agent-manager-aiam-guia-de-autoestudio-es.pdf`: el material original del curso (97 páginas, 5 módulos).
- `estudio/`: la carpeta de los archivos generados a partir del curso. Por ahora contiene:
  - `estudio/modulos/`: el documento convertido, listo para escuchar, separado en un archivo por módulo (`modulo-1-el-nuevo-rol-del-manager.md` a `modulo-5-impacto-al-negocio.md`). Es el material principal de estudio.
  - `estudio/preguntas-frecuentes.md`: respuestas a las dudas de comprensión del usuario, en el orden en que las hizo.
  - `estudio/glosario.md`: siglas y términos consultados, en orden alfabético.
  - `estudio/diagramas.md`: diagramas Mermaid de temas del curso, agregados a pedido; GitHub los muestra dibujados.
  - `estudio/plantillas/`: 15 plantillas para aplicar el curso en la práctica (oportunidades, business case, registro de agentes, ficha de identidad, instrucciones, onboarding, rediseño de procesos, gestión del cambio, supervisión, intervenciones, riesgos y seguridad, Governance Board, auditoría trimestral, reporte a la dirección y escala). Empiece por `00-guia.md`, que explica cuál usar y cuándo.
  - `estudio/apuntes/`: apuntes visuales para imprimir y repasar, una serie de hojas A4 por módulo con diagramas y poco texto (`apuntes-modulo-N.pdf` y `apuntes-completos.pdf`). Se regeneran con `python estudio/apuntes/generar.py`, que necesita Chrome o Edge.
- `AGENTS.md`: las reglas de conversión y de mantenimiento que debe seguir cualquier agente de IA que trabaje en este repositorio.
- `MEMORY.md`: la memoria del proyecto: contexto, decisiones tomadas, estado actual, consultas realizadas y pendientes.
- `README.md`: este archivo.

## Estructura de `estudio/modulos/`

Sigue la misma estructura y numeración del PDF:

- Módulo 1. El Nuevo Rol del Manager: De Supervisar Personas a Orquestar Agentes
- Módulo 2. Diseñar y Activar Agentes: El Arte del Onboarding Agentic
- Módulo 3. Supervisión, Auditoría y Performance del Agente
- Módulo 4. Rediseño de Procesos: Equipos Híbridos Humanos + Agentes
- Módulo 5. Impacto al Negocio: Medir, Comunicar y Escalar Resultados

Cada módulo incluye su objetivo de aprendizaje, todas las secciones, los casos reales, el checklist de competencias, las responsabilidades del AIAM™, la reflexión estratégica y las 10 preguntas de validación (solo la pregunta, la respuesta correcta y por qué es correcta).

## Qué se cambió respecto del PDF

- Las tablas, cards, listas y checklists se convirtieron en párrafos, sin perder ninguna celda ni ítem.
- Se eliminaron cabeceras, pies de página, números de página, duración y nivel de cada módulo, la portada y las páginas finales de Certiprof.
- En los cuestionarios se eliminaron las alternativas incorrectas, pero se conservaron los conceptos que se explicaban al descartarlas.
- Cifras y símbolos se escribieron para que se lean bien en voz alta (formato numérico español, “frente a” en lugar de “vs.”, etc.).

El detalle completo de las reglas está en `AGENTS.md`.

## Cómo usarlo

1. Abrir el módulo que corresponda de `estudio/modulos/` en el lector text-to-speech de preferencia.
2. Cuando aparezca un término o una duda, preguntarle al agente de IA. La respuesta se agrega a `estudio/glosario.md` (términos) o a `estudio/preguntas-frecuentes.md` (dudas de comprensión), con un largo pensado para escucharla en uno o dos minutos.

## Mantenimiento

`README.md`, `AGENTS.md` y `MEMORY.md` se actualizan periódicamente, cada vez que cambia algo relevante (ver la sección “Mantenimiento de los archivos del proyecto” en `AGENTS.md`).

## Aviso de derechos

El contenido del curso y la marca CERTIPROF® pertenecen a Certiprof, LLC. Este repositorio es material de estudio personal basado en su guía de autoestudio del programa AI Agent Manager (AIAM™).
