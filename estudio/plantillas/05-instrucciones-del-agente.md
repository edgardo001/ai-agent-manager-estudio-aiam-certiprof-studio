# 05 · Instrucciones del agente (JD + SOP)

> **Para qué sirve:** redactar el documento de instrucciones del agente con el rigor de un JD (job description, descripción de cargo: el "qué" y el "para qué") combinado con un SOP (standard operating procedure, procedimiento operativo estándar: el "cómo", paso a paso). Un JD sin SOP deja al agente sin guía operacional; un SOP sin JD produce un agente que ejecuta pasos sin entender su objetivo (sección 2.5).
> **Cuándo llenarla:** después de la ficha de identidad (plantilla 04) y antes de la validación pre-producción (plantilla 06). Se actualiza cada vez que un error se repite (los errores no corregidos en las instrucciones se repiten, sección 2.4), cuando cambia el alcance y cuando la auditoría detecta deriva.
> **Quién la llena y quién la aprueba:** la redacta y la valida el AI Agent Manager (gestor de agentes de IA), con aportes del Agent Owner (responsable directo del agente, sección 4.5) y de quienes hacen hoy el trabajo. Traducir los objetivos de negocio en instrucciones operativas es responsabilidad del manager (responsabilidad 3 del Módulo 1).
> **Con qué se llena:** la ficha de identidad (plantilla 04), las metas del business case (caso de negocio, plantilla 02), el proceso rediseñado (plantilla 07), la base de conocimiento y los casos reales del proceso.
> **Base en el curso:** Módulo 2, sección 2.5 (siete componentes y ejemplo de soporte B2B), sección 2.4 (el agente opera literalmente), responsabilidad 2 del Módulo 2 y preguntas 3 y 7 del Módulo 2.
> **Se conecta con:** se alimenta de 04 · Ficha de identidad del agente y 07 · Rediseño de proceso y piloto; alimenta a 06 · Onboarding y aceptación (que prueba estas instrucciones) y a 09 · Plan de supervisión (que vigila las métricas del componente 7).

## Cómo llenarla

1. Copie de la ficha 04 el alcance, las herramientas, las restricciones, el escalamiento y las métricas: las instrucciones deben coincidir con la ficha.
2. Escriba el contexto organizacional como si se lo explicara a alguien que no sabe nada de la empresa: el agente no infiere el contexto que no se le da (sección 2.4).
3. Escriba el objetivo en una sola oración, medida en términos de negocio.
4. Escriba el SOP como pasos numerados. En cada paso indique qué hacer, qué herramienta usar y qué criterio aplica para decidir.
5. Elimine toda palabra ambigua ("flexibilidad", "cuando sea apropiado", "según perciba"). Si la necesita, conviértala en criterios explícitos (pregunta 7 del Módulo 2).
6. Haga la prueba del colega: ¿un colega podría seguir estas instrucciones sin pedir aclaraciones? Si no, siga precisando (responsabilidad 2 del Módulo 2).

## Plantilla

**Agente:** `[nombre, igual que en la ficha 04]`  **Versión:** `[n.º]`  **Fecha:** `[AAAA-MM-DD]` (versión y fecha no vienen en el curso; sirven para saber qué instrucciones estaban vigentes)

### Parte JD: el "qué" y el "para qué"

**1. Contexto organizacional:** `[empresa, área, proceso y audiencia con la que interactúa el agente]`

**2. Objetivo principal:** `[una oración: qué debe lograr el agente, medido en términos de negocio]`

### Parte SOP: el "cómo"

**3. Proceso paso a paso:**

| Paso | Qué hacer | Herramienta que usa | Criterio de decisión en este paso |
|---|---|---|---|
| 1 | `[…]` | `[…]` | `[…]` |
| 2 | `[…]` | `[…]` | `[…]` |
| 3 | `[…]` | `[…]` | `[…]` |

**4. Herramientas y accesos disponibles:** `[cada API (conexión con otro sistema), base de datos o sistema, con su propósito]` (deben ser los mismos permisos de la ficha 04, ni uno más)

**5. Restricciones operacionales (lo que NO debe hacer):** `[lista explícita]`

**6. Protocolos de escalamiento:** `[condiciones específicas para transferir a un humano, y qué contexto completo se le entrega]`

**7. Métricas de éxito:** `[indicadores de negocio con su meta]`

### Revisión de calidad de las instrucciones

- [ ] Tiene los siete componentes: contexto, objetivo, SOP, herramientas, restricciones, escalamiento y métricas (sección 2.5).
- [ ] Cada paso del SOP dice qué hacer, con qué herramienta y con qué criterio.
- [ ] El escalamiento está definido como criterios de negocio, no "a juicio del agente" (pregunta 3 del Módulo 2).
- [ ] Toda "flexibilidad" está definida: qué señales activan qué adaptación, dentro de qué parámetros y qué situaciones van siempre a un humano (pregunta 7 del Módulo 2).
- [ ] Los criterios de éxito son explícitos, medibles y sin ambigüedad: el agente no interpreta intenciones, solo métricas definidas (sección 2.4).
- [ ] Prueba del colega: un colega podría seguirlas sin requerir aclaración adicional (responsabilidad 2 del Módulo 2).
- [ ] Coinciden con la ficha de identidad (plantilla 04).

**Validado por (AI Agent Manager) y fecha:** `[nombre, AAAA-MM-DD]`

## Ejemplo lleno

Agente de soporte B2B (empresa que vende a otras empresas) de la sección 2.5. Los componentes 1, 2, 4, 5, 6 y 7 son los ejemplos textuales del curso. El curso no trae los pasos del SOP: los del componente 3 son datos ficticios de ejemplo, armados solo con las herramientas, restricciones y escalamientos del propio curso.

**Agente:** Agente de Soporte N1. **Versión:** 1. **Fecha:** 2026-09-01.

**1. Contexto organizacional:** "Operas en el área de Customer Success (éxito del cliente) de una empresa de software B2B. Interactúas con clientes existentes que reportan problemas técnicos a través del portal de soporte."

**2. Objetivo principal:** "Tu objetivo es resolver el 80% de los tickets (solicitudes) de soporte de nivel 1 sin intervención humana, en un tiempo promedio inferior a 3 minutos."

**3. Proceso paso a paso (ficticio):**

| Paso | Qué hacer | Herramienta | Criterio de decisión |
|---|---|---|---|
| 1 | Leer el ticket e identificar al cliente | Portal de soporte | Si el cliente menciona cancelación, ir al escalamiento |
| 2 | Revisar el historial del cliente | CRM (sistema de gestión de clientes) | Usar el historial solo de ese cliente; nunca mostrar datos de otros |
| 3 | Buscar la solución | Base de conocimiento | Si no hay resolución documentada, ir al escalamiento |
| 4 | Responder al cliente con la solución documentada | Portal de soporte | Si la solución exige cambiar la cuenta, pedir confirmación humana |
| 5 | Confirmar el cierre o escalar | Portal de soporte | Si el tiempo de resolución supera 8 minutos, ir al escalamiento |

**4. Herramientas y accesos:** "CRM: para consultar historial del cliente. Base de conocimiento: para buscar soluciones documentadas."

**5. Restricciones:** "No realizar cambios en la cuenta del cliente sin confirmación humana. No compartir información de otros clientes. No ofrecer descuentos no autorizados."

**6. Escalamiento:** escalar a un humano, con contexto completo, si primero, el ticket no tiene resolución documentada; segundo, el cliente menciona cancelación; o tercero, el tiempo de resolución supera 8 minutos.

**7. Métricas:** tasa de resolución autónoma mayor o igual al 80%; CSAT (satisfacción del cliente) mayor o igual a 4,2 sobre 5; tasa de escalamiento menor o igual al 20%; tiempo promedio de resolución menor o igual a 3 minutos.

**Revisión (ficticia):** las siete casillas marcadas. Prueba del colega: una ejecutiva de soporte recién llegada siguió los cinco pasos sin preguntar nada.

## Errores comunes

- **Instrucciones conversacionales e informales.** Comunicarse con el agente evitando instrucciones formales contradice el principio de instrucciones explícitas y estructuradas (pregunta 8 del Módulo 2).
- **Omitir el escalamiento "para simplificar".** Cuándo interviene un humano es una decisión de gobierno del manager, que debe quedar definida antes de producción y no delegarse al agente (pregunta 3 del Módulo 2).
- **Dejar "flexibilidad" sin parámetros.** La flexibilidad sin parámetros es ambigüedad, y la ambigüedad produce resultados impredecibles (pregunta 7 del Módulo 2; sección 2.4).
- **Esperar que el agente aprenda solo de sus errores.** El agente aprende solo dentro de su ciclo de actualización: lo que no se corrige en las instrucciones se repite (sección 2.4).
- **Escribir solo el JD o solo el SOP.** Ninguno de los dos basta por sí solo (sección 2.5).
