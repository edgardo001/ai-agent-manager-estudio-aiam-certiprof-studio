# 04 · Ficha de identidad del agente

> **Para qué sirve:** definir la identidad operacional de un agente con los seis parámetros fundacionales (nombre y rol, alcance, permisos, restricciones, escalamiento y métricas) y su nivel de autonomía, antes de cualquier configuración técnica. Es la arquitectura de gobernanza que determina qué puede hacer el agente, con qué recursos, bajo qué condiciones y quién responde por sus acciones (sección 2.2).
> **Cuándo llenarla:** una vez por agente, apenas se decide crearlo y antes de escribir una sola línea de instrucción. Se actualiza cada vez que cambia su alcance, sus permisos o su nivel, y se revisa en cada auditoría trimestral.
> **Quién la llena y quién la aprueba:** la llena y la firma el AI Agent Manager (gestor de agentes de IA), con apoyo del Agent Owner (responsable directo del agente, sección 4.5). Las métricas las define el AI Agent Manager, no el equipo técnico (sección 2.2). Los permisos los decide el manager como decisión de gobierno de negocio, no se delegan al criterio técnico (pregunta 1 del Módulo 2).
> **Con qué se llena:** la oportunidad y la taxonomía del proceso (plantilla 01), el business case (caso de negocio, plantilla 02), la lista de sistemas que existen en el área, y conversaciones con quienes hacen hoy el trabajo.
> **Base en el curso:** Módulo 1, sección 1.2 (cuatro niveles de autonomía); Módulo 2, secciones 2.2 (seis parámetros) y 2.3 (permisos mínimos y regla práctica); responsabilidades 1 y 3 del Módulo 2.
> **Se conecta con:** se alimenta de 01 · Oportunidades y taxonomía y 02 · Business case; alimenta a 03 · Registro de agentes, 05 · Instrucciones del agente, 06 · Onboarding y aceptación, 09 · Plan de supervisión y 11 · Matriz de riesgos y seguridad.

## Cómo llenarla

1. Escriba el nombre y, en una sola oración, el rol: qué problema resuelve, para quién y en qué contexto.
2. Clasifique el nivel de autonomía (1 a 4) y copie las implicaciones de supervisión de ese nivel.
3. Defina el alcance: qué procesos, datos y sistemas abarca y, sobre todo, cuáles quedan explícitamente fuera.
4. Liste cada permiso de acceso con su justificación. Borre todo permiso que no pueda justificar con la función del agente.
5. Escriba las restricciones (lo que el agente no puede hacer bajo ninguna circunstancia) y las condiciones de escalamiento a un humano.
6. Defina las métricas de éxito en términos de negocio.
7. Haga la prueba de la regla práctica de la sección 2.3. Si la respuesta es "sí" o "tal vez", reduzca el alcance antes de seguir.

## Plantilla

### 1. Nombre y rol

**Nombre del agente:** `[escriba aquí…]` (da claridad de comunicación en la organización)
**Rol en una oración:** `[qué problema resuelve, para quién y en qué contexto operacional]`
**AI Agent Manager responsable:** `[nombre]`  **Agent Owner:** `[nombre]`

### 2. Nivel de autonomía (sección 1.2)

| Nivel | Qué hace el agente | Qué exige al manager | Marque |
|---|---|---|---|
| 1 Asistencia | Sugiere; el humano decide y actúa. | Humano en el loop (en el circuito) en cada decisión; supervisar la calidad de las sugerencias y su ajuste al contexto de negocio. | [ ] |
| 2 Automatización | Completa tareas bien definidas sin intervención humana en cada caso. | Monitorear la calidad del output (resultado) y definir umbrales de excepción que activen revisión humana. | [ ] |
| 3 Augmentación | Combina herramientas, adapta su enfoque y completa objetivos de varios pasos. | Revisión periódica del proceso y de las decisiones; auditoría de calidad, no de cada acción; métricas de negocio como indicador primario. | [ ] |
| 4 Autonomía Total | Actúa end-to-end (de punta a punta) sin confirmación humana en procesos consecuentes. | Máxima gobernanza: límites operacionales precisos, protocolos de escalamiento, criterios de kill switch (botón de apagado de emergencia) y auditoría continua. | [ ] |

**Justificación del nivel elegido:** `[por qué este nivel y no el siguiente]`
**Umbrales de excepción (nivel 2) o criterios de kill switch (nivel 4):** `[escriba aquí, si aplica]`

### 3. Alcance

**Procesos, datos y sistemas que abarca:** `[escriba aquí…]`
**Explícitamente fuera de alcance:** `[escriba aquí…]` (sin límites de alcance, el agente puede derivar hacia funciones no autorizadas)

### 4. Permisos de acceso (permisos mínimos, sección 2.3)

El principio de permisos mínimos, en inglés least-privilege (el menor privilegio posible), exige dar acceso solo a lo estrictamente necesario para la función, y ninguno más. Documente la justificación de cada permiso (responsabilidad 3 del Módulo 2). La columna "Tipo de acceso" no viene en el curso; es una ayuda práctica para ver si basta con consultar.

| Sistema, API (conexión con otro sistema), base de datos o herramienta | Tipo de acceso | Justificación con la función del agente | ¿Es estrictamente necesario? |
|---|---|---|---|
| `[…]` | `[consulta / modificación…]` | `[…]` | `[sí / no → revocar]` |

- [ ] Ningún permiso fue otorgado "por conveniencia" (se rechaza, responsabilidad 3 del Módulo 2).
- [ ] Ningún permiso viene de la configuración inicial sin revisión, de la falta de definición del alcance o de la presión por desplegar rápido (sección 2.3).

### 5. Restricciones operacionales

Lo que el agente NO puede hacer bajo ninguna circunstancia (decisiones que requieren juicio humano, transacciones sobre un umbral financiero, comunicaciones externas no autorizadas, etcétera):
`[escriba aquí, una por línea…]`

### 6. Protocolos de escalamiento

Condiciones en que el agente transfiere el control a un humano (casos ambiguos, alto riesgo, clientes insatisfechos, errores detectados):
`[condición → a quién se transfiere]`

### 7. Métricas de éxito (de negocio)

| Métrica | Meta | Cómo se mide |
|---|---|---|
| `[…]` | `[…]` | `[…]` |

### 8. Prueba final: regla práctica (sección 2.3)

"¿Podría este agente, con sus permisos actuales, causar un daño que yo no podría explicar ante el CEO (gerente general) ni ante un cliente?"
**Respuesta:** `[no / sí / tal vez]` → si es "sí" o "tal vez", los permisos son excesivos: reduzca el alcance antes de ir a producción.
**Firma del AI Agent Manager y fecha:** `[nombre, AAAA-MM-DD]`

## Ejemplo lleno

Agente de soporte B2B (de empresa a empresa) de la sección 2.5. Lo que viene del curso: contexto, objetivo, herramientas, restricciones, escalamiento y métricas. Son datos ficticios de ejemplo: el nombre, las personas, la clasificación de nivel, el tipo de acceso y la fila del sistema de facturación revocado.

**Nombre:** Agente de Soporte N1. **Rol:** resolver los tickets (solicitudes) de soporte de nivel 1 que los clientes existentes de una empresa de software B2B reportan en el portal de soporte, dentro del área de Customer Success (éxito del cliente).
**AI Agent Manager:** Ana Rojas. **Agent Owner:** Luis Pérez.

**Nivel:** 2, Automatización. **Justificación:** completa una tarea bien definida (tickets de nivel 1 con solución documentada) sin intervención en cada caso, y no puede cambiar cuentas sin confirmación humana. Si se le permitiera modificar cuentas o actuar en varios sistemas por su cuenta, habría que reclasificarlo en Nivel 3. **Umbrales de excepción:** los mismos tres criterios de escalamiento de abajo.

**Alcance:** tickets de nivel 1 de clientes existentes que llegan por el portal de soporte. **Fuera de alcance:** cambios en la cuenta del cliente, descuentos, cancelaciones, tickets sin resolución documentada.

| Sistema | Tipo de acceso | Justificación | ¿Necesario? |
|---|---|---|---|
| CRM (sistema de gestión de clientes) | Consulta | Consultar el historial del cliente | Sí |
| Base de conocimiento | Consulta | Buscar soluciones documentadas | Sí |
| Sistema de facturación | Modificación | Venía en la configuración inicial "por si acaso" | No → revocado |

**Restricciones:** no realizar cambios en la cuenta del cliente sin confirmación humana; no compartir información de otros clientes; no ofrecer descuentos no autorizados.

**Escalamiento:** escalar a un humano con contexto completo si el ticket no tiene resolución documentada, si el cliente menciona cancelación o si el tiempo de resolución supera 8 minutos.

**Métricas:** tasa de resolución autónoma mayor o igual al 80%; CSAT (satisfacción del cliente) mayor o igual a 4,2 sobre 5; tasa de escalamiento menor o igual al 20%; tiempo promedio de resolución menor o igual a 3 minutos.

**Regla práctica:** con el acceso de modificación a facturación la respuesta era "tal vez"; tras revocarlo, la respuesta es "no".

## Errores comunes

- **Escribir instrucciones antes de definir la identidad.** La ficha es el punto de partida del onboarding (incorporación), no un artefacto posterior (responsabilidad 1 del Módulo 2).
- **Dar permisos de más "por si acaso".** Si el agente se equivoca o es manipulado, el impacto crece en proporción al exceso de permisos (sección 2.3; pregunta 1 del Módulo 2: un agente de inventario no necesita nómina ni reportes financieros).
- **Confiar en que el proveedor ya resolvió la seguridad.** La AI Agent Index 2025 (índice de agentes de IA, de Cambridge, MIT, Harvard Law, Stanford y UPenn) encontró que la mayoría de los desarrolladores comparte poca o ninguna información de seguridad; el manager debe establecer la protección desde el diseño (sección 2.3).
- **Dejar en blanco restricciones y escalamiento.** Son los parámetros que más se omiten y la brecha que más fallos genera en producción (reflexión estratégica del Módulo 2).
- **Subestimar el nivel.** Implementar un agente de Nivel 4 como si tuviera el riesgo de uno de Nivel 2 es un error frecuente (sección 1.2, nota crítica).
