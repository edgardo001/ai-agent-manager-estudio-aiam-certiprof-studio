# 14 · Reporte a la dirección

> **Para qué sirve:** traducir la operación de los agentes al lenguaje de la dirección (dinero, tiempo del cliente, participación de mercado, riesgo regulatorio), para que el valor sea comprensible y defendible y la dirección pueda decidir. Es la sexta competencia del rol: traducir el desempeño técnico del agente a lenguaje de P&L (estado de resultados: ingresos, costos y utilidad) y articular su impacto ante los stakeholders (partes interesadas) del negocio (1.3).
> **Cuándo llenarla:** **mensual** mientras el proyecto está en piloto; **trimestral** cuando la operación es estable; **puntual** ante una incidencia significativa o un hito de escala (5.4). No se llena a diario: los tableros técnicos en tiempo real son para uso propio del AIAM™.
> **Quién la llena y quién la aprueba:** la llena el AI Agent Manager (AIAM™, el gerente de agentes de IA); la recibe el comité directivo o el C-suite (la alta dirección: gerente general, finanzas, operaciones…); el Governance Board (junta de gobierno de agentes) recibe la misma información de portafolio.
> **Con qué se llena:** el dashboard (tablero) de supervisión de la sección 3.5, sobre todo el estado del portafolio y el ROI (retorno sobre la inversión) acumulado; el Business Case actualizado; el registro de intervenciones; la matriz de riesgos; los indicadores del equipo humano.
> **Base en el curso:** Módulo 5, sección 5.4 (tres principios, traducción técnico → directivo, cadencia); 5.2 (tres horizontes); 3.5 (dashboard ejecutivo); Módulo 1, sección 1.3, competencia 6 (comunicación organizacional); 4.6 y pregunta 10 del Módulo 4 (reporte en tres capas).
> **Se conecta con:** se alimenta de 02 · Business case (02-business-case.md), 09 · Plan de supervisión (09-plan-de-supervision.md), 10 · Registro de intervenciones (10-registro-de-intervenciones.md), 11 · Matriz de riesgos y seguridad (11-matriz-de-riesgos-y-seguridad.md) y 08 · Gestión del cambio y roles (08-gestion-del-cambio-y-roles.md). Alimenta a 12 · Governance Board (12-governance-board.md) y a 15 · Evaluación de escala y madurez (15-evaluacion-de-escala-y-madurez.md).

## Cómo llenarla

1. Elija el **tipo de reporte** según la cadencia: mensual (piloto), trimestral (operación estable) o puntual (incidencia o hito).
2. Abra con el **problema de negocio**, no con la solución técnica (primer principio, 5.4).
3. Tome los datos del dashboard (3.5) y **tradúzcalos**: cada métrica técnica pasa a una unidad directiva (segundo principio).
4. Ordene el valor en los **tres horizontes**, marcando lo que es dato medido y lo que es proyección (5.2).
5. Muestre las **tres capas**: equipo humano, sistema híbrido y negocio (4.6).
6. **Anticipe la pregunta de riesgo**: qué pasa si falla, qué controles hay y quién es responsable (tercer principio).
7. Cierre con la **decisión o el próximo paso** que necesita de la dirección (5.3, quinto elemento del business case).

## Plantilla

**Tipo de reporte:** `[ ] mensual (piloto)  [ ] trimestral (operación estable)  [ ] puntual (incidencia o hito de escala)`
**Período:** `[AAAA-MM-DD a AAAA-MM-DD]` · **Destinatario:** `[comité, persona]` · **Responsable:** `[AIAM™]`

### 1. Problema de negocio y mensaje principal

**Problema de negocio que atendemos:** `[en una oración, en términos de clientes, dinero o tiempo]`
**Mensaje principal del período:** `[una o dos oraciones que la dirección debe recordar]`

### 2. Estado del portafolio (semáforo)

| Agente | Estado | Comentario en lenguaje directivo |
|---|---|---|
| `[…]` | `[verde / amarillo / rojo]` | `[dentro de parámetros, requiere atención o alerta activa (3.5, panel 1)]` |

### 3. Traducción de métricas técnicas a lenguaje directivo

| Métrica técnica (del dashboard) | Valor | Traducción directiva | Unidad directiva |
|---|---|---|---|
| `[tasa de resolución autónoma, tiempo de respuesta, costo por caso…]` | `[…]` | `[qué significa para clientes, equipo o dinero]` | `[dinero / tiempo del cliente / participación de mercado / riesgo regulatorio]` |

### 4. Valor en tres horizontes

| Horizonte | Qué mostrar | Dato del período | ¿Medido o proyección? |
|---|---|---|---|
| H1 · Eficiencia operacional (0 a 6 meses) | Tiempo, costo, volumen, horas liberadas frente al baseline (línea base) | `[…]` | `[…]` |
| H2 · Calidad y capacidad (6 a 18 meses) | NPS (índice de recomendación del cliente), volumen adicional sin más personal | `[…]` | `[…]` |
| H3 · Transformación estratégica (más de 18 meses) | Nuevos servicios, ventaja competitiva | `[…]` | `[…]` |

**ROI acumulado del portafolio (3.5, panel 5):** `[horas ahorradas, casos resueltos autónomamente, impacto en NPS, reducción de costo operativo]`

### 5. Las tres capas del equipo híbrido (4.6)

| Capa | Indicadores clave | Estado y señal de alerta |
|---|---|---|
| Equipo humano | Satisfacción laboral, carga cognitiva, nivel de adopción, escalaciones iniciadas por el humano | `[…]` |
| Sistema híbrido | Completitud autónoma, tiempo de ciclo de punta a punta, frecuencia de handoffs (traspasos agente-humano), tasa de error | `[…]` |
| Negocio | Volumen por unidad de tiempo, costo por transacción, satisfacción del cliente final, ROI frente al equipo previo | `[…]` |

### 6. Riesgo y control

**¿Qué pasa si falla?** `[impacto posible en clientes o negocio]`
**¿Qué controles tenemos?** `[circuit breaker (corte automático), muestreo de calidad, supervisión humana, Junta de Gobierno…]`
**¿Quién es responsable?** `[AIAM™, Agent Owner (dueño del agente)…]`
**Incidencias del período y cómo se resolvieron:** `[desde el registro de intervenciones, en lenguaje directivo]`

### 7. Decisión o próximo paso

**Lo que pedimos a la dirección:** `[decisión concreta, o "ninguna decisión: solo información"]`
**Criterios para decidir:** `[…]`

### Verificación antes de enviar

- [ ] Empieza por el problema de negocio, no por la tecnología.
- [ ] No quedan términos técnicos sin traducir (logs o registros del sistema, tokens o unidades de texto procesadas, latencia).
- [ ] Están los tres horizontes, aunque H2 y H3 sean proyecciones.
- [ ] Responde qué pasa si falla, qué controles hay y quién responde.
- [ ] Respeta la cadencia: no es un reporte extra que sobrecargue a la dirección.

## Ejemplo lleno

Reporte mensual del piloto del agente de soporte B2B (de empresa a empresa) de la sección 2.5. Las traducciones vienen literalmente de la sección 5.4; **el período, la redacción del problema y el estado del semáforo son datos ficticios de ejemplo**.

- **Tipo y período:** mensual (piloto), del 2026-10-01 al 2026-10-31.
- **Problema de negocio:** los clientes esperaban demasiado por respuestas a problemas técnicos simples, y el equipo de soporte dedicaba su tiempo a casos rutinarios.
- **Estado del portafolio:** agente de soporte B2B en verde.
- **Traducción 1:** en lenguaje técnico, "el agente tiene una tasa de completitud autónoma del 84% con un tiempo de respuesta promedio de 1,3 segundos". En lenguaje directivo: "4 de cada 5 consultas se resuelven sin intervención humana, en menos de 2 segundos. Nuestro equipo se concentra en el 20% que requiere criterio, no en el 80% que ya es rutina".
- **Traducción 2 (riesgo y control):** en lenguaje técnico, "detectamos 3 instancias de behavioral drift (deriva de comportamiento) en el último mes que activaron el circuit breaker y fueron corregidas". En lenguaje directivo: "Nuestro sistema de supervisión detectó y corrigió 3 anomalías antes de que afectaran a ningún cliente. El mecanismo de control funciona exactamente como fue diseñado".
- **Horizontes:** H1 medido (resolución autónoma frente a la meta del 80% de la sección 2.5); H2 y H3 presentados como proyección desde la primera presentación, como pide la 5.2.
- **Decisión pedida:** ninguna este mes; en el reporte trimestral se presentará el Business Case actualizado con la recomendación de próxima fase.

Referencia real del curso: en UPS ORION, la comunicación continua del valor en tres horizontes mantuvo el compromiso de la dirección durante los 10 años de implementación (5.5).

## Errores comunes

1. **Describir la solución técnica antes que el problema de negocio:** "el agente procesa 1.200 solicitudes por día" en vez de "podemos atender el triple de clientes sin contratar a una sola persona adicional" (5.4).
2. **Sobre-reportar:** la sobre-reportería agota la atención directiva y diluye los mensajes importantes; la dirección recibe ciclos estratégicos, no el tablero en tiempo real (5.4).
3. **Llevar métricas técnicas al C-suite:** latencia, uptime (tiempo en funcionamiento) o tokens no son relevantes directamente para la dirección; las métricas de negocio son el lenguaje de reporte del AIAM™ (3.2).
4. **Reportar una sola capa:** un reporte solo técnico o solo humano es incompleto, y uno solo de costos es miope y omite el valor estratégico (pregunta 10 del Módulo 4).
5. **No anticipar la pregunta de riesgo:** la dirección siempre preguntará qué pasa si falla, qué controles hay y quién es responsable (5.4).
