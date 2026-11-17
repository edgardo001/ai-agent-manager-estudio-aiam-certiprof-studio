# 13 · Auditoría trimestral del portafolio

> **Para qué sirve:** revisar cada trimestre todos los agentes del portafolio con las tres preguntas del curso: ¿siguen generando valor medible?, ¿tienen dueño claro?, ¿han derivado de su función original? Es el tercer mecanismo contra el agent sprawl (crecimiento desordenado de agentes sin dueño, sin propósito y sin métricas) y es business governance (gobierno de negocio), no IT governance (gobierno de sistemas) (sección 2.7).
> **Cuándo llenarla:** una vez por trimestre, antes de la sesión del Governance Board (comité de gobierno de agentes) y del reporte trimestral a la dirección. En la misma revisión se ajusta la taxonomía de tareas (sección 4.2).
> **Quién la llena y quién la aprueba:** la lidera el AI Agent Manager (gestor de agentes de IA); cada Agent Owner (responsable directo del agente) aporta los datos de sus agentes y el Quality Reviewer (revisor de calidad) aporta las muestras. Los resultados se presentan al Governance Board.
> **Con qué se llena:** el registro de agentes (plantilla 03), los dashboards (tableros) y baselines (líneas base) de la plantilla 09, el registro de intervenciones (plantilla 10), las matrices de riesgos (plantilla 11), las instrucciones originales de cada agente (plantilla 05), muestras de logs (registros de actividad) y la taxonomía de tareas (plantilla 01).
> **Base en el curso:** Módulo 2, sección 2.7 (auditoría periódica), responsabilidades 3 y 5, preguntas 5 y 9; Módulo 3, sección 3.3 (behavioral drift); Módulo 4, secciones 4.2 y 4.3 (paso 5: revisión trimestral).
> **Se conecta con:** se alimenta de 01 · Oportunidades y taxonomía, 03 · Registro de agentes, 05 · Instrucciones del agente, 09 · Plan de supervisión, 10 · Registro de intervenciones y 11 · Matriz de riesgos y seguridad; alimenta a 03 · Registro de agentes, 12 · Governance Board, 14 · Reporte a la dirección y 15 · Evaluación de escala y madurez.

## Cómo llenarla

1. Confirme que el registro de agentes está completo: pregunte en cada área si hay agentes o pilotos que no figuran (los pilotos que pasan a producción sin proceso formal son una fuente de agent sprawl; sección 2.7).
2. Para cada agente, responda las tres preguntas con evidencia, no con opiniones.
3. Revise permisos, fecha de última validación y estado de la supervisión de cada agente.
4. Busque redundancias: agentes que hacen versiones ligeramente distintas de lo mismo.
5. Revise la taxonomía de tareas, los criterios de handoff (traspaso de trabajo entre agente y humano) y los umbrales de intervención (sección 4.3, paso 5).
6. Decida una acción por agente, priorice y lleve el resultado al Governance Board.

## Plantilla

### A. Datos de la auditoría

**Trimestre:** `[ej.: T4 2026]` · **Fecha:** `[AAAA-MM-DD]` · **AI Agent Manager:** `[ ]`
**Agentes en el registro:** `[número]` · **Agentes encontrados fuera del registro:** `[número y cuáles]`

### B. Las tres preguntas por agente (sección 2.7)

| Agente | 1. ¿Genera valor medible? | 2. ¿Tiene dueño claro? | 3. ¿Derivó de su función original? |
|---|---|---|---|
| `[ ]` | `[métrica de negocio actual frente a baseline y meta]` | `[AI Agent Manager y Agent Owner designados, sí o no]` | `[ver sección C]` |

Guía de "¿derivó?": hay dos formas de deriva en el curso. La behavioral drift (deriva de comportamiento): el agente se desplaza poco a poco de sus instrucciones; se detecta con la tendencia de calidad y comparando muestras actuales con el baseline de los primeros 30 días (sección 3.3). El scope drift (expansión de alcance no autorizada): el agente empieza a hacer funciones que no estaban en sus instrucciones (pregunta 9 del Módulo 2).

### C. Revisión de gobierno por agente

| Agente | Fecha de última validación | ¿Permisos siguen siendo los mínimos? | ¿Muestreo al día? | ¿Umbrales definidos? | ¿Intervenciones abiertas? | Comparación con los primeros 30 días | ¿Funciones fuera de las instrucciones? |
|---|---|---|---|---|---|---|---|
| `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |

### D. Redundancias y fragmentación

- [ ] ¿Hay agentes que hacen versiones ligeramente distintas de lo mismo? `[cuáles]`
- [ ] ¿La inversión total en agentes supera el valor generado? `[dato]`
- [ ] ¿Hay agentes sin dueño, sin propósito documentado o sin métricas? `[cuáles]`

### E. Revisión trimestral de la taxonomía (secciones 4.2 y 4.3)

| Tarea o proceso | Clasificación actual (agente, humano o colaboración) | ¿Cambió? (más datos, agente más maduro o nuevas condiciones del negocio) | Ajuste a criterios de handoff o umbrales |
|---|---|---|---|
| `[ ]` | `[ ]` | `[ ]` | `[ ]` |

### F. Decisión por agente

| Agente | Decisión | Responsable | Fecha |
|---|---|---|---|
| `[ ]` | `[mantener / corregir instrucciones / formalizar o restringir alcance / reducir permisos / revalidar / designar dueño / consolidar con otro agente / retirar]` | `[ ]` | `[ ]` |

"Consolidar" y "retirar" son decisiones prácticas que el curso no enumera; las mencionamos porque el Agent Owner gestiona el ciclo de vida del agente (sección 4.5) (no viene en el curso).

**Prioridad:** primero los agentes en producción sin validación, porque son el mayor riesgo activo (pregunta 5 del Módulo 2); luego los que no tienen dueño; luego los que derivaron.

### G. Resumen para el Governance Board y la dirección

**Agentes que generan valor medible:** `[n de N]` · **Sin dueño:** `[ ]` · **Con deriva:** `[ ]` · **Decisiones que requieren al Board:** `[ ]`

## Ejemplo lleno

Datos ficticios de ejemplo, T4 2026, en la empresa de software B2B (que vende a otras empresas) de la plantilla 03. El caso del agente de onboarding (incorporación) de empleados viene de la pregunta 9 del Módulo 2; el agente de soporte es el de la sección 2.5.

**Agentes en el registro:** 3. **Encontrados fuera del registro:** 1 (agente de onboarding de empleados, configurado hace 6 meses por RRHH, recursos humanos).

| Agente | ¿Valor medible? | ¿Dueño claro? | ¿Derivó? | Decisión |
|---|---|---|---|---|
| Agente de Soporte N1 | Sí: 82% de resolución autónoma frente a 0% de baseline; CSAT (satisfacción del cliente) 4,3 sobre 5 | Sí: Ana Rojas y Luis Pérez | Sin scope drift; el tono comparado con los primeros 30 días se mantiene | Mantener; cerrar la intervención 4 abierta |
| Agente de Cobranza Preventiva | No se sabe: sin métricas | Sí desde la sesión 1 del Board: Pedro Soto | No se puede evaluar sin baseline | Revalidar (en curso, 30 días) |
| Asistente de Propuestas | No: sin métricas de negocio | Sí: Ana Rojas y Marta Díaz | No | Definir métricas antes del próximo trimestre |
| Agente de onboarding de empleados | Sin métricas | No: nadie registrado | Sí, scope drift: en los últimos dos meses responde sobre beneficios de compensación y negociación salarial, fuera de sus instrucciones | Restringir esas consultas, revisar permisos de acceso a datos de compensación, designar dueño e inscribirlo en el registro |

**Redundancia:** Ventas y Customer Success (éxito del cliente) evalúan cada uno un agente para responder consultas de clientes; se recomienda al Board una sola solución.
**Taxonomía:** las preguntas de facturación pasan de "humano lidera" a "agente como primera capa", porque ya hay respuestas documentadas en la base de conocimiento.

## Errores comunes

- **Tratar la auditoría como un trámite de IT.** Es gobierno de negocio aplicado a sistemas autónomos (sección 2.7).
- **Dar por buena la ausencia de quejas.** No equivale a respuestas correctas ni a permisos adecuados; dejar que siga es aceptar un riesgo no gestionado (pregunta 9 del Módulo 2).
- **Creer que el agente "aprendió" funciones nuevas.** El agente no aprende de forma autónoma así: es una expansión de alcance que se formaliza o se restringe (pregunta 9 del Módulo 2).
- **Revisar solo los agentes registrados.** Los pilotos que pasaron a producción sin proceso formal originan el agent sprawl (sección 2.7).
- **Congelar la taxonomía.** Lo que hoy necesita supervisión humana intensa puede ser territorio del agente en seis meses, y viceversa (sección 4.2).
