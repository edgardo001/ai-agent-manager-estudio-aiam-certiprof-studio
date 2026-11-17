# 08 · Gestión del cambio y roles del equipo híbrido

> **Para qué sirve:** preparar a las personas para trabajar con agentes: narrativa del cambio, diagnóstico de resistencias, plan de formación en 3 niveles de adopción, asignación explícita de los 6 roles del equipo híbrido y seguimiento de los indicadores en 3 capas (humano, sistema y negocio).
> **Cuándo llenarla:** junto con el rediseño del proceso (plantilla 07), antes del piloto. Los roles se revisan cada vez que entra o sale una persona o un agente; los indicadores, de forma continua, y el conjunto, cada trimestre.
> **Quién la llena y quién la aprueba:** la llena el AI Agent Manager (AIAM™) con el Change Champion (referente del cambio en el equipo). Los hallazgos de la capa de negocio se escalan a la junta de gobierno agentic (sección 4.6). La aprobación de la plantilla no viene en el curso; se sugiere la dirección del área.
> **Con qué se llena:** la plantilla 07 (proceso TO-BE, es decir, el proceso futuro), la lista de personas y roles del equipo, encuestas o entrevistas 1 a 1, y los datos de indicadores del agente y del negocio.
> **Base en el curso:** Módulo 4: sección 4.1 (equipo híbrido), 4.4 (gestión del cambio, resistencias y 3 niveles de adopción), 4.5 (nuevos roles), 4.6 (indicadores en 3 capas), caso Accenture, responsabilidades 3, 4 y 5 del Módulo 4 y preguntas 2, 3, 4, 7 y 8.
> **Se conecta con:** se alimenta de 07 (07-rediseno-de-proceso-y-piloto.md). Alimenta a 03 (03-registro-de-agentes.md, Agent Owner de cada agente), 09 (09-plan-de-supervision.md), 12 (12-governance-board.md) y 14 (14-reporte-a-la-direccion.md).

## Cómo llenarla

1. Escriba la narrativa del cambio: por qué cambia el proceso, qué rol ocupa el agente y cómo evolucionará el rol humano.
2. Asigne cada uno de los 6 roles a una persona con nombre. En equipos pequeños una persona puede tener varios roles; lo que no puede haber es un rol sin dueño.
3. Defina para cada rol del equipo el nivel de adopción que debe alcanzar (1, 2 o 3) y la formación para llegar.
4. Diagnostique las 3 manifestaciones de resistencia y anote cómo va a intervenir.
5. Fije los indicadores de las 3 capas, sus señales de alerta y la acción prevista.
6. Revise las señales periódicamente y documente cada acción correctiva antes de que el problema escale.

## Plantilla

### A. Narrativa del cambio

Los equipos que reciben una narrativa clara reportan tasas de adopción 2,4 veces superiores a los que reciben solo entrenamiento técnico (Deloitte, sección 4.4).

| Pregunta | Qué escribir |
|---|---|
| ¿Por qué cambia el proceso? | `[escriba aquí…]` |
| ¿Qué rol ocupa el agente? | `[escriba aquí…]` Qué hace y qué no hace. |
| ¿Cómo evoluciona el rol humano? | `[escriba aquí…]` Qué tareas ganan las personas (criterio, relaciones, ética, creatividad). |
| Canal y fecha de comunicación | `[escriba aquí…]` (no viene en el curso; campo práctico) |

### B. Asignación de roles del equipo híbrido (sección 4.5)

| Rol | Responsabilidad principal | Relación con el AIAM™ | Persona asignada |
|---|---|---|---|
| Agent Owner (dueño del agente) | Define el propósito de uno o más agentes, valida sus outputs (resultados), escala sus fallos y gestiona su ciclo de vida | Reporta al AIAM™; primer contacto ante incidencias | `[nombre]` |
| Workflow Designer (diseñador de flujos) | Mapea el AS-IS (proceso actual), diseña el TO-BE (proceso futuro), define los handoffs (traspasos) y mantiene la documentación | Trabaja bajo dirección del AIAM™ con el método de 5 pasos | `[nombre]` |
| Quality Reviewer (revisor de calidad) | Valida muestras de outputs para detectar deriva de comportamiento, alucinaciones (datos inventados) y errores de contexto | Da insumos al AIAM™ para decisiones de intervención | `[nombre]` |
| Change Champion (referente del cambio) | Facilita la formación entre pares, comunica el sentido del cambio, hace de interfaz entre el equipo y la transformación | Aliado estratégico del AIAM™ ante la resistencia cultural | `[nombre]` |
| Ethics Reviewer (revisor ético) | Evalúa sesgo, privacidad, equidad y cumplimiento de políticas internas en los outputs | Escala riesgos éticos al AIAM™; puede activar el circuit breaker (corte de emergencia del agente) | `[nombre]` |
| AI Agent Manager (AIAM™) | Diseña el equipo híbrido, gestiona la taxonomía, lidera el rediseño, comunica a la dirección y garantiza la gobernanza | Rol central; responde ante la dirección | `[nombre]` |

- [ ] Ningún rol quedó sin persona asignada (sin gaps, es decir, vacíos, de propiedad).
- [ ] Cada agente tiene un Agent Owner asignado (lección del caso Accenture).

### C. Plan de formación en 3 niveles de adopción (sección 4.4)

Nivel 1, Conciencia: entiende qué hace el agente, sus capacidades y límites, y cómo leer sus outputs. Nivel 2, Competencia: diseña instrucciones efectivas, interpreta resultados, detecta errores y decide sobre ellos. Nivel 3, Colaboración Estratégica: rediseña su propia forma de trabajar, propone mejoras al flujo híbrido y actúa como sensor de calidad. No todos los roles necesitan el nivel 3.

| Rol del equipo | Nivel actual | Nivel objetivo | Formación prevista | Fecha |
|---|---|---|---|---|
| `[rol]` | `[1 / 2 / 3]` | `[1 / 2 / 3]` | `[…]` | `[…]` |

### D. Diagnóstico de resistencia (sección 4.4)

Las tres son responsabilidad del manager, no del trabajador.

| Manifestación | Cómo se ve | ¿Aparece? Evidencia | Intervención prevista |
|---|---|---|---|
| Rechazo activo | "El agente comete errores" | `[…]` | `[…]` |
| Rechazo pasivo | No reporta los fallos del agente para no depender de él | `[…]` | `[…]` |
| Sobre-dependencia | Delega incluso tareas que requieren criterio humano | `[…]` | `[…]` El curso indica formación en el nivel 2 y criterios de revisión obligatoria (pregunta 4 del Módulo 4). |

### E. Indicadores en 3 capas (sección 4.6)

Ninguna capa basta por sí sola; se leen juntas.

| Capa | Indicadores clave | Señales de alerta | Acción del AIAM™ | Valor actual |
|---|---|---|---|---|
| Equipo humano | Satisfacción laboral, carga cognitiva percibida, nivel de adopción, tasa de escalación iniciada por el humano | Más quejas, menos uso voluntario del agente, más horas extra sin menos volumen | Revisar el nivel de adopción, ajustar la formación, entrevistas 1 a 1 para hallar friction points (puntos de fricción) | `[…]` |
| Sistema híbrido | Tasa de completitud autónoma, tiempo de ciclo end-to-end (de principio a fin), frecuencia de handoffs, tasa de error del agente | Handoffs frecuentes en el mismo punto, tiempo de ciclo estancado o creciente, más errores | Revisar la taxonomía, ajustar criterios de handoff, auditar el prompt (instrucciones) y los datos del agente | `[…]` |
| Negocio | Volumen por unidad de tiempo, costo por transacción, satisfacción del cliente final, ROI (retorno de la inversión) frente al equipo previo | Baja del NPS (indicador de recomendación del cliente), costos operativos en alza pese al agente, pipeline (cartera de oportunidades) estancado | Análisis de root cause (causa raíz), revisar el TO-BE, escalar a la junta de gobierno agentic | `[…]` |

**Acciones correctivas documentadas:** `[fecha, señal detectada, acción tomada, resultado]`

## Ejemplo lleno

Equipo de soporte de Customer Success (éxito del cliente) de la empresa de software B2B (que vende a otras empresas) de la sección 2.5, con 5 personas. Nombres, niveles y valores son datos ficticios de ejemplo.

**Narrativa:** "El agente responderá los tickets de nivel 1 que ya tienen solución documentada. Ustedes se concentrarán en clientes que piensan cancelar, casos sin solución conocida y en mejorar la base de conocimiento. El agente no viene a sustituirlos, sino a amplificar su trabajo: el trabajo repetitivo pasa al agente." (La idea de amplificación y no sustitución viene del informe McKinsey citado en la sección 4.1.)

**Roles** (como en la pregunta 7 del Módulo 4, una persona puede tener dos roles):

| Persona | Roles |
|---|---|
| Laura, supervisora de soporte | Agent Owner y Quality Reviewer |
| Diego, analista senior | Workflow Designer y Change Champion |
| Marta, del área legal | Ethics Reviewer |
| Andrés, gerente de Customer Success | AI Agent Manager |

**Formación:** analistas, del nivel 1 al 2; Laura y Diego, al nivel 3, porque rediseñan el flujo y comunican el modelo.

**Resistencia detectada:** un analista reenvía al cliente las respuestas del agente sin leerlas porque "el agente siempre acierta": sobre-dependencia. Intervención: formación de nivel 2 y lista de respuestas con revisión obligatoria (por ejemplo, las que mencionan cancelación).

**Indicadores al mes 3:** capa humana, satisfacción laboral en alza. Capa sistema, tiempo de ciclo reducido. Capa negocio, el NPS bajó 8 puntos (situación de la pregunta 8 del Módulo 4). Lectura: el agente quedó atendiendo interacciones de alto valor emocional; acción: ajustar la taxonomía para devolver esas interacciones al humano y llevar el hallazgo a la junta de gobierno agentic.

## Errores comunes

- Dar solo entrenamiento técnico sin explicar el porqué del cambio: los equipos que sí reciben una narrativa clara reportan tasas de adopción 2,4 veces superiores (sección 4.4).
- Culpar al trabajador por la resistencia: las tres manifestaciones son responsabilidad del manager (sección 4.4).
- Dejar roles sin asignar "porque somos pocos": los vacíos de propiedad generan agent sprawl (proliferación desordenada de agentes) y fallos silenciosos (sección 4.5; pregunta 7 del Módulo 4).
- Medir solo las métricas del agente (velocidad, volumen, error) y no las tres capas: una mejora en una capa puede ocultar un deterioro en otra (sección 4.6; preguntas 3 y 8 del Módulo 4).
- Tratar la gestión del cambio como una nota al pie del proceso técnico, cuando en el caso Accenture fue una iniciativa estratégica (caso Accenture, Módulo 4).
