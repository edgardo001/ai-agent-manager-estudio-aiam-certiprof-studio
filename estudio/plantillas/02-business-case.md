# 02 · Business Case AIAM™ (caso de negocio)

> **Para qué sirve:** presentar a la dirección, en cinco elementos, qué problema resuelve el agente, cuánto cuesta, cuánto vale y cuál es el riesgo de no actuar, y terminar con una decisión concreta que la dirección debe tomar.
> **Cuándo llenarla:** el baseline (línea base, el punto de partida medido) se llena **antes de activar el primer agente**; el resto, antes de pedir la aprobación del piloto. Después se actualiza y se presenta **trimestralmente** a la dirección.
> **Quién la llena y quién la aprueba:** la llena el AI Agent Manager (AIAM™, el gerente de agentes de IA); la decide la dirección o el comité directivo; la Junta de Gobierno Agentic (Governance Board) revisa el portafolio y las métricas de ROI (retorno sobre la inversión).
> **Con qué se llena:** métricas actuales del proceso (tiempo, costo, calidad, capacidad), presupuesto de plataforma e implementación, horas del equipo, KPI (indicadores clave de desempeño) definidos para el agente, matriz de riesgos y controles.
> **Base en el curso:** Módulo 5, secciones 5.1, 5.2 y 5.3; responsabilidades 1 y 2 del Módulo 5; sección 3.7 (línea base y AI Productivity Paradox).
> **Se conecta con:** se alimenta de 01 · Oportunidades y taxonomía (01-oportunidades-y-taxonomia.md), 07 · Rediseño de proceso y piloto (07-rediseno-de-proceso-y-piloto.md, el AS-IS da el baseline), 09 · Plan de supervisión (09-plan-de-supervision.md, los KPI) y 11 · Matriz de riesgos y seguridad (11-matriz-de-riesgos-y-seguridad.md). Alimenta a 14 · Reporte a la dirección (14-reporte-a-la-direccion.md), 15 · Evaluación de escala y madurez (15-evaluacion-de-escala-y-madurez.md) y 12 · Governance Board (12-governance-board.md).

## Cómo llenarla

1. Mida el **baseline** del proceso sin agente (tiempo, costo, calidad y capacidad) y anote la fecha y las condiciones de volumen y complejidad. Sin baseline, cualquier mejora posterior es anecdótica (5.3).
2. Sume la **inversión total**, incluidos los costos ocultos: tiempo del equipo en el piloto, errores del agente durante la curva de aprendizaje y ajustes de proceso (5.3).
3. Defina los **retornos en los tres horizontes** (H1, H2 y H3), aunque H2 y H3 todavía sean proyecciones (5.2).
4. Exprese cada retorno **primero** en unidades que la dirección entiende (tiempo, dinero, clientes) y **después** en proyección financiera. Nunca al revés (5.3).
5. Liste los **riesgos** con probabilidad, impacto y control activo (5.3).
6. Cierre con la **próxima fase**: una recomendación y la decisión que se pide, con criterios explícitos (5.3).
7. Revise la lista de verificación final y prográmela para la presentación trimestral (responsabilidad 2 del Módulo 5).

## Plantilla

**Agente o proceso:** `[escriba aquí el nombre del agente y el proceso que cubre]`
**AI Agent Manager responsable:** `[nombre]` · **Agent Owner (dueño del agente):** `[nombre]`
**Fecha de esta versión:** `[AAAA-MM-DD]` · **Versión:** `[1, 2, 3…]`
**Problema de negocio que resuelve (una oración):** `[qué problema resuelve, no cómo funciona el agente]`

### Elemento 1. Baseline (estado actual sin agentes)

| Dimensión | Métrica | Valor actual | Qué escribir |
|---|---|---|---|
| Tiempo | `[…]` | `[…]` | Tiempo de ciclo o de resolución por caso. |
| Costo | `[…]` | `[…]` | Costo por transacción o por caso. |
| Calidad | `[…]` | `[…]` | Tasa de error, CSAT (satisfacción del cliente) u otra medida de calidad. |
| Capacidad | `[…]` | `[…]` | Volumen procesado por período y personas que lo procesan. |

**Fecha y período de medición:** `[AAAA-MM-DD; semanas o meses medidos]`
**Condiciones de volumen y complejidad:** `[para comparar después en las mismas condiciones (5.2)]`

### Elemento 2. Inversión (costo total, honesto)

| Partida | Monto o esfuerzo | Qué escribir |
|---|---|---|
| Plataforma tecnológica | `[…]` | Licencias, infraestructura. |
| Tiempo de implementación | `[…]` | Horas o costo de configurar e integrar. |
| Formación del equipo | `[…]` | Capacitación en los niveles de adopción (4.4). |
| Rediseño de procesos | `[…]` | Trabajo del AS-IS (proceso actual) al TO-BE (proceso futuro) (4.3). |
| Mantenimiento continuo | `[…]` | Supervisión, ajustes de instrucciones, auditorías. |
| Oculto: tiempo del equipo en el piloto | `[…]` | Horas de personas desviadas al piloto. |
| Oculto: errores durante la curva de aprendizaje | `[…]` | Costo estimado de corregir errores del agente. |
| Oculto: ajustes de proceso | `[…]` | Cambios no previstos en el flujo. |
| **Total** | `[…]` | |

### Elemento 3. Retornos en tres horizontes

| Horizonte | Ventana | Métricas (ejemplos del curso) | Valor medido o proyectado | Narrativa para la dirección |
|---|---|---|---|---|
| H1 · Eficiencia operacional | 0 a 6 meses | Tiempo de ciclo, costo por transacción, volumen procesado, tasa de error, horas humanas liberadas | `[…]` (`[medido / proyección]`) | "Hacemos lo mismo mejor, más rápido y más barato." |
| H2 · Calidad y capacidad | 6 a 18 meses | NPS (índice de recomendación del cliente), escalaciones reducidas, volumen adicional sin aumentar el headcount (dotación de personal), satisfacción del equipo | `[…]` | "Hacemos más y mejor sin crecer en estructura." |
| H3 · Transformación estratégica | Más de 18 meses | Nuevos servicios habilitados, market share (participación de mercado), time-to-market (tiempo de llegada al mercado), retención de talento, ventaja competitiva | `[…]` | "Hacemos cosas que antes eran imposibles a este costo y velocidad." |

**Cómo se calcula cada horizonte (5.2):** H1, baseline pre-agente frente a post-agente en las mismas condiciones; H2, encuestas periódicas, dashboards (tableros) operativos y comparativa de headcount frente a output (resultado producido); H3, análisis de negocio comparativo, benchmarks (comparaciones de referencia) de industria y proyecciones con y sin modelo agentic.

**Tipo de valor que el ROI clásico no captura (5.1):** el ROI clásico es el beneficio menos la inversión, dividido por la inversión.
- Valor diferido (ahorros que llegan meses después del piloto): `[…]`
- Valor habilitado (capacidades nuevas que antes no existían): `[…]`
- Valor de opción (poder escalar sin aumento proporcional de costos): `[…]`

**Retorno en unidades directivas (tiempo, dinero, clientes):** `[escriba aquí, antes de la cifra financiera]`
**Proyección financiera:** `[escriba aquí, después]`

### Elemento 4. Riesgos

| Riesgo | Probabilidad | Impacto estimado | Control activo del AIAM™ |
|---|---|---|---|
| `[…]` | `[alta / media / baja]` | `[…]` | `[circuit breaker (corte automático), supervisión humana, dashboard, Junta de Gobierno…]` |

### Elemento 5. Próxima fase

**Recomendación:** `[ ] escalar el piloto  [ ] expandir a otro proceso  [ ] invertir en plataforma  [ ] pausar para consolidar`
**Decisión que se pide a la dirección:** `[una pregunta concreta, de sí o no]`
**Criterios explícitos para decidir:** `[qué umbrales o condiciones justifican cada opción]`

### Verificación antes de presentar

- [ ] El baseline está documentado con fecha y fue medido antes de activar el agente.
- [ ] La inversión incluye los tres costos ocultos.
- [ ] Están los tres horizontes, aunque H2 y H3 sean proyecciones marcadas como tales.
- [ ] Los retornos aparecen primero en tiempo, dinero o clientes, y después en cifras financieras.
- [ ] Cada riesgo tiene probabilidad, impacto y control.
- [ ] Termina con una decisión, no con un resumen.

## Ejemplo lleno

Agente de soporte B2B (de empresa a empresa) de la sección 2.5. **El baseline, la inversión, las proyecciones de H2 y H3, el riesgo y el criterio de escala son datos ficticios de ejemplo**; los objetivos y métricas de éxito del agente salen del curso (2.5).

- **Problema de negocio:** los tickets de soporte de nivel 1 consumen al equipo de Customer Success (éxito del cliente) y alargan la espera del cliente.
- **Baseline (ficticio):** 12 minutos promedio por ticket de nivel 1; 9 dólares por ticket; CSAT de 3,9 sobre 5; 6 personas atienden 4.000 tickets al mes. Medido de 2026-01-05 a 2026-02-28, sin campañas especiales.
- **Inversión (ficticia):** plataforma, implementación, formación, rediseño y mantenimiento por 60.000 dólares el primer año, más costos ocultos estimados en 15.000 dólares (horas del equipo en el piloto, corrección de errores del agente, ajustes del flujo).
- **Retornos:** H1, meta del curso de resolver el 80% de los tickets de nivel 1 sin intervención humana en menos de 3 minutos, con CSAT mayor o igual a 4,2 sobre 5 y escalamiento menor o igual al 20% (2.5). H2 (proyección): atender más clientes sin contratar. H3 (proyección): ofrecer soporte de nivel 1 las 24 horas a nuevos segmentos. En unidades directivas: "4 de cada 5 consultas se resolverán sin esperar a una persona".
- **Riesgos (ficticio):** el agente ofrece descuentos no autorizados (probabilidad baja, impacto medio; control: restricción explícita en las instrucciones y muestreo semanal de outputs).
- **Próxima fase:** se pide aprobar un piloto de 3 meses; criterio para escalar: cumplir las cuatro métricas de éxito de la 2.5 durante 4 semanas seguidas.

Referencia real del curso: UPS ORION presentó su business case en los tres horizontes: H1, reducción de costo por milla; H2, reducción de emisiones de CO₂ como ventaja regulatoria y reputacional; H3, capacidad de absorber un 15% más de volumen sin aumentar la flota (5.5).

## Errores comunes

1. **Presentar solo el Horizonte 1** en los primeros seis meses: la dirección queda con la idea de que el agente es solo para reducir costos y asigna presupuesto de "eficiencia", no de "transformación" (5.2; pregunta 1 del Módulo 5).
2. **No tener baseline** o construirlo después de activar el agente: la mejora queda anecdótica y no defendible (5.3; pregunta 10 del Módulo 5; 3.7).
3. **Ocultar costos**: omitir el tiempo del equipo en el piloto, los errores de la curva de aprendizaje o los ajustes de proceso (5.3).
4. **Omitir el análisis de riesgos**: el business case pierde credibilidad ante cualquier comité experimentado (5.3; pregunta 5 del Módulo 5).
5. **Medir solo eficiencia**: según BCG (2025) se captura menos del 30% del valor real; y Gartner proyecta que más del 40% de los proyectos de IA agentica serán cancelados antes de 2027 por no articular su valor (5.1).
