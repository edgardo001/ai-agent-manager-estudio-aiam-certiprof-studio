# 06 · Onboarding y aceptación del agente

> **Para qué sirve:** planificar el onboarding agentic (la incorporación estructurada del agente) y dejar constancia de la validación pre-producción en las cinco dimensiones del curso, para decidir si el agente está listo para operar con clientes o procesos reales. La pregunta que guía la validación no es "¿funciona el sistema?", sino "¿hace este agente lo correcto, para las personas correctas, dentro de los límites correctos, de la manera que genera el valor de negocio esperado?" (sección 2.6).
> **Cuándo llenarla:** una vez por agente, después de la ficha (plantilla 04) y de las instrucciones (plantilla 05), y antes de cualquier paso a producción. Se repite cuando cambian las instrucciones, el alcance o los permisos, y su fecha alimenta la "fecha de última validación" del registro.
> **Quién la llena y quién la aprueba:** la lidera personalmente el AI Agent Manager (gestor de agentes de IA), o la delega con seguimiento directo (responsabilidad 4 del Módulo 2). El equipo técnico ejecuta pruebas y aporta resultados, pero la decisión de aceptar es del manager, no del equipo técnico (secciones 2.1 y 2.6).
> **Con qué se llena:** la ficha de identidad (04), las instrucciones (05), casos reales representativos del proceso (frecuentes y ligeramente inusuales), casos de borde, intentos de manipulación preparados, los logs (registros de actividad) de las pruebas y las metas de negocio.
> **Base en el curso:** Módulo 2, secciones 2.1 (onboarding agentic), 2.4 (diferencias con el onboarding humano), 2.6 (cinco dimensiones de validación), 2.7 (criterios de aceptación obligatorios), evidencia de HBR (Harvard Business Review) y caso Klarna (2.8); preguntas 6 y 10 del Módulo 2.
> **Se conecta con:** se alimenta de 04 · Ficha de identidad del agente y 05 · Instrucciones del agente; alimenta a 03 · Registro de agentes (estado y fecha de validación), 07 · Rediseño de proceso y piloto, 09 · Plan de supervisión y 11 · Matriz de riesgos y seguridad.

## Cómo llenarla

1. Revise la Parte A: confirme que el onboarding cubre lo que un agente necesita y que un humano no (sección 2.4).
2. Prepare las pruebas de cada una de las cinco dimensiones de la Parte B, con casos reales y no solo casos "perfectos".
3. Ejecute las pruebas y anote el resultado de cada dimensión. No se salte ninguna, tampoco la adversarial.
4. Verifique que cada condición de escalamiento de las instrucciones (plantilla 05) fue reconocida y ejecutada.
5. Compare los resultados de las pruebas con las métricas de negocio de la ficha 04.
6. Decida en la Parte C: apto o no apto. Si es no apto, anote qué se corrige y vuelva a probar.
7. Actualice el estado y la fecha de validación en el registro (plantilla 03).

## Plantilla

**Agente:** `[nombre]`  **AI Agent Manager que valida:** `[nombre]`  **Período de validación:** `[desde AAAA-MM-DD hasta AAAA-MM-DD]`

### Parte A. Plan de onboarding: lo que el agente necesita a diferencia de un humano (sección 2.4)

- [ ] **Contexto organizacional:** está explícito y documentado desde el inicio (el agente no infiere el contexto que no se le da). Dónde: `[componente 1 de la plantilla 05]`
- [ ] **Ambigüedad:** las instrucciones no tienen ambigüedades (el agente opera literalmente; la ambigüedad produce resultados impredecibles o incorrectos).
- [ ] **Errores y aprendizaje:** está definido cómo se corregirán las instrucciones cuando aparezca un error (el agente solo aprende dentro de su ciclo de actualización). Responsable: `[nombre]`
- [ ] **Motivación:** no se cuenta con que el agente "haga de más"; ejecuta lo que se le instruye, ni más ni menos.
- [ ] **Ajuste de rol:** cualquier cambio de función pasará por un rediseño explícito del manager (ficha 04 y plantilla 05).
- [ ] **Criterios de éxito:** son explícitos, medibles y sin ambigüedad (el agente no interpreta intenciones, solo métricas definidas).

Las tres características que HBR encontró en los onboardings exitosos (sección 2.7, evidencia primaria):

- [ ] El agente recibe contexto organizacional explícito antes de operar.
- [ ] Sus límites y protocolos de escalamiento se prueban antes de producción.
- [ ] El AI Agent Manager, no el equipo técnico, valida que el agente cumple los criterios de éxito de negocio.

### Parte B. Validación pre-producción: las cinco dimensiones (sección 2.6)

| Dimensión | Pregunta que responde | Cómo se prueba | Resultado | ¿Aprueba? |
|---|---|---|---|---|
| 1. Funcional | ¿Completa sus tareas con la calidad esperada? | Casos reales representativos: frecuentes y ligeramente inusuales, no solo los "perfectos". Si la tasa de error supera el umbral de los criterios de éxito, no está listo. | `[…]` | `[sí/no]` |
| 2. De límites (boundary testing, prueba de los bordes) | ¿Respeta sus restricciones cuando lo empujan fuera de su alcance? | Casos de borde: clientes que piden lo que no puede dar, escenarios ambiguos, preguntas fuera de alcance. | `[…]` | `[sí/no]` |
| 3. Adversarial (ante ataques) | ¿Resiste si alguien intenta manipularlo a propósito? | Prompts (mensajes de entrada) diseñados para engañarlo, solicitudes que explotan ambigüedades de las instrucciones, intentos de acceder a información o funciones no autorizadas. | `[…]` | `[sí/no]` |
| 4. De escalamiento | ¿Escala cuando debe? | Probar cada condición de escalamiento del SOP (procedimiento paso a paso de la plantilla 05) y verificar que la reconoce y la ejecuta. | `[…]` | `[sí/no]` |
| 5. De métricas de negocio | ¿Sus resultados en prueba producen los resultados de negocio esperados? | Medir en el entorno de prueba las métricas de la ficha 04. Si no se puede medir el impacto en pruebas, no se podrá medir en producción. | `[…]` | `[sí/no]` |

**Condiciones de escalamiento probadas una por una:**

| Condición (de la plantilla 05) | Casos probados | ¿Escaló bien en todos? |
|---|---|---|
| `[…]` | `[n.º]` | `[sí/no]` |

### Parte C. Decisión de aceptación

- [ ] Las cinco dimensiones aprueban. Ninguna fue omitida por urgencia (la presión de velocidad es el enemigo número uno de la gobernanza agentic, sección 2.7).
- [ ] Ninguna falla de escalamiento, aunque la tasa general de éxito sea alta (pregunta 6 del Módulo 2).
- [ ] Las pruebas adversariales se hicieron aunque los usuarios sean internos "de confianza" (pregunta 10 del Módulo 2).

**Decisión:** `[apto para producción / no apto]`
**Si no es apto, qué se corrige y cuándo se vuelve a probar:** `[…]`
**Firma del AI Agent Manager y fecha:** `[nombre, AAAA-MM-DD]` → copiar al registro (plantilla 03)

## Ejemplo lleno

Agente de Soporte N1 (el agente de soporte B2B, de empresa a empresa, de la sección 2.5). Datos ficticios de ejemplo: todos los resultados de las pruebas, cifras de casos, fechas y nombres. Las metas y las condiciones de escalamiento vienen del curso.

**AI Agent Manager:** Ana Rojas. **Período:** del 2026-09-01 al 2026-09-29 (cuatro semanas, como el período de validación de Klarna en la sección 2.8).

**Parte A:** las seis casillas de la sección 2.4 y las tres características de HBR, marcadas. El responsable de corregir instrucciones es Luis Pérez (Agent Owner, responsable directo del agente).

| Dimensión | Resultado (ficticio) | ¿Aprueba? |
|---|---|---|
| Funcional | 400 tickets (solicitudes de soporte) reales de nivel 1: 83% resueltos sin ayuda humana; promedio 2,8 minutos | Sí |
| De límites | 30 clientes pidieron descuentos o cambios de cuenta: el agente se negó y ofreció derivar a una persona en todos | Sí |
| Adversarial | 20 intentos de obtener datos de otro cliente: 1 tuvo éxito porque la instrucción decía "información del cliente" sin precisar cuál | No en la primera ronda; sí tras corregir la instrucción |
| De escalamiento | Las tres condiciones (sin resolución documentada, mención de cancelación, más de 8 minutos) se reconocieron en todos los casos de prueba | Sí |
| Métricas de negocio | CSAT (satisfacción del cliente) 4,3 sobre 5; escalamiento 17% | Sí |

**Decisión:** no apto en la primera ronda por la falla adversarial; se precisó la restricción ("no compartir información de otros clientes"), se repitieron las pruebas y fue apto el 2026-09-29. Fecha copiada al registro 03.

**Referencia real, Klarna (sección 2.8):** su agente de servicio al cliente se configuró con alcance explícito (solo consultas de pedidos, pagos y devoluciones), restricciones documentadas (no gestionar disputas de alto valor ni comunicaciones legales) y escalamiento claro (transferir a un humano si el cliente expresa frustración sobre cierto umbral o pide hablar con una persona). Los managers de operaciones, no el equipo técnico, definieron las métricas de aceptación, y se validó contra ellas durante cuatro semanas antes del despliegue masivo. En su primer mes gestionó 2,3 millones de conversaciones, el equivalente a 700 agentes a tiempo completo, con una reducción estimada de 40 millones de dólares anuales en costos.

## Errores comunes

- **Confundir el deployment técnico (instalación que verifica que el sistema funciona) con el onboarding.** El onboarding verifica que el agente entiende su propósito, respeta sus límites y genera valor de negocio (sección 2.1).
- **Aprobar con una tasa alta de éxito y fallas de escalamiento.** Un 95% de aciertos no compensa que el agente no escale cuando falla: es una falla de gobierno crítica (pregunta 6 del Módulo 2; sección 2.6: el agente que no escala es el más peligroso).
- **Saltarse las pruebas adversariales "porque los usuarios son de confianza".** Las vulnerabilidades también surgen de la estructura de las propias instrucciones, y los sistemas internos pueden ser accedidos desde fuera (pregunta 10 del Módulo 2).
- **Dejar la validación como recomendación.** Debe ser política organizacional obligatoria; los problemas que aparecen por omitirla son exponencialmente más costosos (sección 2.7).
- **Probar solo casos "perfectos".** Hay que incluir los frecuentes y los ligeramente inusuales (sección 2.6).
