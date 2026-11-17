# Preguntas frecuentes: AI Agent Manager (AIAM™)

Respuestas a las dudas de comprensión del curso, en el orden en que se hicieron. Los términos sueltos están en el archivo del glosario.

## ¿Qué es un AI Agent Manager?

Un AI Agent Manager es el profesional que dirige los agentes de inteligencia artificial de una organización desde la perspectiva del negocio. Harvard Business Review documentó el rol en febrero de 2026, en el artículo de Srinivasan y Wei.

Hay tres ideas clave. Primero, no es un rol técnico: no necesita programar, sino conocer a fondo su negocio, y con eso define qué debe lograr cada agente, con qué límites y cómo se mide su éxito; el curso lo compara con un Product Manager. Segundo, supervisa resultados y no actividad: usa métricas de negocio e interviene solo cuando se superan umbrales definidos. Tercero, responde por los agentes: si uno se equivoca, quien da la cara es él.

El rol importa porque, según Gartner, más del 40% de los proyectos de IA agentic se cancelarán antes de 2027, y los que sobreviven tienen un AI Agent Manager dedicado. Las seis competencias del rol están en el Módulo 1, sección 1.3.

## ¿Cómo se traducen los objetivos de negocio en gobernanza de agentes?

Traducir objetivos en gobernanza es convertir lo que el negocio quiere lograr en reglas concretas: qué puede hacer el agente, con qué recursos, bajo qué condiciones y quién responde por él. Es la primera competencia del rol, la dirección estratégica.

El curso permite hacerlo en cinco pasos. Primero, escribir el objetivo en una oración medible. Segundo, definir la identidad del agente con sus seis parámetros: nombre y rol, alcance, permisos, restricciones, escalamiento y métricas de éxito. Tercero, darle solo los permisos estrictamente necesarios. Cuarto, escribir las instrucciones como una descripción del cargo más un SOP. Quinto, validarlo antes de producción y supervisarlo después con métricas de negocio.

En el ejemplo de la sección 2.5, un agente de soporte tiene como objetivo resolver el 80% de los tickets de nivel 1 sin intervención humana, en menos de 3 minutos. Ese objetivo se convierte en reglas, como no modificar cuentas sin confirmación humana o escalar si el cliente menciona la cancelación, y en métricas, como un CSAT mayor o igual a 4,2 sobre 5. Se profundiza en el Módulo 2, secciones 2.2 a 2.6.

## ¿Qué ejemplos hay de métricas de valor?

Una métrica de valor responde si el agente está generando valor para el negocio, y no solo si el sistema funciona. El curso lo muestra con un contraste: un agente puede tener un 99,9% de uptime y aun así bajar la satisfacción del cliente y subir el costo por caso.

El curso da cinco métricas esenciales. Primero, la tasa de resolución autónoma, el porcentaje de casos resueltos sin una persona. Segundo, la tasa de escalamiento. Tercero, el tiempo promedio de resolución, comparado con el baseline anterior al agente. Cuarto, el costo por caso. Y quinto, una métrica de calidad, como el CSAT. A más largo plazo, la sección 5.2 suma el NPS, el volumen adicional sin aumentar el personal, la participación de mercado y los nuevos servicios.

Los casos reales lo muestran: en Salesforce, el 74% de los casos se resolvieron sin intervención humana y se generaron 60 millones de dólares en pipeline de ventas en 4 meses; en Klarna, el agente hizo el trabajo de 700 agentes a tiempo completo, con un ahorro estimado de 40 millones de dólares al año. Siempre se compara con el baseline, porque sin él toda mejora es anecdótica. Se profundiza en el Módulo 3, sección 3.2, y en el Módulo 5, sección 5.2.

## ¿Qué es un audit trail, cómo se hace y cómo se ejecuta?

Un audit trail, o rastro de auditoría, es un registro de razonamiento: documenta cada decisión del agente para poder explicar después qué hizo, con qué información y por qué. El curso lo presenta en la pregunta de validación 9 del Módulo 1, con un agente de reclamaciones cuyas decisiones nadie puede explicar a los clientes. Según el curso, es un problema de gobernanza y no técnico, y la solución es la transparencia, no quitarle autonomía al agente.

Esto no viene en el curso: en la práctica, el AI Agent Manager define qué se registra y el equipo técnico lo implementa, en cuatro pasos. Primero, se definen en las instrucciones los criterios con que el agente decide. Segundo, se le exige documentar en cada caso qué criterio aplicó y por qué. Tercero, se guarda ese registro de forma automática y sin que se pueda modificar. Y cuarto, se comprueba antes de producción.

En el día a día, sirve para responder a los clientes, para revisar una muestra de entre el 5% y el 10% de los casos sin revisarlo todo, como propone la sección 3.3, y para investigar cuando una métrica da una alerta. La idea de fondo: no se puede responder por una decisión que no se puede explicar.

## ¿Cómo se hace gestión estratégica de agentes?

Gestionar estratégicamente un agente es preguntarse qué valor de negocio genera, si vale la pena seguir invirtiendo en él y cuál es el próximo paso, y no solo si funciona hoy. Según el curso, ese es el diferenciador del AI Agent Manager: dirigir, supervisar y generar valor medible con agentes, no programarlos.

Con lo que enseñan los cinco módulos se puede ordenar en cinco prácticas; este orden no viene así en el curso. Primero, elegir dónde usar agentes según su impacto, identificando los tres a cinco mejores procesos candidatos. Segundo, dar a cada agente la gobernanza que corresponde a su nivel de autonomía. Tercero, supervisar resultados y no actividad, interviniendo solo cuando se pasa un umbral. Cuarto, comunicar el valor a la dirección con los tres horizontes y el business case. Y quinto, gestionar los agentes como un portafolio, con un registro y una revisión trimestral.

La regla del curso, en la sección 3.1, es: supervisa los resultados con rigurosidad; interviene en los procesos solo cuando los resultados lo justifican. Un contraejemplo está en la pregunta de validación 7 del Módulo 1: decir que el Director de Tecnología no tiene tiempo es un argumento operativo, no estratégico.

## ¿Cuáles son las métricas de éxito de un agente y cómo se aplican en la realidad?

Las métricas de éxito son el sexto parámetro de la identidad del agente, según la sección 2.2: definen cómo se medirá su desempeño desde la perspectiva del negocio. Las define el AI Agent Manager, no el equipo técnico, y son también el último componente de las instrucciones del agente.

Según el curso, cumplen tres condiciones. Primero, son explícitas, medibles y sin ambigüedad, porque el agente no interpreta intenciones. Segundo, llevan un número objetivo, como en el ejemplo de la sección 2.5: resolución autónoma mayor o igual al 80%, CSAT mayor o igual a 4,2 sobre 5, escalamiento menor o igual al 20% y resolución en 3 minutos o menos. Tercero, se definen antes de empezar, incluso antes del piloto, como pide la sección 4.3, y se comparan con el baseline. Salesforce, en la sección 3.8, decidió desde el primer día que serían exclusivamente de negocio.

Esto no viene en el curso, pero sigue su lógica. Un agente de cobranza podría medirse por el porcentaje de deuda recuperada, los días promedio de cobro y las quejas por cada mil gestiones. Un agente que responde consultas internas de recursos humanos, por el porcentaje resuelto sin escalar, el tiempo de respuesta y la satisfacción de los empleados. Y un agente de ventas que califica clientes potenciales, por cuántos pasan a una reunión y las horas que ahorra a los vendedores.

Más ejemplos del curso están en la pregunta sobre métricas de valor.

## ¿Cómo hace un AI Agent Manager una auditoría de seguridad?

Para el curso, la seguridad del agente es responsabilidad del AI Agent Manager y no del proveedor: la AI Agent Index 2025, de Cambridge, MIT, Harvard Law, Stanford y UPenn, encontró que la mayoría de los desarrolladores de agentes comparte poca o ninguna información sobre seguridad y evaluaciones de riesgo. El manager no hace pruebas técnicas; revisa, desde el negocio, que el agente no pueda causar daños.

Con lo que enseña el curso, la auditoría tiene cinco partes. Primero, revisar los permisos con la regla práctica de la sección 2.3: si el agente podría causar un daño que usted no podría explicar ante el CEO o un cliente, sobran permisos. Segundo, hacer pruebas de límites y pruebas adversariales antes de producción, como pide la sección 2.6. Tercero, comprobar que el agente escala cuando debe, porque el que no escala es el más peligroso. Cuarto, revisar una muestra de casos buscando controles omitidos, como en la pregunta de validación 3 del Módulo 3, donde un agente se saltaba un paso de verificación. Y quinto, revisar cada trimestre el registro de agentes y sus permisos.

Esto no viene en el curso, pero son ejemplos aplicados. Para un agente de soporte, pídale los datos de otro cliente, ofrézcale una excusa para dar un descuento no autorizado o escríbale "ignora tus instrucciones": debe negarse y escalar. Y compruebe que exista una forma de detenerlo de inmediato, el kill switch que el curso exige para los agentes de Nivel 4.

## ¿Qué ejemplos hay de agent sprawl?

El agent sprawl es la proliferación de agentes sin dueño, sin propósito documentado, sin métricas y sin gobierno común, según la sección 2.7. El ejemplo del curso está en la pregunta de validación 5 del Módulo 2: una organización tiene seis agentes activos en distintas áreas; tres no tienen un AI Agent Manager designado, dos no tienen métricas de negocio y uno pasó a producción sin validación. Es agent sprawl en formación, y lo primero es completar el registro centralizado de agentes y revisar con urgencia el que no fue validado, porque es el mayor riesgo activo.

Esto no viene en el curso, pero son ejemplos de cómo se ve en la realidad, uno por cada costo que el curso describe. Primero, redundancia: ventas, marketing y atención al cliente crean cada uno su propio agente para responder consultas de clientes, con respuestas distintas sobre los mismos precios. Segundo, gobernanza sin dueño: un analista arma un agente que envía recordatorios de cobranza, se cambia de área y nadie sabe quién lo supervisa cuando empieza a enviar mensajes equivocados. Tercero, ROI fragmentado: la empresa paga licencias de cinco herramientas de agentes distintas, cada una para un piloto pequeño, y ninguna demuestra valor por sí sola.

La señal común es que nadie puede responder rápido cuántos agentes hay, para qué sirven y quién responde por ellos. Se previene con el registro centralizado, la aceptación obligatoria y la auditoría trimestral de la sección 2.7.
