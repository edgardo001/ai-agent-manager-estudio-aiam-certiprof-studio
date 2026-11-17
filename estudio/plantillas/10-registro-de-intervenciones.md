# 10 · Registro de intervenciones

> **Para qué sirve:** dejar por escrito cada vez que una señal del agente obliga a decidir si se interviene o se deja correr: qué se vio, qué criterio se aplicó, qué se hizo y cómo terminó. El curso pide que el Governance Board (comité de gobierno de agentes) produzca "decisiones de intervención documentadas" y que ninguna alerta quede sin acción documentada (secciones 3.5 y 3.6).
> **Cuándo llenarla:** cada vez que el dashboard (tablero de supervisión) muestre una alerta, que el muestreo encuentre errores, que cambie una condición externa o que alguien reporte un incidente. Se abre el mismo día y se cierra cuando se verifica el resultado.
> **Quién la llena y quién la aprueba:** la llena el AI Agent Manager (gestor de agentes de IA) o el Agent Owner (responsable directo del agente, primer contacto ante incidencias; sección 4.5). Aportan el Quality Reviewer (revisor de calidad) y el Ethics Reviewer (revisor ético). Las decisiones que superan la autoridad del AI Agent Manager se escalan al Governance Board.
> **Con qué se llena:** los umbrales de la plantilla 09, el panel 4 del dashboard (anomalías y alertas), los resultados del muestreo cualitativo, el audit trail (registro de razonamiento del agente) y los reportes del equipo.
> **Base en el curso:** Módulo 3, secciones 3.3, 3.4, 3.5 y 3.6; Módulo 1, sección 1.2 (kill switch en Nivel 4) y pregunta 9 (audit trail); Módulo 2, pregunta 9 (scope drift); Módulo 4, sección 4.5 (circuit breaker).
> **Se conecta con:** se alimenta de 09 · Plan de supervisión y 11 · Matriz de riesgos y seguridad; alimenta a 05 · Instrucciones del agente (cuando hay que corregirlas), 12 · Governance Board, 13 · Auditoría trimestral del portafolio y 14 · Reporte a la dirección.

## Cómo llenarla

1. Anote la señal tal como apareció, con fecha, hora y fuente, y compárela con el umbral definido en la plantilla 09.
2. Revise el audit trail de los casos afectados para entender qué decidió el agente y por qué.
3. Aplique el framework (marco) de intervención de la sección 3.4: ¿es ruido normal o una señal real? Escriba el criterio que usó.
4. Si hay que intervenir, clasifique el fallo (tipo 1, 2 o 3 de la sección 3.3, scope drift o cambio externo) y elija la acción.
5. Asigne un responsable y una fecha, y defina cómo sabrá que la intervención funcionó.
6. Cierre la entrada cuando la métrica vuelva a su rango, y lleve las entradas relevantes al Governance Board y al reporte a la dirección.

## Plantilla

### A. Requisitos previos del agente (se revisan una vez)

- [ ] El agente documenta en cada caso los criterios de decisión que aplicó (audit trail), porque el AI Agent Manager responde por esas decisiones ante el cliente y la organización (pregunta 9 del Módulo 1).
- [ ] Están definidos los umbrales de intervención (plantilla 09, sección F).
- [ ] Si el agente es de Nivel 4, están definidos los criterios de kill switch (apagado de emergencia que detiene al agente), junto con límites operacionales y protocolos de escalamiento (sección 1.2).
- [ ] Está definido quién puede activar el circuit breaker (mecanismo de corte que detiene o frena la operación del agente); el curso indica que el Ethics Reviewer puede activarlo (sección 4.5).
- [ ] Cómo se activan técnicamente el circuit breaker y el kill switch: `[describir]` (el curso no detalla el mecanismo; no viene en el curso).

### B. Ficha de cada intervención

| Campo | Qué escribir |
|---|---|
| N.º y agente | Correlativo y nombre del agente (como en la plantilla 03). |
| Fecha y hora de detección | El timestamp (fecha y hora) de la alerta. |
| Fuente | Panel 4 del dashboard, muestreo cualitativo, Quality Reviewer, Ethics Reviewer, cliente, equipo humano o aviso de cambio externo. |
| Señal observada | El dato concreto: "escalamiento pasó del 8% al 19% en dos semanas". |
| Umbral de referencia | El umbral de la plantilla 09 que se compara. |
| Contexto revisado | ¿Hubo cambio de instrucciones, de volumen o tipo de casos, evento externo o estacional? ¿Qué muestra el audit trail? |
| Decisión | Dejar correr o intervenir. |
| Criterio aplicado | La regla de la sección 3.4 que justifica la decisión. |
| Clasificación del fallo | Tipo 1 (error silencioso), tipo 2 (behavioral drift, deriva de comportamiento), tipo 3 (alucinación de consecuencia real), scope drift (el agente amplió su alcance sin autorización), cambio de condición externa, otro. |
| Acción | Ver la lista de acciones del curso, abajo. |
| Responsable y fecha límite | Nombre y fecha. |
| Verificación | Qué métrica debe volver a qué valor y cuándo se mide. |
| Escalado a | Nadie, Governance Board o dirección, y por qué. |
| Estado y fecha de cierre | Abierta, en curso o cerrada. |

### C. Acciones que el curso indica según la situación

- [ ] Muestreo cualitativo inmediato de los casos afectados para encontrar el patrón (pregunta 1 del Módulo 3).
- [ ] Revisar y actualizar las instrucciones del agente (plantilla 05) antes de que actúe bajo una condición nueva (sección 3.4).
- [ ] Formalizar el nuevo alcance o restringirlo explícitamente, y revisar los permisos de acceso (pregunta 9 del Módulo 2).
- [ ] Agregar un punto de verificación obligatoria antes de decisiones irreversibles (sección 3.3, tipo 3).
- [ ] Activar el protocolo del Ethics Reviewer, documentar el patrón, ajustar los criterios del agente y comunicar a la Junta de Gobierno Agentic (pregunta 2 del Módulo 4).
- [ ] Activar el circuit breaker o el kill switch.
- [ ] Escalar al Governance Board decisiones que superan la autoridad del AI Agent Manager (sección 3.6).

### D. Tabla resumen del período

| N.º | Fecha | Agente | Señal | Decisión | Tipo de fallo | Acción | Responsable | Estado |
|---|---|---|---|---|---|---|---|---|
| `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |

Registrar también las decisiones de dejar correr permite demostrar después que la señal se vio y se evaluó (no viene en el curso).

## Ejemplo lleno

Datos ficticios de ejemplo sobre el "Agente de Soporte N1" de la sección 2.5. Las situaciones 2 y 4 imitan las preguntas 3 y 1 del Módulo 3.

| N.º | Fecha | Señal | Contexto revisado | Decisión y criterio | Tipo | Acción y responsable | Estado |
|---|---|---|---|---|---|---|---|
| 1 | 2026-10-06 | CSAT (satisfacción del cliente) bajó de 4,3 a 4,1 en una semana | Coincide con el lanzamiento de una versión nueva del producto, documentado; las instrucciones no cambiaron | Dejar correr: variación por evento externo documentado (sección 3.4) | Ninguno | Volver a medir en 2 semanas; Luis Pérez | Cerrada: 4,3 el 2026-10-20 |
| 2 | 2026-10-13 | El muestreo encontró 12 de 50 casos sin el paso de verificación de seguridad; ninguno generó queja | El audit trail muestra que el agente no aplicaba el paso en consultas de cambio de contraseña | Intervenir: los errores comparten categoría y siguen un patrón de las instrucciones | Tipo 1, error silencioso | Reescribir el paso en las instrucciones (plantilla 05) y repetir el muestreo la semana siguiente; Ana Rojas | Cerrada: 0 de 50 el 2026-10-27 |
| 3 | 2026-10-20 | La empresa cambia su política de reembolsos desde el 1 de noviembre | Cambio de condición externa | Intervenir siempre: actualizar las instrucciones antes de que rija la política (sección 3.4) | Cambio externo | Actualizar restricciones y escalamiento; Ana Rojas; antes del 2026-10-30 | Cerrada |
| 4 | 2026-11-10 | El escalamiento subió del 18% al 26% y se mantuvo 4 días; las métricas técnicas están perfectas | Sin cambio de volumen; muchos escalamientos por mención de cancelación | Intervenir: supera el umbral del 20% con patrón de 3 o más días | Posible behavioral drift | Muestreo inmediato de los casos escalados; Carla Méndez | En curso |

**Escalado al Governance Board:** ninguna en este período; la entrada 4 se informará en la próxima sesión si no se cierra antes.

## Errores comunes

- **Intervenir ante el ruido.** Intervenir antes de tiempo destruye el valor de la autonomía y deja al manager atrapado en la operación (sección 3.4).
- **No intervenir cuando corresponde.** Los fallos silenciosos que no se atienden crecen hasta ser crisis de negocio (sección 3.4).
- **Esperar a que el cambio externo "se note".** Ante una regulación, producto o política nueva, siempre se revisan las instrucciones antes (sección 3.4).
- **Tratar un problema de gobernanza como uno técnico.** Que el agente tome decisiones que nadie puede explicar se resuelve con transparencia (audit trail), no quitándole autonomía ni delegándolo a ingeniería (pregunta 9 del Módulo 1).
- **Dejar alertas sin acción.** Un dashboard sin acciones asociadas a sus alertas es decorativo (responsabilidad 3 del Módulo 3).
