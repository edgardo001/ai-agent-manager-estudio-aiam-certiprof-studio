# 01 · Oportunidades y taxonomía de tareas

> **Para qué sirve:** identificar los 3 a 5 procesos del área más candidatos a transformación con agentes, clasificar sus tareas (qué hace el agente, qué retiene el humano y dónde colaboran) y proponer el nivel de autonomía de cada uno, con criterios de impacto medible.
> **Cuándo llenarla:** al inicio, antes de diseñar o comprar cualquier agente. Se revisa cada trimestre (el curso pide revisar la taxonomía trimestralmente) o cuando cambian las condiciones del negocio.
> **Quién la llena y quién la aprueba:** la llena el AI Agent Manager (AIAM™), con apoyo del Workflow Designer (quien diseña y documenta los procesos) y de las personas que hoy hacen el trabajo. La aprueba la dirección del área (no viene en el curso quién aprueba esta plantilla en particular; se sugiere la dirección del área).
> **Con qué se llena:** lista de procesos actuales del área, volúmenes y frecuencias, calidad y disponibilidad de los datos, consecuencias conocidas de los errores, entrevistas con quienes ejecutan el trabajo.
> **Base en el curso:** Módulo 1, sección 1.2 (agente frente a RPA y chatbot; los 4 niveles de autonomía) y quinta responsabilidad del Módulo 1 (identificación de oportunidades); Módulo 4, sección 4.2 (taxonomía de tareas: 4 variables y 6 tipos de tarea).
> **Se conecta con:** alimenta a 02 (02-business-case.md), 03 (03-registro-de-agentes.md), 04 (04-ficha-de-identidad-del-agente.md) y 07 (07-rediseno-de-proceso-y-piloto.md, paso 2). Se revisa junto con 13 (13-auditoria-trimestral-del-portafolio.md).

## Cómo llenarla

1. Liste los procesos actuales del área. No filtre todavía: anote todos los que conozca.
2. Para cada proceso, evalúe las 4 variables de la taxonomía (sección 4.2): variabilidad del contexto, consecuencia del error, necesidad de relación y disponibilidad de datos estructurados.
3. Ubique cada tarea del proceso en uno de los 6 tipos de tarea y decida quién lidera (agente, humano o colaboración), escribiendo la justificación.
4. Decida si de verdad hace falta un agente o basta una automatización RPA (robot de reglas fijas) o un chatbot (asistente conversacional limitado), con la tabla de la sección 1.2.
5. Proponga el nivel de autonomía (1 a 4) y anote la supervisión que ese nivel exige.
6. Priorice y quédese con 3 a 5 procesos candidatos, cada uno con un criterio de impacto medible.

## Plantilla

### A. Inventario de procesos del área

| Proceso | Qué escribir |
|---|---|
| Nombre del proceso | `[escriba aquí…]` Nombre corto que entienda cualquiera del área. |
| Quién lo ejecuta hoy | `[escriba aquí…]` Rol o equipo. |
| Volumen y frecuencia | `[escriba aquí…]` Cuántas veces por día, semana o mes. |
| Dolor actual | `[escriba aquí…]` Qué cuesta o falla hoy (tiempo, errores, espera). Campo práctico (no viene en el curso). |

### B. Las 4 variables de la taxonomía (una tabla por proceso)

Marque Alta, Media o Baja y justifique. Regla del curso: más variabilidad, más consecuencia del error y más necesidad de relación empujan la tarea hacia el humano; sin datos limpios y estructurados, el agente genera ruido, no valor.

| Variable | Valoración | Qué escribir |
|---|---|---|
| Variabilidad del contexto | `[Alta / Media / Baja]` | ¿Los casos se parecen entre sí o cada uno es distinto? Las tareas muy variables requieren criterio humano. |
| Consecuencia del error | `[Alta / Media / Baja]` | ¿Qué pasa si sale mal (dinero, cliente, legal)? Mayor consecuencia exige supervisión humana. |
| Necesidad de relación | `[Alta / Media / Baja]` | ¿Requiere empatía, negociación o confianza? Si es así, se queda en el dominio humano. |
| Datos estructurados disponibles | `[Sí / Parcial / No]` | ¿Existen datos limpios y ordenados que el agente pueda usar? |

### C. Clasificación de tareas (6 tipos de la sección 4.2)

| Tarea del proceso | Tipo de tarea | Quién lidera | Modelo de colaboración | Justificación |
|---|---|---|---|---|
| `[tarea]` | `[uno de los 6 tipos]` | `[Agente / Humano / Colaboración]` | `[cómo trabajan juntos]` | `[por qué, citando las 4 variables]` |

Referencia rápida de los 6 tipos (sección 4.2):

| Tipo de tarea | Señales de que lidera el agente | Señales de que lidera el humano | Colaboración recomendada |
|---|---|---|---|
| Procesamiento de datos y reportes | Volumen alto, estructura fija, periodicidad frecuente | Datos irregulares, contexto ambiguo, fuentes no integradas | El agente genera; el humano valida y decide sobre hallazgos |
| Comunicación externa con clientes | FAQ (preguntas frecuentes), seguimiento, actualizaciones de estado, primeras respuestas | Negociaciones, quejas escaladas, relaciones estratégicas | Agente como primera capa; humano en escalaciones y cierres clave |
| Análisis estratégico y decisiones | Agregación de datos, escenarios, backtesting (probar un modelo con datos pasados) | Señales débiles, factores cualitativos | El agente prepara el tablero analítico; el humano decide |
| Gestión de excepciones y problemas | Clasificación inicial, enrutamiento, apertura de tickets (solicitudes registradas) | Casos complejos, crisis, decisiones éticas | El agente diagnostica y enruta; el humano resuelve lo no estructurado |
| Onboarding (incorporación) y formación de equipos | Material de orientación, quizzes (pruebas cortas), seguimiento de progreso | Mentoría, conversaciones de carrera, cultura | El agente como plataforma; el humano como guía y referente |
| Coordinación de proyectos | Actualizaciones de estado, alertas de hitos, tareas rutinarias | Conflictos, re-planificación, alineación política | El agente lleva el tablero; el humano conduce reuniones y decide |

### D. ¿Agente, RPA o chatbot? (sección 1.2)

- [ ] El proceso exige decisiones de varios pasos en escenarios ambiguos (si no, quizá basta RPA, que sigue reglas fijas).
- [ ] El proceso necesita adaptarse a contextos nuevos sin reprogramación.
- [ ] El proceso usa varias herramientas, APIs (conexiones entre sistemas) o bases de datos.
- [ ] El proceso va más allá de una interacción conversacional puntual (si no, quizá basta un chatbot).

### E. Nivel de autonomía propuesto (sección 1.2)

| Campo | Qué escribir |
|---|---|
| Nivel propuesto | `[1 Asistencia / 2 Automatización / 3 Augmentación / 4 Autonomía Total]` |
| Por qué ese nivel | `[escriba aquí…]` |
| Supervisión que exige | `[escriba aquí…]` Nivel 1: humano en el loop (en el circuito) para cada decisión. Nivel 2: monitoreo de calidad del output (resultado) y umbrales de excepción. Nivel 3: revisión periódica del proceso, auditoría de calidad y métricas de negocio. Nivel 4: límites operacionales precisos, protocolos de escalamiento, criterios de kill switch (apagado de emergencia) y auditoría continua. |

### F. Priorización final (3 a 5 procesos)

| Prioridad | Proceso | Impacto medible esperado | Indicador para medirlo | Nivel de autonomía |
|---|---|---|---|---|
| 1 | `[proceso]` | `[qué mejora y cuánto]` | `[métrica de negocio]` | `[1 a 4]` |

## Ejemplo lleno

Área de Customer Success (éxito del cliente) de una empresa de software B2B (que vende a otras empresas), el mismo ejemplo de la sección 2.5. Los volúmenes son datos ficticios de ejemplo.

**Proceso 1: soporte técnico de nivel 1 (tickets del portal).** Variabilidad: Media (muchos problemas repetidos, con solución documentada). Consecuencia del error: Media. Necesidad de relación: Baja en preguntas frecuentes, Alta si el cliente habla de cancelar. Datos: Sí (CRM, sistema de gestión de clientes, y base de conocimiento).

| Tarea | Tipo | Quién lidera | Justificación |
|---|---|---|---|
| Responder problemas con solución documentada | Comunicación externa con clientes | Agente (primera capa) | Preguntas frecuentes y primeras respuestas, con datos estructurados |
| Clasificar y enrutar tickets | Gestión de excepciones | Agente | Clasificación inicial y enrutamiento |
| Cliente que menciona cancelación | Comunicación externa con clientes | Humano | Relación estratégica; además es condición de escalamiento en la 2.5 |
| Casos sin resolución documentada | Gestión de excepciones | Humano | Caso no estructurado |

Agente o RPA: agente, porque consulta historial en el CRM, busca en la base de conocimiento y decide en varios pasos. Nivel propuesto: 2, Automatización (el curso pone como ejemplo de Nivel 2 la clasificación de tickets de soporte). Impacto medible (de la sección 2.5): resolver el 80% de los tickets de nivel 1 sin intervención humana, en menos de 3 minutos promedio, con CSAT (satisfacción del cliente) mayor o igual a 4,2 sobre 5.

**Proceso 2: aprobación de facturas** (pertenece al área de operaciones, no a soporte; es el ejemplo de la pregunta 1 del Módulo 4 y se incluye para mostrar otro tipo de proceso). El agente lidera recepción, verificación contra el ERP (sistema de gestión de la empresa), validación del monto con el presupuesto y detección de duplicados; la aprobación final queda en el humano por su consecuencia y responsabilidad.

**Proceso 3: reporte semanal de tickets** (datos ficticios de ejemplo). Procesamiento de datos y reportes: el agente genera, la supervisora valida y decide sobre los hallazgos. Nivel 2.

## Errores comunes

- Implementar un agente en Nivel 4 asumiendo que el riesgo es el mismo que en Nivel 2: la diferencia es exponencial (sección 1.2, Nota Crítica).
- Usar "agente", "chatbot" y "automatización" como sinónimos, lo que genera expectativas incorrectas e implementaciones mal diseñadas (sección 1.2).
- Asignar al agente tareas sin datos limpios y estructurados: genera ruido, no valor (sección 4.2).
- Tratar la taxonomía como algo fijo: debe revisarse cada trimestre, porque lo que hoy requiere supervisión humana intensiva puede ser territorio del agente en seis meses, y viceversa (sección 4.2).
- Dejar que cada persona decida individualmente qué delega y qué retiene, sin una taxonomía explícita (Reflexión Estratégica del Módulo 4).
