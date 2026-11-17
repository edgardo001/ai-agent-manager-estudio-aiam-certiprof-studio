# Diagramas: AI Agent Manager (AIAM™)

Diagramas en formato Mermaid sobre los temas del curso, agregados a pedido, en el orden en que se piden. GitHub y la mayoría de los editores de Markdown los muestran dibujados; en un editor de texto plano se ve el código.

Cada diagrama indica de qué módulo y sección sale. Todo su contenido viene del curso, salvo lo que se marca explícitamente.

## Qué debe tener un sistema agentic, visto como un flujo de n8n

Muestra las piezas que el curso exige a un agente, ordenadas como si fuera un flujo de n8n, con el ejemplo del agente de soporte técnico de la sección 2.5. Sale sobre todo del Módulo 2 (secciones 2.2 a 2.7) y del Módulo 3 (secciones 3.2 a 3.5). La forma de flujo de n8n y los nombres de sus nodos no vienen en el curso: son una analogía para entenderlo.

```mermaid
flowchart TD
    subgraph DISENO["1 · Antes de activar: onboarding agentic, Módulo 2"]
        ID["Identidad del agente<br/>nombre y rol · alcance"]
        PERM["Permisos mínimos<br/>solo CRM y base de conocimiento"]
        INST["Instrucciones = descripción del cargo + SOP<br/>objetivo: 80% de tickets nivel 1 sin humano, en menos de 3 min"]
        VAL{{"Validación: 5 filtros<br/>funcional · límites · adversarial<br/>escalamiento · métricas de negocio"}}
        REG[("Registro centralizado de agentes")]
        ID --> PERM --> INST --> VAL
        VAL -- "aprueba" --> REG
        VAL -. "no aprueba: corregir" .-> INST
    end

    subgraph FLUJO["2 · Cada caso en producción: el flujo tipo n8n"]
        T(["Disparador<br/>llega un ticket del cliente"])
        A["Nodo agente de IA<br/>decide en varios pasos"]
        H1[["Herramienta: CRM"]]
        H2[["Herramienta: base de conocimiento"]]
        R{{"Restricciones<br/>¿cambiar la cuenta, datos de otro cliente, descuento?"}}
        E{{"Escalamiento<br/>¿sin solución, menciona cancelar, más de 8 min?"}}
        HUM["Traspaso a una persona<br/>con el contexto completo"]
        OK["Responde y resuelve"]
        LOG[("Audit trail y logs<br/>qué decidió, con qué datos y por qué")]
        T --> A
        H1 <--> A
        H2 <--> A
        A --> R
        R -- "sí: no lo hace" --> HUM
        R -- "no" --> E
        E -- "sí" --> HUM
        E -- "no" --> OK
        HUM --> LOG
        OK --> LOG
    end

    subgraph SUP["3 · Supervisión del AI Agent Manager, Módulo 3"]
        MET["Métricas de negocio<br/>resolución autónoma ≥ 80% · CSAT ≥ 4,2 de 5<br/>escalamiento ≤ 20% · tiempo ≤ 3 min"]
        DASH["Dashboard y muestreo del 5% al 10% de los casos"]
        UMB{{"¿Se superó un umbral o hay un patrón?"}}
        INT["Intervenir<br/>volver al bloque 1: ajustar instrucciones o permisos"]
        CORRE["Dejar correr"]
        KILL["Kill switch o circuit breaker<br/>detener al agente"]
        MET --> DASH --> UMB
        UMB -- "sí" --> INT
        UMB -- "no" --> CORRE
        INT -. "riesgo grave" .-> KILL
    end

    REG ==> T
    LOG ==> MET
```

Cómo leerlo en clave n8n: el disparador es el nodo que inicia el flujo; el agente de IA es el nodo AI Agent, con sus instrucciones como mensaje de sistema; el CRM y la base de conocimiento son sus herramientas, y no se le conecta ninguna otra, por los permisos mínimos; las restricciones y el escalamiento son nodos de condición, como IF o Switch; y el audit trail es un nodo que guarda cada ejecución. Lo que n8n no hace solo es lo de los bloques 1 y 3: diseñar, validar y supervisar, que es el trabajo del AI Agent Manager.

## Caso real UPS ORION, visto como un flujo de n8n

Muestra el caso UPS ORION de la sección 5.5: un agente que optimiza rutas de entrega, donde el agente recomienda y el conductor decide. A diferencia del ejemplo anterior, aquí el humano no interviene solo por excepción, sino en cada ruta. La forma de flujo de n8n no viene en el curso: es una analogía para entenderlo.

```mermaid
flowchart TD
    subgraph ESC["1 · Del piloto a la escala, sección 5.5"]
        P["Piloto de medición de rutas, 2003<br/>1 milla menos por conductor al día = 50 M USD al año"]
        C{{"4 condiciones de escala<br/>gobernanza clara · datos de calidad<br/>equipos habilitados · métricas de consistencia"}}
        S["Escala completa en 10 años<br/>55.000 rutas en EE. UU."]
        P --> C
        C -- "se cumplen" --> S
    end

    subgraph FLUJO["2 · Cada ruta, cada día: el flujo tipo n8n"]
        T(["Disparador<br/>inicio de la jornada o cambio de condición"])
        D[["Datos: rutas, clima y volumen"]]
        A["Nodo agente de IA: ORION<br/>optimiza la ruta en tiempo real"]
        REC["Envía la recomendación<br/>al dispositivo del conductor"]
        H{{"El conductor decide<br/>¿sigue la ruta recomendada?"}}
        SIG["Sigue la ruta del agente"]
        DESV["Se desvía según su criterio<br/>el conductor retiene la autoridad"]
        M[("Millas recorridas")]
        T --> A
        D <--> A
        A --> REC --> H
        H -- "sí" --> SIG --> M
        H -- "no" --> DESV --> M
    end

    subgraph VAL["3 · Medir y comunicar el valor, Módulo 5"]
        RES["Resultado a escala, cada año<br/>100 M de millas menos · 400 M USD de ahorro<br/>100.000 toneladas menos de CO₂"]
        H1["H1 · menos costo por milla"]
        H2["H2 · menos emisiones de CO₂<br/>ventaja regulatoria y reputacional"]
        H3["H3 · 15% más volumen<br/>sin aumentar la flota"]
        DIR["Business case a la dirección<br/>mantuvo la inversión durante 10 años"]
        RES --> H1 & H2 & H3 --> DIR
    end

    S ==> T
    M ==> RES
```

Cómo leerlo en clave n8n: el disparador inicia el flujo cada jornada o cuando cambian el tráfico, el clima o el volumen; el nodo de datos alimenta al agente; y el nodo de decisión no lo resuelve una máquina, sino el conductor. En n8n eso se parece a un paso que espera la respuesta de una persona. La lección del curso: el éxito de ORION no fue tecnológico, sino gerencial; la diferencia entre un piloto que muere y un sistema que genera 400 millones de dólares al año es la calidad del management, no la del algoritmo.
