# 12 · Governance Board

> **Para qué sirve:** constituir y operar el Governance Board Agentic (comité interfuncional de gobierno de agentes), que establece estándares, revisa el portafolio de agentes activos, responde por incidentes de impacto organizacional y evalúa si los agentes generan el valor prometido (sección 3.6). Incluye el acta de cada sesión.
> **Cuándo llenarla:** la parte A, una vez, al crear el Board, idealmente antes de escalar, porque la gobernanza no puede crearse después de la escala (sección 5.5). Las partes B a E, en cada sesión: quincenal o mensual según la madurez de la organización, y de forma extraordinaria ante incidentes de impacto.
> **Quién la llena y quién la aprueba:** la prepara el AI Agent Manager (gestor de agentes de IA) que actúa como secretario de la sesión (no viene en el curso); cada AI Agent Manager aporta el estado de su portafolio. Aprueba el Board, con su patrocinador del C-suite (alta dirección).
> **Con qué se llena:** el registro de agentes (plantilla 03), los dashboards (tableros) de supervisión (plantilla 09), el registro de intervenciones (plantilla 10), las matrices de riesgos (plantilla 11), las solicitudes de nuevos despliegues (plantillas 04 a 06), la auditoría trimestral (plantilla 13) y los business cases (plantilla 02).
> **Base en el curso:** Módulo 3, sección 3.6, responsabilidad 5 y preguntas 4 y 9; Módulo 5, sección 5.5 (Junta de Gobierno Agentic, condición 1 y modelo de madurez) y responsabilidad 4.
> **Se conecta con:** se alimenta de 03 · Registro de agentes, 09 · Plan de supervisión, 10 · Registro de intervenciones, 11 · Matriz de riesgos y seguridad y 13 · Auditoría trimestral del portafolio; alimenta a 03 · Registro de agentes (actualizado), 14 · Reporte a la dirección y 15 · Evaluación de escala y madurez.

Nota: la sección 3.6 lo llama Governance Board Agentic y la 5.5, Junta de Gobierno Agentic. Aquí se tratan como la misma instancia (interpretación; el curso no lo dice de forma explícita).

## Cómo llenarla

1. Constituya el Board con los cinco integrantes recomendados y fije la frecuencia (parte A).
2. Antes de cada sesión, pida a cada AI Agent Manager el estado de su portafolio en el formato de la parte B.
3. En la sesión, siga la agenda de cuatro puntos: portafolio, nuevos despliegues de alto riesgo, incidentes y estándares (parte C).
4. Para cada decisión, anote qué tensión estratégica se estaba equilibrando (parte D).
5. Cierre con los cuatro outputs (resultados) esperados y actualice el registro de agentes (parte E).

## Plantilla

### A. Constitución del Board

| Integrante recomendado (sección 3.6) | Nombre y cargo |
|---|---|
| AI Agent Managers de áreas clave | `[ ]` |
| Representante de IT (sistemas) y Seguridad | `[ ]` |
| Representante de Legal y Riesgo | `[ ]` |
| Representante de RRHH (recursos humanos) y Talento | `[ ]` |
| Patrocinador del C-suite | `[ ]` |

**Frecuencia:** `[quincenal o mensual]` · **Cuándo hay sesión extraordinaria:** `[incidentes de impacto; defina cuáles]`
**Roles definidos en la organización (sección 5.5):** Agent Owners (responsables directos de agentes) `[ ]`, Ethics Reviewers (revisores éticos) `[ ]`, AI Agent Managers `[ ]`.
**Criterios de escala explícitos:** `[cuándo un piloto puede pasar a escala; ver plantilla 15]`
**Alcance:** dual: seguridad e infraestructura, y sobre todo gobierno del valor de negocio (pregunta 4 del Módulo 3).

### B. Estado del portafolio (uno por AI Agent Manager, formato de la pregunta 9 del Módulo 3)

| Agente | Semáforo (verde, amarillo o rojo) | Resolución | Costo por caso | CSAT (satisfacción del cliente) | ROI acumulado (retorno de la inversión) | ¿Muestreo al día? | ¿Umbrales definidos? | ¿Owner documentado? | Acción pendiente (si está en amarillo o rojo) |
|---|---|---|---|---|---|---|---|---|---|
| `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[sí/no]` | `[sí/no]` | `[sí/no]` | `[ ]` |

### C. Agenda de la sesión

**Sesión N.º:** `[ ]` · **Fecha:** `[AAAA-MM-DD]` · **Tipo:** `[ordinaria / extraordinaria]` · **Asistentes:** `[ ]`

1. **Revisión del portafolio de agentes activos:** `[agentes en amarillo o rojo y decisiones]`
2. **Aprobación de nuevos despliegues de alto riesgo.** Por cada solicitud, verifique:
   - [ ] Ficha de identidad con los seis parámetros (plantilla 04).
   - [ ] Permisos mínimos justificados (plantilla 11, sección B).
   - [ ] Las cinco dimensiones de validación aprobadas: funcional, límites, adversarial, escalamiento y métricas de negocio (plantilla 06).
   - [ ] Métricas de negocio, baseline (línea base) y umbrales definidos antes del despliegue (plantilla 09).
   - [ ] AI Agent Manager y Agent Owner designados (plantilla 03).
   - Decisión: `[aprobado / aprobado con condiciones / rechazado]` y motivo.
3. **Análisis de incidentes:** `[entradas de la plantilla 10 escaladas al Board, causa y decisión]`
4. **Actualización de estándares de gobernanza:** `[estándar nuevo o modificado]`

**Decisiones escaladas por AI Agent Managers que superan su autoridad:** `[ ]`

### D. Tensiones estratégicas (MIT SMR y BCG, 2025)

Marque qué tensión equilibra cada decisión; sin una instancia que las gestione, la organización las resuelve de forma improvisada y contradictoria (sección 3.6).

| Tensión | Decisión de esta sesión que la toca | Cómo se equilibró |
|---|---|---|
| Velocidad de adopción frente a seguridad de gobernanza | `[ ]` | `[ ]` |
| Autonomía del agente frente a control del manager | `[ ]` | `[ ]` |
| Eficiencia operacional frente a accountability (responder por los resultados) ética | `[ ]` | `[ ]` |
| Innovación experimental frente a estabilidad operacional | `[ ]` | `[ ]` |

### E. Outputs de la sesión (sección 3.6)

- [ ] Registro centralizado de agentes actualizado (plantilla 03).
- [ ] Decisiones de intervención documentadas (plantilla 10).
- [ ] Métricas de ROI del portafolio (insumo de la plantilla 14).
- [ ] Recomendaciones de política organizacional: `[ ]`
- **Pendientes, responsables y fechas:** `[ ]`

## Ejemplo lleno

Datos ficticios de ejemplo. La empresa es la de software B2B (que vende a otras empresas) de la plantilla 03; el agente de soporte es el de la sección 2.5.

**Constitución:** Ana Rojas (AI Agent Manager, Customer Success, es decir, éxito del cliente), Pedro Soto (AI Agent Manager, Finanzas), jefe de Seguridad de IT, abogada de Legal y Riesgo, jefa de Talento, y el gerente de Operaciones como patrocinador. Frecuencia mensual, porque la organización está en el Nivel 1 de madurez, Exploración, y su palanca de avance es justamente establecer la Junta (sección 5.5).

**Sesión 1 · 2026-11-17 · ordinaria.**

| Agente | Semáforo | Resolución | CSAT | ¿Muestreo? | ¿Umbrales? | ¿Owner? | Acción pendiente |
|---|---|---|---|---|---|---|---|
| Agente de Soporte N1 | Amarillo | 82% | 4,3 | Sí | Sí | Sí | Escalamiento en 26% por 4 días; muestreo en curso (plantilla 10, entrada 4) |
| Agente de Cobranza Preventiva | Rojo | Sin dato | Sin dato | No | No | No | En producción sin validar |
| Asistente de Propuestas | Amarillo | Sin dato (Nivel 1: el vendedor decide) | Sin dato | No | No | Sí | Definir métricas de negocio y su muestreo |

**Decisiones:** (1) el Agente de Cobranza Preventiva pasa a validación pre-producción en 30 días, con Pedro Soto como AI Agent Manager; tensión velocidad frente a seguridad, resuelta a favor de la seguridad. (2) Se rechaza un nuevo agente de Ventas que pedía escritura en el CRM (sistema de gestión de clientes) sin pruebas adversariales. (3) Estándar nuevo: ningún agente opera sin AI Agent Manager ni Agent Owner registrados.
**Outputs:** registro actualizado; 2 decisiones de intervención documentadas; recomendación de política: validación obligatoria para todo agente nuevo.

## Errores comunes

- **Reducir el Board a un comité técnico.** Su alcance es dual, y su función central es el gobierno del valor de negocio (pregunta 4 del Módulo 3).
- **Presentar al Board reportes técnicos o anecdóticos.** Necesita semáforo, métricas primarias de negocio, ROI, estado de gobernanza y acciones pendientes (pregunta 9 del Módulo 3).
- **Crear la gobernanza después de escalar.** Debe precederla (sección 5.5, condición 1).
- **Resolver cada tensión caso a caso.** Genera inconsistencias que se convierten en riesgo acumulado (sección 3.6).
- **Posponer la definición del alcance del Board.** El curso indica que es crítica y no conviene postergarla (pregunta 4 del Módulo 3).
