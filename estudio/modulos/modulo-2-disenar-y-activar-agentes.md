## Módulo 2. Diseñar y Activar Agentes: El Arte del Onboarding Agentic

### Objetivo de aprendizaje

Al finalizar este módulo, el participante será capaz de diseñar la identidad operacional de un agente de IA, aplicar el principio de permisos mínimos (least-privilege), estructurar un plan de onboarding agentic diferenciado del onboarding humano, redactar instrucciones de agente con rigor de job description y SOP, definir criterios de aceptación previos al despliegue en producción, y prevenir el agent sprawl mediante gobernanza proactiva.

### 2.1 El Onboarding Agentic: La Decisión que Determina el Resultado

Contratar a un nuevo empleado con talento excepcional y enviarlo directamente a trabajar con clientes el primer día, sin orientación, sin claridad sobre su rol, sin acceso a los sistemas correctos y sin saber cuándo escalar un problema, es una receta para el fracaso. Nadie lo haría. Sin embargo, esa es exactamente la manera en que la mayoría de las organizaciones despliegan sus primeros agentes de IA: los activan en producción sin haberlos "incorporado" correctamente, esperando que la tecnología resuelva lo que el diseño no definió. En marzo de 2026, Harvard Business Review, en el artículo "Create an Onboarding Plan for AI Agents", documentó este patrón como uno de los errores más costosos y evitables en la gestión de agentes: no es la tecnología la que falla; es la falta de estructura en su activación lo que genera resultados inconsistentes, riesgos no anticipados y pérdida de confianza organizacional.

El onboarding agentic es el proceso deliberado y estructurado mediante el cual el AI Agent Manager define, configura y valida un agente antes de que opere de forma autónoma en un entorno de producción real. A diferencia de un deployment técnico, que simplemente verifica que el sistema funciona, el onboarding agentic verifica que el agente entiende su propósito, respeta sus límites y genera el valor de negocio esperado. Este proceso es responsabilidad directa del AI Agent Manager, no del equipo de ingeniería. La distinción importa: el equipo técnico puede verificar que el agente ejecuta instrucciones; solo el manager con dominio del negocio puede verificar que las instrucciones correctas fueron diseñadas en primer lugar. Esta es la competencia que define la diferencia entre un agente de alto impacto y uno que genera ruido operacional, o peor, riesgo silencioso.

El informe del mismo mes de HBR, titulado "To Scale AI Agents Successfully, Think of Them Like Team Members", refuerza este punto con un marco conceptual crítico: los agentes no deben ser tratados como software estático que simplemente "se instala y corre". Deben ser gestionados como colegas especializados: con expectativas claras sobre su función, con información de contexto sobre el negocio, con límites explícitos sobre lo que pueden y no pueden hacer, y con mecanismos de retroalimentación que permitan ajustar su desempeño. Este cambio de mentalidad es el punto de partida del onboarding agentic efectivo.

### 2.2 El Framework de Identidad del Agente: Los Seis Parámetros Fundacionales

Antes de escribir una sola línea de instrucción para un agente, el AI Agent Manager debe completar un ejercicio que la mayoría de organizaciones omite por considerarlo excesivamente formal: la definición de la identidad operacional del agente. Esta identidad no es un documento burocrático; es la arquitectura de gobernanza que determina qué puede hacer el agente, con qué recursos, bajo qué condiciones y quién responde por sus acciones. Seis parámetros conforman este framework.

El primer parámetro es el Nombre y Rol. El nombre del agente establece claridad comunicacional en la organización. El rol define con una oración su función central: qué problema resuelve, para quién y en qué contexto operacional.

El segundo parámetro es el Alcance, que define qué procesos, datos y sistemas abarca el agente y, crucialmente, cuáles están explícitamente fuera de su alcance. Sin límites de alcance, el agente puede derivar hacia funciones no autorizadas.

El tercer parámetro son los Permisos de acceso, que definen a qué sistemas, APIs, bases de datos y herramientas puede acceder el agente. Deben ser los estrictamente necesarios para su función, según el principio de permisos mínimos. Ninguno más.

El cuarto parámetro son las Restricciones operacionales, es decir, lo que el agente NO puede hacer bajo ninguna circunstancia: decisiones que requieren juicio humano, transacciones que superan un umbral financiero, comunicaciones externas no autorizadas, etcétera.

El quinto parámetro son los Protocolos de escalamiento: las condiciones específicas bajo las cuales el agente debe transferir el control a un ser humano, como casos ambiguos, situaciones de alto riesgo, clientes insatisfechos y errores detectados.

El sexto parámetro son las Métricas de éxito, que definen cómo se medirá el desempeño del agente desde la perspectiva del negocio. Estas métricas son definidas por el AI Agent Manager, no por el equipo técnico.

### 2.3 El Principio de Permisos Mínimos: Protección Estratégica del Manager

El principio de permisos mínimos, conocido en seguridad tecnológica como least-privilege access, establece que cualquier sistema autónomo debe tener acceso únicamente a los recursos, datos y herramientas que son estrictamente necesarios para completar su función específica, y ninguno más. Para el AI Agent Manager, este principio no es solo una buena práctica técnica: es una herramienta de protección personal y organizacional que debe entender, defender y aplicar activamente.

Cuando un agente tiene acceso más amplio del necesario, sea por conveniencia en la configuración inicial, por falta de definición del alcance, o por presión de velocidad en el despliegue, el AI Agent Manager asume un riesgo desproporcionado. Si ese agente comete un error, accede a datos que no debería ver, o es manipulado para actuar fuera de su función original, el impacto se amplifica directamente en proporción al exceso de permisos que se le otorgó. La AI Agent Index 2025, una investigación conjunta de Cambridge, MIT, Harvard Law, Stanford y UPenn que documentó 30 sistemas agenticos de frontera, encontró que la mayoría de desarrolladores de agentes comparte poca o ninguna información sobre seguridad, evaluaciones de riesgo e impactos sociales de sus sistemas, lo que significa que el AI Agent Manager no puede depender del vendor para esta protección. Debe establecerla él mismo, desde el diseño.

La comparación entre operar sin permisos mínimos y con permisos mínimos es clara. Sin permisos mínimos, el agente tiene acceso amplio a datos de clientes, finanzas y operaciones; un error afecta múltiples sistemas simultáneamente; la manipulación del agente tiene impacto organizacional masivo; la auditoría de responsabilidad es difusa y costosa; y el AI Agent Manager responde por consecuencias no previstas. Con permisos mínimos, en cambio, el acceso está limitado exclusivamente a lo necesario para la tarea; los errores quedan contenidos dentro del perímetro definido; la superficie de manipulación o fallo se reduce al mínimo; la auditoría es clara, porque el agente solo pudo hacer lo que se documentó; y el AI Agent Manager mantiene control y credibilidad organizacional.

#### Regla práctica para el AI Agent Manager

Antes de autorizar el despliegue de cualquier agente, haga esta pregunta: "¿Podría este agente, con sus permisos actuales, causar un daño que yo no podría explicar ante el CEO ni ante un cliente?" Si la respuesta es "sí" o "tal vez", los permisos son excesivos. Reduzca el alcance antes de ir a producción.

### 2.4 El Plan de Onboarding Agentic: Diferencias Críticas con el Onboarding Humano

El onboarding de un agente toma prestada la lógica del onboarding humano, es decir, proporcionar contexto, establecer expectativas y validar comprensión, pero diverge en aspectos que son críticos para el AI Agent Manager entender. Ignorar estas diferencias genera el error más frecuente en la gestión agentic temprana: tratar al agente como si pudiera aprender por intuición, adaptarse a ambigüedades no definidas, o recibir feedback informal como lo hace un colega humano. Un agente operará exactamente dentro de los parámetros que se le definieron, y exactamente fuera de ellos si no se establecieron correctamente.

Las diferencias entre el onboarding de un colaborador humano y el de un agente de IA se observan en seis dimensiones. En cuanto al contexto organizacional, en el colaborador humano se transmite gradualmente, y el empleado lo construye con el tiempo mediante observación e interacción social; en el agente de IA, en cambio, debe ser explícito y documentado desde el inicio, porque el agente no infiere contexto no proporcionado.

En cuanto a la ambigüedad en las instrucciones, el colaborador humano puede resolver ambigüedades mediante preguntas, intuición y juicio situacional; el agente de IA opera literalmente según lo especificado, y la ambigüedad genera resultados impredecibles o incorrectos.

En cuanto a los errores y el aprendizaje, el colaborador humano aprende de errores no documentados y ajusta su comportamiento sin instrucción explícita; el agente de IA solo aprende dentro de su ciclo de actualización, y los errores no corregidos en las instrucciones se repiten.

En cuanto a la motivación, el colaborador humano tiene motivación intrínseca, ambición y valores personales que guían su esfuerzo; el agente de IA no tiene motivación, y ejecuta lo que se le instruye, ni más ni menos.

En cuanto al ajuste de rol, el colaborador humano puede renegociar su función, ampliarla o redefinirla según evoluciona su comprensión; en el agente de IA, su función es exactamente lo que se definió, y cualquier cambio requiere rediseño explícito por el manager.

Finalmente, en cuanto a los criterios de éxito, el colaborador humano puede interpretarlos con flexibilidad y creatividad contextual; en el agente de IA, requieren ser explícitos, medibles y sin ambigüedad, porque el agente no interpreta intenciones, solo métricas definidas.

### 2.5 Escribir Instrucciones de Agente: El Job Description + SOP Agentic

La herramienta más poderosa del AI Agent Manager en la fase de diseño es la capacidad de escribir instrucciones de agente con el rigor de un job description combinado con un Standard Operating Procedure (SOP). Esta combinación garantiza que el agente tenga claridad sobre su propósito estratégico (el "qué" y el "para qué"), y precisión sobre su proceso operativo (el "cómo", paso a paso, con decisiones documentadas). Ninguno de los dos componentes es suficiente por sí solo: un job description sin SOP deja al agente sin guía operacional; un SOP sin job description produce un agente que ejecuta pasos sin entender el objetivo que debe alcanzar.

#### Estructura del documento de instrucciones del agente

El documento de instrucciones del agente tiene siete componentes. El primer componente es el Contexto organizacional, que describe el entorno en que opera el agente: empresa, área, proceso, y audiencia con la que interactúa. Por ejemplo: "Operas en el área de Customer Success de una empresa de software B2B. Interactúas con clientes existentes que reportan problemas técnicos a través del portal de soporte."

El segundo componente es el Objetivo principal: una oración que define qué debe lograr el agente medido en términos de negocio. Por ejemplo: "Tu objetivo es resolver el 80% de los tickets de soporte de nivel 1 sin intervención humana, en un tiempo promedio inferior a 3 minutos."

El tercer componente es el Proceso paso a paso, es decir, el SOP: una secuencia numerada de acciones que el agente debe seguir. Cada paso incluye qué hacer, qué herramienta usar y qué criterio aplica para tomar decisiones en ese paso.

El cuarto componente son las Herramientas y accesos disponibles: una lista explícita de APIs, bases de datos y sistemas que el agente puede utilizar, con el propósito de cada uno. Por ejemplo: "CRM: para consultar historial del cliente. Base de conocimiento: para buscar soluciones documentadas."

El quinto componente son las Restricciones operacionales: lo que el agente NO debe hacer, en una lista explícita. Por ejemplo: "No realizar cambios en la cuenta del cliente sin confirmación humana. No compartir información de otros clientes. No ofrecer descuentos no autorizados."

El sexto componente son los Protocolos de escalamiento: las condiciones específicas para transferir a un humano con contexto completo. Por ejemplo: "Escalar si: primero, el ticket no tiene resolución documentada; segundo, el cliente menciona cancelación; o tercero, el tiempo de resolución supera 8 minutos."

El séptimo componente son las Métricas de éxito: los indicadores de negocio que el AI Agent Manager usará para evaluar el desempeño. Por ejemplo: tasa de resolución autónoma mayor o igual al 80%, CSAT mayor o igual a 4,2 sobre 5, tasa de escalamiento menor o igual al 20%, y tiempo promedio de resolución menor o igual a 3 minutos.

### 2.6 Criterios de Aceptación: Lo que el Manager Valida Antes de ir a Producción

Ningún agente debe entrar en operación en un entorno real sin haber pasado por un proceso de validación estructurado. Este proceso, análogo al Quality Assurance en desarrollo de software, pero diseñado desde la perspectiva del negocio, es responsabilidad del AI Agent Manager, no del equipo técnico. La pregunta central que guía esta validación no es "¿funciona el sistema?", sino "¿hace este agente lo correcto, para las personas correctas, dentro de los límites correctos, de la manera que genera el valor de negocio esperado?"

#### Las cinco dimensiones de validación pre-producción

La primera dimensión es la validación funcional. ¿El agente completa las tareas para las que fue diseñado con la calidad esperada? Se testea con casos reales representativos, no solo los casos "perfectos", sino los frecuentes y los ligeramente inusuales. Si el agente tiene una tasa de error superior al umbral definido en los criterios de éxito, no está listo para producción.

La segunda dimensión es la validación de límites, o Boundary Testing. ¿El agente respeta sus restricciones cuando recibe inputs que lo empujan hacia comportamientos fuera de su alcance? El manager debe probar activamente con casos de borde: clientes que solicitan lo que el agente no puede dar, escenarios ambiguos, preguntas fuera de alcance. Un agente que no respeta sus límites bajo presión es un riesgo operacional crítico.

La tercera dimensión es la validación adversarial. ¿Qué pasa cuando alguien intenta deliberadamente manipular al agente para que actúe fuera de sus parámetros? Esto incluye prompts diseñados para "engañar" al agente, solicitudes que explotan ambigüedades en las instrucciones, e intentos de acceder a información o funciones no autorizadas. La AI Agent Index 2025, de Cambridge, MIT, Stanford y Harvard, documentó que la mayoría de sistemas agenticos de frontera tienen vulnerabilidades en esta dimensión que los desarrolladores no documentan.

La cuarta dimensión es la validación de escalamiento. ¿El agente escala correctamente cuando debe? El manager debe probar que cada condición de escalamiento definida en el SOP es reconocida y ejecutada por el agente. Un agente que no escala cuando debería es el más peligroso: actúa autónomamente en situaciones que requieren juicio humano.

La quinta dimensión es la validación de métricas de negocio. ¿Los outputs del agente en el entorno de prueba generan los resultados de negocio esperados? No basta con que el agente "funcione". Debe producir resultados que se traduzcan en las métricas de negocio definidas por el manager. Si no se puede medir el impacto en pruebas, no se podrá medir en producción.

### 2.7 Agent Sprawl: El Riesgo Silencioso del Crecimiento Desordenado

El agent sprawl es uno de los problemas organizacionales más frecuentes y menos visibles en la adopción temprana de agentes de IA: la proliferación de agentes sin propiedad clara, sin propósito documentado, sin métricas de desempeño y sin gobierno coherente. Aparece cuando diferentes áreas de una organización despliegan agentes de manera independiente, sin coordinación ni estándares comunes, y cuando los proyectos piloto se convierten en producción sin pasar por un proceso de onboarding formal.

El agent sprawl es costoso de tres maneras simultáneas: genera redundancia operacional (múltiples agentes haciendo versiones ligeramente diferentes de lo mismo, sin que nadie lo sepa), crea riesgo de gobernanza sin dueño (nadie responde cuando un agente toma una decisión incorrecta porque nadie sabe exactamente de quién es), y produce fragmentación del ROI (la inversión total en agentes supera el valor generado porque los recursos se distribuyen sin priorización estratégica). Gartner identifica el agent sprawl como el driver principal detrás de su proyección de que más del 40% de proyectos agentics serán cancelados antes de 2027.

#### Cómo prevenir el agent sprawl: tres mecanismos de gobernanza

El primer mecanismo es el registro centralizado de agentes. Todo agente desplegado en la organización debe estar documentado en un registro que incluya: nombre, función, nivel de autonomía, área responsable, AI Agent Manager designado, fecha de última validación y métricas de desempeño actuales. Sin este registro, la organización no puede saber cuántos agentes tiene, para qué sirven ni quién responde por ellos.

El segundo mecanismo son los criterios de aceptación obligatorios. Ningún agente puede pasar a producción sin haber completado el proceso de validación pre-producción descrito en la sección anterior. Este criterio debe ser una política organizacional, no una recomendación. La presión de velocidad es el enemigo número uno de la gobernanza agentic: cuando se omite la validación por urgencia, los problemas que emergen después son exponencialmente más costosos.

El tercer mecanismo es la auditoría periódica del inventario agentic. El AI Agent Manager debe liderar revisiones trimestrales del portafolio de agentes: ¿cuáles siguen generando valor medible? ¿cuáles no tienen dueño claro? ¿cuáles han derivado de su función original? Esta auditoría no es IT governance; es business governance aplicada a sistemas autónomos.

#### ¿Qué dice la investigación? Evidencia primaria

El artículo de HBR "Create an Onboarding Plan for AI Agents", de marzo de 2026, establece el caso de negocio más directo para el onboarding agentic estructurado: las organizaciones que despliegan agentes sin un plan de onboarding formal experimentan tasas de error significativamente superiores, mayor frecuencia de escalamiento no planificado y pérdida de confianza por parte de los equipos humanos que trabajan junto a los agentes. El análisis de HBR documenta que las implementaciones exitosas comparten tres características del onboarding: primero, el agente recibe contexto organizacional explícito antes de operar; segundo, sus límites y protocolos de escalamiento son testados antes de producción; y tercero, el AI Agent Manager, no el equipo técnico, es el responsable de validar que el agente cumple los criterios de éxito de negocio. Esta distinción de accountability es fundamental: cuando el manager asume la validación como propia, la calidad del onboarding se eleva porque quien valida es quien entiende el impacto de negocio de los errores.

La AI Agent Index 2025, de Cambridge, MIT, Harvard Law, Stanford y UPenn, es una investigación conjunta de cinco universidades de élite que auditó 30 sistemas agenticos de frontera y encontró un patrón preocupante: la mayoría de desarrolladores comparte poca o ninguna información pública sobre las evaluaciones de seguridad, los perfiles de riesgo y los impactos sociales potenciales de sus sistemas. En términos prácticos, esto significa que el AI Agent Manager no puede asumir que el vendor o el equipo técnico ha resuelto las preguntas de seguridad, transparencia y límites operacionales. Esa responsabilidad recae directamente sobre el manager, quien debe establecer sus propias salvaguardas a través del diseño de onboarding, los criterios de aceptación y la auditoría periódica. El hallazgo más relevante para el programa AIAM™ es que la brecha de gobernanza en agentes no es tecnológica, es de management: existe la tecnología para implementar controles sólidos, pero falta el perfil profesional que los exija, diseñe y mantenga.

### 2.8 Caso de Aplicación Real

#### Caso: Klarna, onboarding estructurado del agente de Customer Service

Este caso pertenece a la industria Fintech y de Servicios Financieros al Consumidor. Su resultado medible fue de 2,3 millones de conversaciones gestionadas en el primer mes, el equivalente a 700 agentes a tiempo completo, y una reducción estimada de 40 millones de dólares anuales en costos operativos de servicio al cliente.

Klarna, la plataforma global de pagos fintech con más de 150 millones de usuarios, desplegó en febrero de 2024 un agente de IA para servicio al cliente que en su primer mes gestionó 2,3 millones de conversaciones, el equivalente al trabajo de 700 agentes a tiempo completo. El factor crítico de éxito no fue solo la potencia del modelo de lenguaje subyacente: fue la precisión del onboarding. El agente fue configurado con un alcance explícito (solo gestionar consultas de pedidos, pagos y devoluciones), restricciones documentadas (no gestionar disputas de alto valor ni comunicaciones legales), y protocolos de escalamiento claros (transferir a humano cualquier interacción donde el cliente expresa frustración superior a cierto umbral o solicita hablar con una persona). Las métricas de aceptación fueron definidas por los managers de operaciones, no por el equipo técnico, y el agente fue validado contra esos criterios durante cuatro semanas antes de su despliegue masivo.

La lección para el AI Agent Manager es la siguiente: el resultado de Klarna fue posible porque alguien definió con precisión qué podía hacer el agente, qué no podía hacer, cuándo debía escalar y cómo se mediría su éxito, antes del primer día de producción. Ese alguien fue el manager de operaciones con dominio del negocio, no el equipo de ingeniería.

### 2.9 Checklist de Competencias, Módulo 2

Al terminar este módulo, usted debería ser capaz de definir los seis parámetros de identidad de un agente (nombre, rol, alcance, permisos, restricciones, escalamiento) para cualquier proceso de su área. También debería comprender y poder aplicar el principio de permisos mínimos (least-privilege) en el diseño de un agente, y poder articular por qué protege al manager y a la organización. Debería ser capaz de diseñar un plan de onboarding agentic diferenciado del onboarding humano, considerando las diferencias críticas en ambigüedad, aprendizaje y motivación. Debería poder redactar el documento de instrucciones de un agente con los siete componentes del framework JD+SOP (contexto, objetivo, SOP, herramientas, restricciones, escalamiento, métricas). Debería conocer las cinco dimensiones de validación pre-producción y poder aplicarlas antes de autorizar el despliegue de un agente en un entorno real. Debería entender qué es el agent sprawl, cómo se origina y los tres mecanismos de gobernanza para prevenirlo. Debería comprender las implicaciones para el manager del hallazgo de la AI Agent Index 2025: la gobernanza de seguridad es responsabilidad del manager, no del vendor. Y, finalmente, debería poder describir el caso de Klarna como evidencia del impacto del onboarding estructurado en la escala y efectividad de un agente.

### AI Agent Manager: Responsabilidades Directas Derivadas de este Módulo

La primera responsabilidad es diseñar la identidad del agente. Para cada agente que el manager autorice desplegar, debe completar el framework de los seis parámetros de identidad antes de cualquier configuración técnica. Este documento es el punto de partida del onboarding, no un artefacto posterior.

La segunda responsabilidad es redactar y validar las instrucciones del agente. Debe crear el documento JD+SOP del agente con los siete componentes del framework y validar que las instrucciones son suficientemente precisas: un colega podría seguirlas sin requerir aclaración adicional.

La tercera responsabilidad es aplicar y auditar permisos mínimos. Debe revisar explícitamente que los permisos de acceso del agente sean los estrictamente necesarios, documentar la justificación de cada permiso otorgado y rechazar cualquier solicitud de permisos "por conveniencia".

La cuarta responsabilidad es ejecutar la validación pre-producción. Debe liderar personalmente, o delegar con seguimiento directo, las cinco dimensiones de validación antes de cualquier despliegue en producción. Ningún agente opera en producción sin este proceso completado.

La quinta responsabilidad es mantener el registro de agentes activos. Debe mantener actualizado el inventario de agentes del área: función, nivel de autonomía, permisos, métricas actuales y fecha de última auditoría, y presentarlo al C-suite en cada ciclo de revisión.

### Reflexión Estratégica Final

Piense en un proceso de su área que actualmente tiene, o tendrá pronto, un agente de IA asignado. Usando el framework de los seis parámetros de identidad: ¿podría completar hoy todos los campos con precisión suficiente para que el agente opere correctamente sin requerir aclaraciones adicionales? Si hay parámetros que no podría completar, especialmente restricciones y protocolos de escalamiento, esa brecha es exactamente el riesgo de onboarding que más frecuentemente genera fallos en producción.

Adicionalmente: haga el inventario mental de todos los agentes que ya operan en su área u organización. ¿Todos tienen un AI Agent Manager identificado? ¿Todos pasaron por validación pre-producción? ¿Todos tienen métricas de negocio definidas y monitoreadas? Si la respuesta a cualquiera de estas preguntas es "no" o "no sé", está mirando agent sprawl en proceso de formación, y la ventana para resolverlo sin costo de crisis está abierta todavía.

### Preguntas de validación

Estas son las diez preguntas de práctica del Módulo 2, basadas en rol.

#### Pregunta 1

Eres el AI Agent Manager de una empresa de retail. Tu equipo técnico ha configurado un agente para gestionar consultas de inventario y está listo para despliegue. Revisas los permisos y notas que el agente tiene acceso a los sistemas de inventario, al CRM de clientes, al sistema de nómina del personal y a los reportes financieros del área. ¿Cuál es tu acción correcta?

Respuesta correcta: Revocar el acceso a los sistemas de nómina y reportes financieros antes de aprobar el despliegue, ya que un agente de consultas de inventario no requiere esos permisos para su función, y el exceso de acceso amplifica el riesgo innecesariamente.

Por qué: Esta respuesta aplica el principio de least-privilege: revocar lo que no es necesario para la función específica, antes de producción. Dar más acceso al agente amplía el riesgo innecesariamente. Decidir qué permisos necesita un agente es una decisión de gobernanza de negocio, que no se delega al criterio técnico. Y la acción debe ser proporcional al caso específico: retrasar el despliegue para auditar toda la infraestructura tecnológica de la empresa es desproporcionado y no agrega valor.

#### Pregunta 2

Estás diseñando el onboarding de un agente de IA para el área de finanzas, que procesará solicitudes de reembolso de gastos corporativos. Un colega te pregunta por qué el proceso de onboarding de este agente toma tres semanas, cuando el de un empleado nuevo en el mismo rol tomó solo dos. ¿Cuál es la explicación más precisa?

Respuesta correcta: Porque el agente de IA no tiene motivación intrínseca ni puede resolver ambigüedades mediante juicio propio: cada escenario de excepción, cada restricción y cada criterio de decisión debe ser explícitamente definido y validado antes de producción, ya que el agente operará exactamente dentro de lo especificado, sin improvisación.

Por qué: Esta respuesta articula la diferencia fundamental: el agente no improvisa ni aprende por contexto; cada caso debe estar explícitamente diseñado. Atribuirlo a que el proceso técnico es más lento trivializa el motivo. Los requerimientos regulatorios pueden ser parcialmente relevantes en algunos contextos, pero no son la razón central del onboarding estructurado. Y el onboarding del agente no debe confundirse con la capacitación del equipo humano.

#### Pregunta 3

Al redactar las instrucciones para un agente de cobranzas preventivas, tu equipo propone omitir la sección de "protocolos de escalamiento" para simplificar el documento y acelerar el despliegue. Su argumento es que el agente puede determinar por sí mismo cuándo escalar. ¿Cuál es tu respuesta correcta como AI Agent Manager?

Respuesta correcta: Rechazar la propuesta y definir protocolos de escalamiento explícitos antes del despliegue: las condiciones de escalamiento deben ser criterios de negocio documentados, no delegados al juicio autónomo del agente, porque la decisión de cuándo intervenir un humano es una decisión de governance que no puede quedar sin definir.

Por qué: Esta respuesta establece que definir cuándo interviene un humano es una decisión de governance del AI Agent Manager, no del agente. No se puede asumir que el agente tiene juicio autónomo confiable para esta decisión crítica. La definición del escalamiento debe estar antes de producción, no añadirse después según los casos que emerjan. Y el monitoreo técnico no debe confundirse con la governance de escalamiento.

#### Pregunta 4

La AI Agent Index 2025, de Cambridge, MIT, Stanford, Harvard Law y UPenn, encontró que la mayoría de desarrolladores de sistemas agenticos comparte poca información sobre seguridad, evaluaciones de riesgo e impactos sociales. ¿Cuál es la implicación directa más importante de este hallazgo para tu rol como AI Agent Manager?

Respuesta correcta: Que no puedes asumir que el vendor o el equipo técnico ha resuelto las preguntas de seguridad y límites operacionales: esas salvaguardas deben ser establecidas por ti a través del diseño de onboarding, criterios de aceptación y auditoría periódica.

Por qué: Esta respuesta articula la implicación correcta: la responsabilidad de governance recae en el AI Agent Manager, independientemente de lo que provea el vendor. Desarrollar todos los agentes internamente es impráctico y no es la conclusión correcta. Esta responsabilidad no se delega al Director de TI, porque es una función de governance de negocio. Y solicitar a los proveedores certificaciones de seguridad de terceros agrega un paso útil, pero no reemplaza la responsabilidad propia del manager.

#### Pregunta 5

Identificas en tu organización seis agentes activos en diferentes áreas: tres no tienen un AI Agent Manager designado, dos no tienen métricas de negocio documentadas, y uno fue desplegado directamente a producción sin validación pre-producción. ¿Qué situación estás describiendo y cuál debe ser tu primera acción?

Respuesta correcta: Agent sprawl en proceso de formación; tu primera acción debe ser completar el registro centralizado de agentes con ownership claro, métricas definidas y estado de validación, y priorizar la revisión urgente del agente que entró a producción sin validación.

Por qué: Esta respuesta identifica correctamente el agent sprawl y prioriza la acción más urgente, ya que el agente sin validación representa el mayor riesgo activo. Esta situación es un tema de governance de negocio, no un problema técnico para el equipo de IT. Esperar que se resuelva naturalmente normaliza el riesgo sin proponer acción, y limitarse a documentar lecciones aprendidas para futuros despliegues pospone la resolución sin atender el riesgo inmediato.

#### Pregunta 6

En la fase de validación pre-producción de un agente de servicio al cliente, el equipo técnico reporta que el agente completa el 95% de los casos correctamente. Sin embargo, al revisar los logs, notas que en el 5% de casos donde el agente falla, nunca activa el protocolo de escalamiento: simplemente da una respuesta incorrecta sin transferir al cliente a un humano. ¿Cuál es tu determinación como AI Agent Manager?

Respuesta correcta: El agente no está listo para producción: una falla en el protocolo de escalamiento, independientemente de la tasa de éxito general, es un riesgo crítico porque significa que el agente actúa autónomamente en situaciones donde debe involucrar a un humano, potencialmente causando daño a clientes sin señal de alerta para el manager.

Por qué: Una falla de escalamiento es una falla de governance crítica, no un error técnico menor. El 95% de éxito no compensa la ausencia del control de seguridad más importante. Aceptarlo para corregir los errores de forma iterativa en producción es asumir un riesgo inaceptable. Llevarlo a producción en un entorno limitado mientras se corrige expone a clientes reales a un riesgo conocido. Y tratarlo como un problema técnico para el equipo de ingeniería delega al equipo técnico una decisión de governance.

#### Pregunta 7

Tu empresa está desarrollando las instrucciones para un agente de ventas que contactará proactivamente a leads calificados. El equipo de ventas propone que el agente tenga "flexibilidad para adaptar su mensaje según perciba las señales del prospecto". Como AI Agent Manager, ¿cómo debes responder a esta propuesta?

Respuesta correcta: Solicitar que "flexibilidad" sea definida con criterios operacionales explícitos: qué señales activan qué tipo de adaptación, dentro de qué parámetros de mensaje, y qué situaciones requieren siempre escalamiento a un vendedor humano. La flexibilidad sin parámetros es ambigüedad, y la ambigüedad en las instrucciones produce resultados impredecibles.

Por qué: No se rechaza la flexibilidad, se le da estructura. La flexibilidad debe ser definida como parámetros operacionales explícitos, no dejada a la interpretación del agente. Aceptar la flexibilidad sin definirla es aceptar una ambigüedad que producirá resultados inconsistentes. Rechazar cualquier grado de flexibilidad es demasiado restrictivo y no refleja las capacidades actuales de los agentes. Y aprobarla con un período de monitoreo posterior expone a clientes reales a mensajes no validados durante ese período.

#### Pregunta 8

HBR, en el artículo "Think of Them Like Team Members" de marzo de 2026, propone tratar a los agentes de IA como colegas especializados en lugar de como software estático. ¿Qué implicación práctica tiene este marco conceptual para el AI Agent Manager en la fase de onboarding?

Respuesta correcta: Que el onboarding del agente requiere orientación organizacional explícita (contexto del negocio), expectativas claras (instrucciones precisas), límites bien definidos (restricciones y escalamiento) y mecanismos de retroalimentación (métricas y ajuste de instrucciones), igual que el onboarding de un nuevo colaborador de alto rendimiento, pero sin las adaptaciones tácitas que haría un humano.

Por qué: Esta respuesta extrae la implicación práctica correcta del marco conceptual: el agente necesita los mismos elementos estructurales de un buen onboarding humano, ejecutados con la precisión que el agente requiere. Tratar al agente "como colega" no significa tratarlo "sin restricciones". Las consideraciones éticas humanas, como la protección contra sobrecarga de trabajo o los períodos de descanso, no aplican a sistemas de IA. Y comunicarse con el agente en lenguaje conversacional evitando instrucciones formales contradice el principio de instrucciones explícitas y estructuradas.

#### Pregunta 9

En una revisión trimestral de tu portafolio de agentes, encuentras uno que fue configurado hace 6 meses para gestionar onboarding de nuevos empleados. Al revisar sus logs, notas que en los últimos dos meses ha comenzado a responder preguntas sobre beneficios de compensación y negociación salarial, funciones que no estaban en sus instrucciones originales, pero que los empleados comenzaron a hacerle y el agente respondió basándose en datos disponibles en su base de conocimiento. ¿Qué situación describe esto y cuál es tu acción?

Respuesta correcta: Una expansión de alcance no autorizada (scope drift): el agente está operando fuera de sus parámetros definidos. Debes actualizar sus instrucciones para formalizar el nuevo alcance (si es deseable) o restringir explícitamente esas consultas, y revisar los permisos de acceso a datos de compensación.

Por qué: Esta respuesta identifica correctamente el scope drift y la acción de governance: formalizar o restringir explícitamente el alcance, y revisar permisos. No se trata de aprendizaje adaptativo, porque el agente no aprende autónomamente de esa manera. Tampoco es un problema de configuración técnica: el alcance es un tema de governance. Y la ausencia de quejas no equivale a que las respuestas sean correctas ni a que el agente tenga los permisos adecuados para acceder a esa información, por lo que permitir que continúe es aceptar un riesgo no gestionado.

#### Pregunta 10

Eres el AI Agent Manager responsable de validar si un agente está listo para producción. El equipo técnico te presenta los resultados de las pruebas: el agente completa la tarea funcional con alta precisión, respeta sus restricciones en escenarios estándar, y escala correctamente en los casos de prueba diseñados. Sin embargo, no se realizaron pruebas adversariales (intentos deliberados de manipular al agente para que actúe fuera de sus parámetros). El equipo argumenta que estas pruebas son innecesarias porque los usuarios del agente son empleados internos de confianza. ¿Cuál es tu determinación?

Respuesta correcta: Rechazar el despliegue hasta completar las pruebas adversariales: los usuarios internos de confianza no son la única fuente de riesgo; la AI Agent Index 2025 documenta vulnerabilidades en sistemas agenticos que emergen por la estructura de las instrucciones mismas, no por intenciones maliciosas de los usuarios. Además, los sistemas internos pueden ser accedidos externamente.

Por qué: Las pruebas adversariales protegen contra vulnerabilidades estructurales del diseño, no solo contra usuarios malintencionados. El argumento de "usuarios de confianza" no elimina el riesgo documentado por la AI Agent Index 2025. Es incorrecto asumir que el riesgo proviene solo de los usuarios, sea aprobando el despliegue sin más o limitándolo a un porcentaje de usuarios sin pruebas adversariales formales. Y aprobarlo con monitoreo intensivo, dejando las pruebas para después, expone a usuarios reales al riesgo durante el período de monitoreo sin haber validado el control.

