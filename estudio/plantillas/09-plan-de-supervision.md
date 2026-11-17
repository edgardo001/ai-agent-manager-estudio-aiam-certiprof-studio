# 09 · Plan de supervisión

> **Para qué sirve:** definir, antes de que el agente entre en producción, qué se va a medir, con qué umbrales se interviene, cómo se detectan los fallos silenciosos y cómo se ve el tablero de supervisión. Es la forma de supervisar resultados y no actividad: "supervisa los resultados con rigurosidad; interviene en los procesos solo cuando los resultados lo justifican" (sección 3.1).
> **Cuándo llenarla:** antes del despliegue de cada agente, junto con la aceptación (plantilla 06); sin esta definición previa, la supervisión es arbitraria (responsabilidad 1 del Módulo 3). Se revisa cada trimestre, cuando cambia el nivel de autonomía o cuando cambia una condición externa (regulación, producto, política).
> **Quién la llena y quién la aprueba:** la llena el AI Agent Manager (gestor de agentes de IA) con el Agent Owner (responsable directo del agente) y el Quality Reviewer (revisor de calidad que valida muestras de outputs, es decir, de resultados del agente; sección 4.5). El equipo técnico aporta la capa técnica. Los agentes de alto riesgo la presentan al Governance Board (comité de gobierno de agentes, sección 3.6).
> **Con qué se llena:** las métricas de éxito de la ficha y de las instrucciones (plantillas 04 y 05), los umbrales de los criterios de aceptación (plantilla 06), el baseline (línea base: cómo era el proceso antes del agente) del business case (plantilla 02) y los datos de los primeros 30 días de operación.
> **Base en el curso:** Módulo 3, secciones 3.1 a 3.5 y responsabilidades 1 a 3; Módulo 1, sección 1.2 (implicaciones de cada nivel de autonomía).
> **Se conecta con:** se alimenta de 02 · Business case, 04 · Ficha de identidad del agente, 05 · Instrucciones del agente y 06 · Onboarding y aceptación; alimenta a 10 · Registro de intervenciones, 12 · Governance Board, 13 · Auditoría trimestral del portafolio y 14 · Reporte a la dirección.

## Cómo llenarla

1. Anote el nivel de autonomía del agente y lo que ese nivel exige de supervisión (sección 1.2).
2. Separe las dos capas: deje la capa técnica al equipo de ingeniería y concéntrese en la capa de negocio (sección 3.2).
3. Defina los cinco KPI (indicadores clave) del set esencial con su baseline, su meta y su umbral de alerta (sección 3.2; obligatorio para Nivel 3 y 4).
4. Diseñe el muestreo cualitativo: entre el 5% y el 10% de los casos, cada semana o cada quincena, contra un criterio de calidad de negocio (sección 3.3 y responsabilidad 2).
5. Defina cómo detectará cada tipo de fallo silencioso y en qué puntos habrá verificación obligatoria (sección 3.3).
6. Traduzca el framework (marco) de intervención a umbrales concretos para este agente (sección 3.4).
7. Arme el dashboard (tablero) de cinco paneles y pruebe que se lee en menos de 90 segundos (sección 3.5).

## Plantilla

### A. Datos del agente

**Nombre del agente:** `[como figura en la plantilla 03]`
**Nivel de autonomía (1 a 4):** `[nivel]` · **Qué exige este nivel:** `[copie la implicación de la sección 1.2]`
**AI Agent Manager:** `[nombre]` · **Agent Owner:** `[nombre]` · **Quality Reviewer:** `[nombre]`
**Fecha del plan:** `[AAAA-MM-DD]` · **Próxima revisión:** `[AAAA-MM-DD]`

### B. Capa técnica (dueño: equipo de ingeniería o IT, es decir, el área de sistemas)

Responde "¿funciona el sistema?". Se revisa en tiempo real o con alertas automáticas. El AI Agent Manager no la reporta a la alta dirección (sección 3.2).

| Métrica técnica | Qué escribir |
|---|---|
| Latencia (tiempo de respuesta del sistema) | Valor de alerta que fija el equipo técnico. |
| Uptime (porcentaje del tiempo en que el sistema está funcionando) | Ídem. |
| Tokens por minuto (volumen de texto que procesa el modelo) | Ídem. |
| Tasa de error de API (fallas de conexión entre sistemas) | Ídem. |
| Contacto técnico que avisa al AI Agent Manager | `[nombre]` |

### C. Capa de negocio: KPI set esencial (dueño: AI Agent Manager)

Responde "¿está generando valor el agente?". Se revisa cada día o cada semana, con análisis de tendencia (sección 3.2).

| KPI | Definición del curso | Baseline (antes del agente) | Meta | Umbral de alerta | Frecuencia | Fuente del dato |
|---|---|---|---|---|---|---|
| Tasa de resolución autónoma | % de casos completados sin intervención humana | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| Tasa de escalamiento | % de casos transferidos a humanos, con tendencia | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| Tiempo promedio de resolución | Comparado con el baseline previo al agente | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| Costo por caso | Inversión total del proceso dividida entre el volumen gestionado | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| Calidad de output | CSAT (satisfacción del cliente), tasa de error detectado después del proceso, o equivalente | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |

### D. Muestreo cualitativo

**Porcentaje de casos revisados:** `[entre el 5% y el 10%]` · **Frecuencia:** `[semanal o quincenal]`
**Criterio de calidad de negocio:** `[qué hace "bien hecho" un caso, más allá de "tarea completada"]`
**Quién revisa:** `[Quality Reviewer o experto del área; en dominios de alto riesgo, un experto, como el experto legal de la pregunta 7 del Módulo 3]`
**Categorías de error que se registran:** `[ej.: omisión de un paso obligatorio, dato incorrecto, tono, fuera de alcance]`

### E. Detección de fallos silenciosos (sección 3.3)

| Tipo | Cómo se detecta en este agente | Qué escribir |
|---|---|---|
| 1. Errores silenciosos (la tarea parece bien hecha pero tiene fallas de fondo) | Muestreo cualitativo periódico | Qué omisión de fondo sería grave en este proceso. |
| 2. Behavioral drift (deriva de comportamiento: se aleja poco a poco de sus instrucciones) | Tendencia de CSAT y de reescalamiento por insatisfacción; comparación de muestras actuales con el baseline de los primeros 30 días | Fecha en que se cierra el baseline de 30 días y qué se compara. |
| 3. Alucinaciones de consecuencia real (datos plausibles pero falsos que otros usan sin verificar) | Puntos de verificación obligatoria antes de decisiones irreversibles o de alto impacto | Lista de outputs que alimentan decisiones automáticas y quién o qué los verifica. |

### F. Umbrales de intervención para este agente (sección 3.4)

| Señal del framework | Se deja correr si… | Se interviene si… | Umbral concreto de este agente |
|---|---|---|---|
| La tasa de escalamiento sube 5% | Fluctuación dentro del rango histórico normal (más o menos 2 semanas) | Supera el umbral de aceptación o hay un patrón sostenido por 3 o más días | `[ ]` |
| El CSAT baja 0,2 puntos en una semana | Variación estacional o evento externo documentado | Coincide con un cambio en las instrucciones o en el volumen o tipo de casos | `[ ]` |
| El tiempo de resolución aumenta 20% | Aumento puntual por un pico de volumen no habitual | Es sostenido y no se relaciona con un cambio de volumen | `[ ]` |
| Cambia una condición externa (regulación, producto, política) | Nunca | Siempre: revisar y actualizar instrucciones antes de que el agente actúe bajo la nueva condición | `[ ]` |
| El muestreo detecta 3 errores en 50 casos | Errores de categorías distintas y sin patrón | Comparten categoría o muestran un patrón en las instrucciones | `[ ]` |

Cada intervención (y cada decisión de dejar correr) se anota en la plantilla 10.

### G. Dashboard de supervisión (sección 3.5)

| Panel | Contenido | Qué escribir |
|---|---|---|
| 1. Estado del portafolio | Semáforo verde, amarillo o rojo por agente; se lee en 15 segundos | Regla para cada color. |
| 2. KPI primarios de negocio | Resolución autónoma, escalamiento, tiempo y costo por caso, frente al baseline y con tendencia de 2 semanas | Origen de los datos. |
| 3. Calidad de output | Casos revisados en el muestreo semanal, categorías de error, tendencia | Quién lo actualiza. |
| 4. Anomalías y alertas | Lista priorizada de umbrales superados, con timestamp (fecha y hora), descripción y acción recomendada | Nunca una alerta sin acción recomendada. |
| 5. ROI acumulado (retorno de la inversión) | Horas ahorradas, casos resueltos solos, impacto en NPS (índice de recomendación del cliente), reducción de costo operativo | Fuente: plantilla 02. |

- [ ] La vista principal tiene como máximo de 5 a 7 métricas primarias; el resto va a paneles de detalle (pregunta 6 del Módulo 3).
- [ ] Alguien que no conoce el agente responde en menos de 90 segundos: "¿genera el valor esperado o requiere mi atención?".
- [ ] Las métricas se acordaron con el equipo técnico, el área de negocio y la dirección: son métricas compartidas (pregunta 10 del Módulo 3).

## Ejemplo lleno

Datos ficticios de ejemplo, sobre el "Agente de Soporte N1" de la sección 2.5 (el mismo de las plantillas 03 y 04). Las metas son las del curso; baselines, nombres y umbrales concretos son ficticios.

**Nivel de autonomía:** 2 (según la plantilla 04). Exige monitorear la calidad del output y definir umbrales de excepción que activen revisión humana (sección 1.2). Aunque el set esencial es obligatorio para Nivel 3 y 4, se usa igual porque coincide con sus métricas de éxito.
**AI Agent Manager:** Ana Rojas · **Agent Owner:** Luis Pérez · **Quality Reviewer:** Carla Méndez.

| KPI | Baseline | Meta (sección 2.5) | Umbral de alerta | Frecuencia |
|---|---|---|---|---|
| Resolución autónoma | 0% (todo lo resolvía una persona) | Mayor o igual al 80% | Menos del 75% por 3 o más días | Diaria |
| Escalamiento | 100% | Menor o igual al 20% | Más del 20% por 3 o más días | Diaria |
| Tiempo promedio | 14 minutos | Menor o igual a 3 minutos | Más de 3 minutos sostenido una semana | Semanal |
| Costo por caso | 9 dólares | 3 dólares | Más de 4 dólares en el mes | Mensual |
| CSAT | 4,0 sobre 5 | Mayor o igual a 4,2 sobre 5 | Baja de 0,2 en una semana sin evento externo | Semanal |

**Muestreo:** 8% de los tickets (solicitudes de soporte) cerrados cada semana; criterio: la solución es la documentada, se cumplió el paso de verificación de seguridad y no se ofreció nada fuera de las restricciones (sin cambios en la cuenta, sin datos de otros clientes, sin descuentos).
**Fallo tipo 1 a vigilar:** omitir la verificación de seguridad, como en la pregunta 3 del Módulo 3. **Tipo 2:** tono que se vuelve informal; baseline de 30 días cerrado el 2026-10-31. **Tipo 3:** el agente no alimenta decisiones automáticas irreversibles; si en el futuro registra datos en el CRM (sistema de gestión de clientes), se agrega un punto de verificación.
**Dashboard:** el panel 1 muestra este agente en verde (82% de resolución, 4,3 de CSAT, 18% de escalamiento, 2,7 minutos).

## Errores comunes

- **Medir lo fácil en vez de lo que importa.** Un agente con 99,9% de uptime puede estar destruyendo la satisfacción del cliente; la falta de métricas de negocio es la causa raíz de la AI Productivity Paradox (paradoja de productividad de la IA) que documenta Gartner (secciones 3.2 y 3.7).
- **Supervisar actividad.** Revisar cada día todo el log (registro) de conversaciones cuando las métricas están dentro de parámetros destruye el valor de la autonomía (sección 3.1 y pregunta 8 del Módulo 3).
- **Confiar en la ausencia de quejas.** Que nadie se queje no valida el trabajo: los errores silenciosos solo se ven con muestreo activo (preguntas 3 y 7 del Módulo 3).
- **Definir las métricas después del despliegue.** Sin baseline previo no hay forma de demostrar valor (sección 3.7 y pregunta 5 del Módulo 3).
- **Un tablero con 23 métricas.** La sobrecarga de información retrasa el diagnóstico (pregunta 6 del Módulo 3).
