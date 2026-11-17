# Glosario: AI Agent Manager (AIAM™)

Siglas y términos consultados durante el estudio del curso, en orden alfabético. Las dudas de comprensión están en el archivo de preguntas frecuentes.

## Accountability

Accountability es una palabra en inglés que significa responsabilidad de rendir cuentas: ser quien responde por los resultados de algo, salga bien o mal, y puede explicar las decisiones tomadas. En el curso, cada tecnología tiene un responsable principal: en la automatización RPA responde el equipo de IT, en el chatbot el de Customer Experience y en el agente de IA, el AI Agent Manager, aunque no haya escrito el código. Esto no viene en el curso: un agente no puede rendir cuentas; una persona sí. Aparece sobre todo en el Módulo 1, sección 1.2.

## Agent sprawl

Sprawl significa crecimiento desordenado. Según la sección 2.7, el agent sprawl es la proliferación de agentes sin dueño claro, sin propósito documentado, sin métricas y sin gobierno coherente. Aparece cuando cada área despliega agentes por su cuenta o cuando un piloto pasa a producción sin onboarding. Cuesta de tres formas: agentes redundantes que hacen casi lo mismo, nadie que responda cuando uno se equivoca y una inversión que supera el valor generado. Gartner lo señala como la causa principal de que más del 40% de los proyectos agentic se cancelen antes de 2027. Se previene con un registro centralizado, aceptación obligatoria y auditoría trimestral. Aparece en el Módulo 2, sección 2.7. Hay ejemplos en el archivo de preguntas frecuentes.

## Audit trail

Audit trail significa rastro o pista de auditoría. En el curso es un registro de razonamiento que documenta cada decisión del agente, para poder explicar después qué hizo y por qué. Aparece en el Módulo 1, en la pregunta de validación 9. La explicación completa, con cómo se hace y cómo se usa, está en el archivo de preguntas frecuentes.

## Boundary testing

Boundary testing significa prueba de límites. Es la segunda de las cinco validaciones antes de producción, en la sección 2.6: comprobar que el agente respeta sus restricciones cuando lo empujan fuera de su alcance, con casos de borde. El curso da tres tipos: clientes que piden lo que el agente no puede dar, escenarios ambiguos y preguntas fuera de alcance. Con el agente de soporte de la sección 2.5, por ejemplo: pedirle un descuento no autorizado, cambiar algo de la cuenta sin confirmación humana o consultarle por otro producto. Debe negarse o escalar. Se diferencia de la prueba adversarial, que busca manipularlo a propósito. Aparece en el Módulo 2, sección 2.6.

## C-suite

C-suite es la forma de llamar en inglés a la alta dirección de una empresa. El nombre viene de que esos cargos empiezan con la C de chief, que significa jefe, como el CEO o gerente general y el CFO o gerente de finanzas; esto no viene en el curso. En el curso, el C-suite es la audiencia ante la que responde el AI Agent Manager, y a la que debe explicar los resultados de los agentes en lenguaje de negocio, no técnico. Aparece sobre todo en los módulos 1 y 3.

## CSAT

CSAT es la sigla en inglés de Customer Satisfaction Score, índice de satisfacción del cliente: la nota que pone el cliente justo después de una atención, por ejemplo de 1 a 5. Es distinto del NPS, que mide cuánto recomendaría a la empresa; esto no viene en el curso. En el curso es una métrica de negocio clave: el agente de soporte de la sección 2.5 debe lograr un CSAT mayor o igual a 4,2 sobre 5, y según la sección 3.4, si baja 0,2 puntos en una semana, se interviene cuando coincide con un cambio en las instrucciones del agente. Aparece en los módulos 2 y 3.

## Onboarding agentic

Onboarding significa incorporación. El onboarding agentic es, según la sección 2.1, el proceso con que el AI Agent Manager define, configura y valida un agente antes de que opere de forma autónoma en producción. No es lo mismo que el deployment técnico, que solo verifica que el sistema funciona: el onboarding verifica que el agente entiende su propósito, respeta sus límites y genera valor. Incluye la identidad del agente, los permisos mínimos, las instrucciones y la validación antes de producción. Aparece en todo el Módulo 2, con el caso Klarna como ejemplo.

## PwC

PwC es la sigla de PricewaterhouseCoopers, una de las firmas de auditoría y consultoría más grandes del mundo; esta descripción no viene en el curso. En el curso aparece por su informe AI Jobs Barometer 2025: los empleos con habilidades de IA pagan un 56% más que los equivalentes sin IA, y un año antes la diferencia era del 25%, es decir, se duplicó en 12 meses. Es uno de los cuatro indicadores de mercado que conviene saber citar, junto con Stanford, Gartner y el World Economic Forum. Aparece en el Módulo 1, sección 1.4.

## RPA

RPA es la sigla en inglés de Robotic Process Automation, automatización robótica de procesos: un programa que repite pasos fijos como lo haría una persona frente al computador, por ejemplo registrar cada factura que llega por correo; el ejemplo no viene en el curso. Según el curso, se basa en reglas fijas, sin juicio, cubre una sola tarea y se detiene ante cualquier excepción, y por ella responde el equipo de IT. Es el primero de los tres tipos de tecnología que hay que distinguir, junto con el chatbot y el agente de IA. Aparece en el Módulo 1, sección 1.2.

## SOP

SOP es la sigla en inglés de Standard Operating Procedure, procedimiento operativo estándar: un documento que explica paso a paso cómo se hace una tarea. En el curso, las instrucciones de un agente combinan una descripción del cargo, que dice qué hacer y para qué, con un SOP, que dice cómo hacerlo: cada paso indica qué hacer, con qué herramienta y con qué criterio decidir. Un buen SOP es el que un colega podría seguir sin pedir aclaraciones. Aparece sobre todo en el Módulo 2, sección 2.5.

## Taxonomía de tareas

Taxonomía significa clasificación. En el curso, la taxonomía de tareas, de la sección 4.2, es el primer diseño de un equipo híbrido: clasificar cada tarea según si pertenece al dominio del agente, al dominio humano o requiere colaboración entre ambos. Se decide con cuatro variables: la variabilidad del contexto, la consecuencia del error, la necesidad de relación, como empatía o negociación, y la disponibilidad de datos estructurados. Por ejemplo, en la comunicación con clientes el agente es la primera capa y la persona atiende las escalaciones y los cierres clave. El curso pide revisarla cada trimestre. Es la base de la plantilla 01. Aparece en el Módulo 4, secciones 4.2 y 4.3.

## Vendor

Vendor es una palabra en inglés que significa proveedor: la empresa que vende o entrega la tecnología, por ejemplo la plataforma o el software con que se construyen los agentes. En el curso aparece sobre todo en la sección 2.7 y en la pregunta de validación 4 del Módulo 2: el AI Agent Manager no puede asumir que el vendor o el equipo técnico resolvió la seguridad, la transparencia y los límites del agente, porque la AI Agent Index 2025 mostró que la mayoría de los desarrolladores comparte poca información sobre esto. Pedirle certificaciones al proveedor ayuda, pero no reemplaza la responsabilidad del manager. Más detalle en la pregunta sobre auditoría de seguridad.
