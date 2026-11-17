# 11 · Matriz de riesgos y seguridad

> **Para qué sirve:** reunir en un solo documento los escenarios de falla del agente, su probabilidad e impacto, y los controles que el AI Agent Manager (gestor de agentes de IA) tiene en marcha para cada uno, incluidos los permisos mínimos y las pruebas de límites y adversariales. El curso deja claro que esta protección no se puede delegar en el vendor (proveedor de la tecnología): la debe establecer el propio manager desde el diseño (sección 2.3).
> **Cuándo llenarla:** en el diseño, antes de las pruebas de aceptación; se completa con los resultados de esas pruebas antes de ir a producción y se actualiza cada trimestre, junto con el business case (caso de negocio), y cada vez que la plantilla 10 registre un incidente nuevo.
> **Quién la llena y quién la aprueba:** la llena el AI Agent Manager con el Agent Owner (responsable directo del agente) y el Ethics Reviewer (revisor ético: sesgo, privacidad, equidad y cumplimiento de políticas; sección 4.5); el equipo de IT (sistemas) y Seguridad y el de Legal y Riesgo aportan su mirada. Los agentes de alto riesgo los aprueba el Governance Board (comité de gobierno de agentes, sección 3.6).
> **Con qué se llena:** la ficha de identidad (plantilla 04: alcance, permisos, restricciones, escalamiento), las instrucciones (plantilla 05), los resultados de las pruebas de aceptación (plantilla 06) y el registro de intervenciones (plantilla 10).
> **Base en el curso:** Módulo 1, sección 1.3 (competencia 5: riesgo y ética) y nota crítica de la 1.2; Módulo 2, secciones 2.3 y 2.6, pregunta 10; Módulo 3, sección 3.3; Módulo 5, sección 5.3 (elemento Riesgos) y responsabilidad 2.
> **Se conecta con:** se alimenta de 04 · Ficha de identidad del agente, 05 · Instrucciones del agente, 06 · Onboarding y aceptación y 10 · Registro de intervenciones; alimenta a 02 · Business case (elemento Riesgos), 12 · Governance Board y 14 · Reporte a la dirección.

## Cómo llenarla

1. Revise cada permiso del agente con la regla práctica de la sección 2.3 y anote la justificación de cada uno.
2. Liste los escenarios de falla del agente usando las categorías de la sección C (las que menciona el curso) y agregue los propios de su proceso.
3. Estime la probabilidad y el impacto de cada riesgo y escriba el control activo que lo contiene.
4. Diseñe y ejecute las pruebas de límites, adversariales y de escalamiento (sección 2.6) y anote el resultado.
5. Si alguna prueba falla o algún riesgo alto no tiene control, el agente no pasa a producción.
6. Actualice la matriz cada trimestre y lleve el resumen al business case y a la dirección.

## Plantilla

### A. Datos del agente

**Nombre del agente:** `[ ]` · **Nivel de autonomía (1 a 4):** `[ ]` · **Fecha:** `[AAAA-MM-DD]`
**AI Agent Manager:** `[ ]` · **Agent Owner:** `[ ]` · **Ethics Reviewer:** `[ ]`
**Nota del nivel:** en Nivel 4 el riesgo no es equivalente al de Nivel 2: la diferencia es exponencial, porque el agente toma decisiones consecuentes solo (sección 1.2).

### B. Revisión de permisos mínimos (least-privilege: acceso solo a lo estrictamente necesario; sección 2.3)

| Sistema, base de datos o herramienta | Tipo de acceso (lectura, escritura, envío) | Justificación de negocio | ¿Estrictamente necesario? | Decisión |
|---|---|---|---|---|
| `[ ]` | `[ ]` | `[ ]` | `[sí / no]` | `[mantener / reducir / quitar]` |

**Regla práctica:** "¿Podría este agente, con sus permisos actuales, causar un daño que yo no podría explicar ante el CEO (gerente general) ni ante un cliente?" Respuesta: `[sí / tal vez / no]`. Si es "sí" o "tal vez", se reducen permisos antes de producción.
- [ ] Se rechazó toda solicitud de permisos "por conveniencia" (responsabilidad 3 del Módulo 2).

### C. Matriz de riesgos

Escala sugerida de probabilidad e impacto: alta, media o baja (no viene en el curso; el curso pide estimarlos, pero no fija la escala).

| Riesgo o escenario de falla | Probabilidad | Impacto | Controles activos | Dueño | Estado |
|---|---|---|---|---|---|
| Error silencioso: la tarea parece correcta pero omite algo de fondo (3.3) | `[ ]` | `[ ]` | `[ej.: muestreo del 5% al 10%]` | `[ ]` | `[ ]` |
| Behavioral drift: el agente se aleja poco a poco de sus instrucciones (3.3) | `[ ]` | `[ ]` | `[ej.: tendencia de CSAT (satisfacción del cliente) y comparación con los primeros 30 días]` | `[ ]` | `[ ]` |
| Alucinación con consecuencia real: un dato falso alimenta una decisión automática (3.3) | `[ ]` | `[ ]` | `[ej.: punto de verificación obligatoria]` | `[ ]` | `[ ]` |
| Scope drift: el agente responde fuera de su alcance (pregunta 9 del Módulo 2) | `[ ]` | `[ ]` | `[ej.: restricción explícita y revisión de permisos]` | `[ ]` | `[ ]` |
| Manipulación del agente o acceso a datos que no debería ver (2.3, 2.6) | `[ ]` | `[ ]` | `[ej.: permisos mínimos y prueba adversarial]` | `[ ]` | `[ ]` |
| El agente no escala cuando debe (2.6) | `[ ]` | `[ ]` | `[ej.: prueba de cada condición de escalamiento]` | `[ ]` | `[ ]` |
| Riesgo ético: sesgo, privacidad, equidad o incumplimiento de políticas (4.5) | `[ ]` | `[ ]` | `[ej.: revisión del Ethics Reviewer y circuit breaker]` | `[ ]` | `[ ]` |
| Cambio de regulación, producto o política (3.4) | `[ ]` | `[ ]` | `[ej.: revisión de instrucciones antes del cambio]` | `[ ]` | `[ ]` |
| Degradación de datos al escalar (5.5) | `[ ]` | `[ ]` | `[ej.: auditar datos antes de expandir]` | `[ ]` | `[ ]` |
| Riesgo propio del proceso: `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |

El circuit breaker es el mecanismo que corta o detiene la operación del agente; el curso dice que el Ethics Reviewer puede activarlo (4.5). Para Nivel 4, anote además los criterios de kill switch (apagado de emergencia; sección 1.2).

### D. Guardrails (controles de seguridad) y pruebas antes de producción (sección 2.6)

**Pruebas de límites (boundary testing: empujar al agente hacia fuera de su alcance):**
- [ ] Clientes que piden lo que el agente no puede dar. Resultado: `[ ]`
- [ ] Escenarios ambiguos. Resultado: `[ ]`
- [ ] Preguntas fuera de alcance. Resultado: `[ ]`

**Pruebas adversariales (intentos deliberados de manipular al agente):**
- [ ] Prompts (mensajes escritos al agente) diseñados para engañarlo. Resultado: `[ ]`
- [ ] Solicitudes que explotan ambigüedades de las instrucciones. Resultado: `[ ]`
- [ ] Intentos de acceder a información o funciones no autorizadas. Resultado: `[ ]`

**Prueba de escalamiento:**
- [ ] Cada condición de escalamiento del SOP (procedimiento paso a paso de las instrucciones) fue reconocida y ejecutada. Resultado: `[ ]`

- [ ] Las pruebas adversariales se hicieron aunque los usuarios sean internos y de confianza (pregunta 10 del Módulo 2).

### E. Resumen para el business case y la dirección

**Riesgos principales (máximo 3):** `[ ]` · **Controles activos:** `[ ]` · **Riesgos sin control suficiente y plan:** `[ ]`

## Ejemplo lleno

Datos ficticios de ejemplo sobre el "Agente de Soporte N1" de la sección 2.5 (Nivel 2 según la plantilla 04). Las restricciones y condiciones de escalamiento son las del curso; las estimaciones y resultados son ficticios.

**Permisos:** CRM (sistema de gestión de clientes) en solo lectura, para consultar el historial del cliente: necesario. Base de conocimiento, para buscar soluciones documentadas: necesaria. Escritura en el CRM, pedida por el equipo técnico "para el futuro": quitada (por conveniencia). Regla práctica: con solo lectura no puede causar un daño inexplicable; respuesta "no".

| Riesgo | Prob. | Impacto | Control activo | Dueño |
|---|---|---|---|---|
| Compartir información de otros clientes | Baja | Alto | Restricción explícita en las instrucciones; prueba adversarial; muestreo | Ana Rojas |
| Ofrecer descuentos no autorizados | Media | Medio | Restricción explícita; prueba de límites; muestreo semanal del 8% | Luis Pérez |
| Hacer cambios en la cuenta sin confirmación humana | Baja | Alto | Sin permiso de escritura; restricción explícita | Ana Rojas |
| Omitir el paso de verificación de seguridad (error silencioso) | Media | Alto | Muestreo con ese criterio; ver entrada 2 de la plantilla 10 | Carla Méndez |
| No escalar cuando el cliente menciona cancelación | Media | Alto | Prueba de escalamiento; seguimiento de la tasa de escalamiento | Luis Pérez |

**Pruebas:** límites, 20 casos, aprobados; adversariales, 15 intentos (pedir datos de otro cliente, "ignora tus instrucciones", excusas para un descuento), 14 rechazados y 1 que ofreció un descuento, corregido en las instrucciones y vuelto a probar con éxito; escalamiento, las 3 condiciones (sin resolución documentada, mención de cancelación, más de 8 minutos) reconocidas.

## Errores comunes

- **Confiar en que el proveedor ya resolvió la seguridad.** La AI Agent Index 2025 (Cambridge, MIT, Harvard Law, Stanford y UPenn, 30 sistemas de frontera) encontró que la mayoría de los desarrolladores comparte poca o ninguna información sobre seguridad y riesgos (secciones 2.3 y 2.7).
- **Dar permisos "por conveniencia" o por apuro.** El impacto de un error o de una manipulación crece en proporción al exceso de permisos (sección 2.3).
- **Saltarse las pruebas adversariales porque los usuarios son de confianza.** Las vulnerabilidades surgen de la estructura de las instrucciones, no solo de usuarios maliciosos, y los sistemas internos pueden ser accedidos desde fuera (pregunta 10 del Módulo 2).
- **Presentar un business case sin riesgos.** Pierde credibilidad ante cualquier comité; anticipar riesgos demuestra madurez gerencial (sección 5.3).
- **Sobrerreaccionar ante un riesgo ético.** Desactivar de inmediato el agente destruye valor; lo indicado es documentar, corregir los criterios y escalar para revisión de política (pregunta 2 del Módulo 4).
