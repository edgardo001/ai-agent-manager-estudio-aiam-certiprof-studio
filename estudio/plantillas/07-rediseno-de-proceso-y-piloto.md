# 07 · Rediseño de proceso y piloto

> **Para qué sirve:** aplicar el método AIAM™ de 5 pasos para rediseñar un proceso como trabajo de un equipo híbrido (personas y agentes), con traspasos definidos por condiciones objetivas, un piloto medido y un plan para escalar.
> **Cuándo llenarla:** una por cada proceso priorizado en la plantilla 01, antes de poner el agente en producción. Se actualiza al cerrar el piloto, al escalar y luego cada trimestre.
> **Quién la llena y quién la aprueba:** la llena el Workflow Designer (diseñador de flujos de trabajo), bajo dirección del AI Agent Manager (AIAM™). El AIAM™ lidera y responde por el rediseño (responsabilidad 2 del Módulo 4). La aprobación para escalar la da la dirección del área (no viene en el curso quién aprueba esta plantilla en particular).
> **Con qué se llena:** observación y entrevistas con quienes hacen el trabajo, la taxonomía de la plantilla 01, las instrucciones del agente (plantilla 05), datos de tiempos y errores del proceso actual.
> **Base en el curso:** Módulo 4, sección 4.3 (método AIAM™ en 5 pasos) y sección 4.2 (taxonomía); preguntas 5 y 6 del Módulo 4.
> **Se conecta con:** se alimenta de 01 (01-oportunidades-y-taxonomia.md). Alimenta a 05 (05-instrucciones-del-agente.md, protocolos de escalamiento), 06 (06-onboarding-y-aceptacion.md), 08 (08-gestion-del-cambio-y-roles.md), 09 (09-plan-de-supervision.md), 13 (13-auditoria-trimestral-del-portafolio.md) y 15 (15-evaluacion-de-escala-y-madurez.md). La línea base del proceso actual sirve también a 02 (02-business-case.md).

## Cómo llenarla

1. **Paso 1, AS-IS (cómo se hace hoy):** documente cada actividad real: quién la hace, con qué frecuencia, qué datos usa y qué decide. Incluya excepciones y atajos no documentados.
2. **Paso 2, clasificar:** aplique la taxonomía de la plantilla 01 a cada actividad y escriba la justificación.
3. **Paso 3, TO-BE (cómo se hará):** rediseñe el flujo completo y defina cada handoff (traspaso entre agente y humano) con una condición objetiva, la información que lo acompaña y el SLA (tiempo de respuesta acordado) en cada dirección.
4. **Paso 4, piloto:** antes de lanzar, fije las métricas de éxito. Lance con un equipo pequeño en contexto controlado y registre lo que el agente no pudo resolver solo.
5. **Paso 5, escalar y refinar:** extienda al equipo completo con las lecciones del piloto y agende la revisión trimestral.

## Plantilla

**Proceso:** `[escriba aquí…]`   **Agente:** `[nombre, igual que en la plantilla 03]`   **Responsable del rediseño:** `[Workflow Designer]`

### Paso 1. Mapa del proceso actual (AS-IS)

El objetivo no es un diagrama perfecto, sino una comprensión honesta del trabajo real (sección 4.3).

| N.º | Actividad | Quién la ejecuta | Frecuencia | Datos que consume | Decisiones que implica | Excepciones o atajos no documentados |
|---|---|---|---|---|---|---|
| 1 | `[…]` | `[…]` | `[…]` | `[…]` | `[…]` | `[…]` |

**Línea base del proceso actual** (no viene en el curso como campo de este paso; sirve para comparar el piloto): tiempo de ciclo `[…]`, tasa de error `[…]`, volumen `[…]`.

### Paso 2. Clasificación con la taxonomía

| N.º | Actividad | Territorio | Justificación (para futuras revisiones) |
|---|---|---|---|
| 1 | `[…]` | `[Agente / Humano / Colaboración activa]` | `[…]` |

### Paso 3. Proceso futuro (TO-BE) y puntos de handoff

**Flujo rediseñado:** `[describa el flujo completo, paso a paso, indicando quién ejecuta cada paso]`

| Handoff | Dirección | Condición objetiva que lo activa | Información que debe acompañarlo | SLA de respuesta |
|---|---|---|---|---|
| H1 | `[Agente → Humano / Humano → Agente]` | `[umbral de confianza del agente, tipo de excepción, tiempo de espera máximo o categoría de cliente]` | `[…]` | `[…]` |

Verificación de cada handoff:

- [ ] La condición es objetiva y medible; no dice "cuando sea necesario".
- [ ] No depende del criterio del agente ni de la intuición del humano.
- [ ] Indica qué información viaja con la tarea (contexto completo).
- [ ] Tiene SLA definido en cada dirección.

### Paso 4. Piloto con un subconjunto

| Campo | Qué escribir |
|---|---|
| Equipo piloto | `[quiénes, cuántas personas]` Un equipo pequeño. |
| Contexto controlado | `[qué casos, canal, período]` |
| Métricas de éxito (definidas ANTES del piloto) | Reducción del tiempo de ciclo: `[meta]`. Tasa de error: `[meta]`. Satisfacción del equipo humano: `[meta]`. Calidad del output (resultado del agente): `[meta]`. |
| Fechas | `[inicio – fin]` |

**Registro de lo que el agente no pudo resolver solo:**

| Fecha | Caso | Por qué no pudo | Quién lo resolvió | ¿Cambia la taxonomía o el handoff? |
|---|---|---|---|---|
| `[…]` | `[…]` | `[…]` | `[…]` | `[Sí / No: qué cambia]` |

**Resultados del piloto:** `[valor logrado de cada métrica frente a la meta y a la línea base]`

### Paso 5. Escalar y refinar continuamente

| Campo | Qué escribir |
|---|---|
| Lecciones del piloto aplicadas | `[…]` |
| Plan de extensión al equipo completo | `[quiénes, cuándo]` |
| Próxima revisión trimestral | `[fecha]` Revisar: la taxonomía, los criterios de handoff y los umbrales de intervención humana, según el historial acumulado y la mejora de los datos. |

## Ejemplo lleno

**Proceso:** soporte técnico de nivel 1 en Customer Success (éxito del cliente) de una empresa de software B2B (que vende a otras empresas), ejemplo de la sección 2.5. Tiempos, volúmenes y resultados son datos ficticios de ejemplo; las condiciones de escalamiento y las metas vienen de la sección 2.5.

**Paso 1 (AS-IS):**

| N.º | Actividad | Quién | Frecuencia | Datos | Decisiones | Excepciones o atajos |
|---|---|---|---|---|---|---|
| 1 | Leer y clasificar el ticket (solicitud de soporte) | Analista de soporte | 300 por día | Portal de soporte | Prioridad y categoría | Los clientes conocidos se atienden "por fuera" del portal |
| 2 | Buscar historial y solución | Analista | Cada ticket | CRM (gestión de clientes), base de conocimiento | Si hay solución documentada | Soluciones en notas personales no publicadas |
| 3 | Responder o derivar | Analista | Cada ticket | Plantillas de respuesta | Resolver o pasar a nivel 2 | Descuentos ofrecidos sin autorización |

Línea base: tiempo promedio de resolución de 25 minutos.

**Paso 2:** actividades 1 y 2: Agente (clasificación inicial y consulta de datos estructurados). Actividad 3: Colaboración activa (el agente responde lo documentado; el humano atiende escalaciones y cierres clave).

**Paso 3 (handoffs, según los protocolos de escalamiento de la sección 2.5):**

| Handoff | Dirección | Condición objetiva | Información que acompaña | SLA |
|---|---|---|---|---|
| H1 | Agente → Humano | El ticket no tiene resolución documentada | Ticket, historial del CRM, búsquedas hechas | 30 minutos (ficticio) |
| H2 | Agente → Humano | El cliente menciona cancelación | Ticket, historial, mensaje textual del cliente | 15 minutos (ficticio) |
| H3 | Agente → Humano | El tiempo de resolución supera 8 minutos | Ticket y pasos ya intentados | 30 minutos (ficticio) |
| H4 | Humano → Agente | Caso resuelto con una solución nueva | Solución para la base de conocimiento | 1 día hábil (ficticio) |

**Paso 4:** equipo piloto de 3 analistas, solo tickets en español del portal, 4 semanas. Metas (sección 2.5): resolución autónoma mayor o igual al 80%, CSAT (satisfacción del cliente) mayor o igual a 4,2 sobre 5, tasa de escalamiento menor o igual al 20% y tiempo promedio menor o igual a 3 minutos. Lo no resuelto: consultas sobre una función recién lanzada sin artículo en la base de conocimiento. Cambio: se agrega el handoff H4. Resultados: 76% de resolución autónoma y CSAT de 4,3 (ficticios).

**Paso 5:** se extiende a todo el equipo después de publicar los artículos faltantes; próxima revisión trimestral fijada para revisar taxonomía, handoffs y umbrales.

## Errores comunes

- Handoffs ambiguos ("el agente escala cuando sea necesario"): según el World Economic Forum (Future of Jobs Report 2025), la ambigüedad en los handoffs es la causa número uno de fricción en equipos híbridos (sección 4.3; pregunta 5 del Módulo 4).
- Automatizar lo que debería seguir siendo humano, o retener en humanos lo que el agente puede hacer con más velocidad y consistencia: los dos errores más comunes del rediseño (sección 4.3).
- Confundir rediseño con automatización: automatizar reemplaza pasos humanos por pasos de máquina; el rediseño híbrido reimagina el flujo completo (sección 4.3).
- Definir las métricas de éxito después del piloto, en vez de antes (sección 4.3, paso 4).
- Reentrenar o escalar ante una caída de desempeño sin diagnosticar antes la causa raíz: el diagnóstico precede a la intervención (pregunta 6 del Módulo 4).
