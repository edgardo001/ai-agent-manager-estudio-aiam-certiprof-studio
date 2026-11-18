# Diagramas del código

Diagramas del código del proyecto: qué archivos y funciones existen, y quién llama a quién. A diferencia de `arquitectura.md`, que muestra el sistema completo a futuro, este archivo muestra el código real de esta versión y se actualiza al terminar cada etapa.

El proyecto no usa clases: por la regla 2 del plan (código simple de seguir), cada archivo de `src/backend/src/` agrupa funciones sueltas sobre un mismo tema, y un archivo llama a las funciones de otro. Por eso los diagramas muestran archivos y funciones, no clases.

**Estado:** etapas 0 y 1 terminadas (2026-11-18).

## 1. El código de hoy (etapas 0 y 1)

Los archivos del código de hoy, los tres scripts de inicio y limpieza, el `.env` y la conexión con Gemini. Las flechas se leen “usa a”.

```mermaid
flowchart LR
    subgraph LANZ["Scripts de inicio y limpieza"]
        DEV["start-dev.bat<br/>crea el entorno virtual,<br/>instala y abre la consola"]
        QA["start-qa.bat<br/>por ahora, solo avisa<br/>que llega en la etapa 6"]
        CLR["clear.bat<br/>borra el entorno virtual y las cachés;<br/>con confirmación, también Docker"]
    end

    subgraph BACK["src/backend/src/"]
        CON["consola.py<br/>conversar()<br/>cargar_instrucciones()"]
        PRU["prueba_conexion.py<br/>probar_conexion()"]
        MOD["modelo.py<br/>preguntar_al_modelo()"]
        CFG["config.py<br/>leer()<br/>faltan_variables()"]
        PROMPT[/"prompt_soporte_n1.md<br/>el JD+SOP, versión 1"/]
    end

    ENV[/"src/docker/.env<br/>clave y nombre del modelo"/]
    GEM[["Gemini API<br/>gemini-3.1-flash-lite"]]

    DEV --> CON
    CON -->|lee| PROMPT
    CON -->|¿faltan variables?| CFG
    CON -->|cada mensaje| MOD
    PRU --> CFG
    PRU --> MOD
    MOD --> CFG
    CFG -->|lee| ENV
    MOD -->|HTTPS| GEM
```

Qué hace cada uno:

- **`consola.py`**: la puerta de entrada para probar. `conversar()` lee lo que usted escribe, guarda la conversación y muestra la respuesta; `cargar_instrucciones()` lee el prompt.
- **`prueba_conexion.py`**: `probar_conexion()` manda un saludo para comprobar la clave y el modelo.
- **`modelo.py`**: `preguntar_al_modelo()` es el único lugar del código que habla con Gemini.
- **`config.py`**: `leer()` toma un valor del `.env`; `faltan_variables()` avisa si falta la clave o el modelo.
- **`prompt_soporte_n1.md`**: no es código; es el texto que define al agente.

## 2. Qué pasa en cada mensaje de la consola

```mermaid
sequenceDiagram
    actor P as Persona
    participant C as consola.py
    participant M as modelo.py
    participant F as config.py
    participant G as Gemini API

    Note over C: al empezar, carga el prompt JD+SOP<br/>como primer mensaje de la conversación
    P->>C: escribe un mensaje
    C->>C: lo agrega a la conversación
    C->>M: preguntar_al_modelo(conversación completa)
    M->>F: URL, clave y nombre del modelo
    M->>G: envía la conversación (máximo 60 segundos)
    G-->>M: respuesta en texto
    M-->>C: texto de la respuesta
    C->>C: agrega la respuesta a la conversación
    C-->>P: muestra la respuesta
```

Lo importante: el modelo no recuerda nada entre mensajes. La consola le envía cada vez la conversación completa, empezando por el prompt; así el agente “recuerda” lo dicho y sigue sus instrucciones en cada respuesta.

## 3. Cómo quedará el código al terminar la versión 1 (etapa 7)

Mapa de lo que se construirá. Los archivos en verde ya existen; los grises son los previstos en el plan, y sus nombres de funciones pueden ajustarse al programarlos.

```mermaid
flowchart TD
    subgraph ENTRADAS["Puertas de entrada"]
        CON["consola.py<br/>conversar()"]
        API["api.py<br/>FastAPI: tickets, cola de escalaciones,<br/>revisión, dashboard, kill switch"]
        FRONT["frontend/src/<br/>páginas HTML y JavaScript"]
    end

    AGE["agente.py<br/>atender_ticket()<br/>el bucle del agente"]

    subgraph PIEZAS["Lo que usa el agente"]
        REG["reglas.py<br/>agente_detenido() · tiempo_excedido()<br/>revisar_entrada() · revisar_respuesta()"]
        HER["herramientas.py<br/>buscar_cliente() · buscar_solucion()<br/>escalar_a_humano()"]
        MOD["modelo.py<br/>preguntar_al_modelo()<br/>crear_embedding(), etapa 2"]
    end

    SUP["supervision.py<br/>paneles · 5 señales · semáforo<br/>muestreo · costo y valor"]
    BD["base_de_datos.py<br/>conectar() · buscar_fragmentos()<br/>registrar_paso(), etapa 4"]

    subgraph TAREAS["Scripts que se corren a mano"]
        CAR["cargar_conocimiento.py"]
        APR["aprobar_prompt.py"]
        TST["tests/<br/>pruebas en tres grupos"]
        PRU["prueba_conexion.py"]
        PBU["probar_busqueda.py"]
    end

    PG[("PostgreSQL con pgvector<br/>6 tablas")]
    DOCS[/"base-de-conocimiento/<br/>documentos .md"/]
    GEM[["Gemini API"]]

    FRONT -->|HTTP| API
    CON --> AGE
    API --> AGE
    API --> SUP
    AGE --> REG
    AGE --> HER
    AGE --> MOD
    AGE -->|cada paso: audit trail| BD
    HER --> BD
    HER -->|buscar_solucion| MOD
    SUP --> BD
    CAR --> DOCS
    CAR --> MOD
    CAR --> BD
    APR --> TST
    APR -->|versión aprobada| BD
    PRU --> MOD
    PBU --> MOD
    PBU --> BD
    TST --> AGE
    MOD --> GEM
    BD --> PG

    classDef existe fill:#d8f3dc,stroke:#2d6a4f,color:#1b4332
    classDef previsto fill:#eeeeee,stroke:#888888,color:#333333
    class CON,MOD,PRU existe
    class API,FRONT,AGE,REG,HER,SUP,BD,CAR,APR,TST,PBU previsto
```

No se dibuja `config.py`, que ya existe, porque casi todos los archivos lo usan para leer el `.env`. Cómo leerlo: todo pasa por `agente.py`, que es el único lugar donde está el bucle del agente; la consola y la API son dos puertas hacia la misma función (decisión D6). El agente nunca habla directo con la base de datos ni con Gemini: lo hace a través de `base_de_datos.py` y `modelo.py`. `supervision.py` no atiende tickets: calcula lo que el AI Agent Manager mira en el dashboard (Módulo 3).

## 4. Los datos: las seis tablas y cómo se relacionan

Se crean en la etapa 2 (`src/docker/postgres/01_esquema.sql`). Se muestran las columnas principales y las que unen las tablas; la lista completa está en “Modelo de datos” del plan.

```mermaid
erDiagram
    registro_agentes ||--o{ tickets : "atiende"
    clientes ||--o{ tickets : "abre"
    tickets ||--o{ mensajes : "conversación"
    tickets ||--o{ registro_auditoria : "cada paso"
    registro_agentes ||--o{ registro_auditoria : "intervenciones y pasos"

    registro_agentes {
        int id
        text nombre
        text nivel_autonomia
        bool detenido
        text version_prompt
    }
    clientes {
        int id
        text codigo
        text nombre
    }
    tickets {
        int id
        int agente_id
        int cliente_id
        text estado
        int csat
        bool en_muestra
    }
    mensajes {
        int id
        int ticket_id
        text quien
        text texto
    }
    registro_auditoria {
        int id
        int agente_id
        int ticket_id
        text tipo
        text decision
    }
    fragmentos_conocimiento {
        int id
        text documento
        text texto
        vector embedding
    }
```

`fragmentos_conocimiento` no se une con las demás: es la biblioteca que consulta `buscar_solucion()` (el RAG del proyecto).

En `clientes`, `codigo` es el ID visible que da el cliente, con el formato `C-001`; `id` es el número interno que usan las uniones. En `registro_auditoria`, `ticket_id` queda vacío en las intervenciones que no son de un ticket, como detener el agente o registrar un cambio externo.

## 5. El RAG de la etapa 2: cargar y buscar documentos

Cómo llegan los documentos de soporte a pgvector y cómo se buscan. Es la versión 1, con `pg8000` y los vectores enviados como texto con `::vector` (decisiones D1 y D2). Se construye en la etapa 2.

```mermaid
flowchart LR
    subgraph CARGA["Carga: cargar_conocimiento.py, se corre cuando cambian los documentos"]
        DOCS[/"base-de-conocimiento/<br/>documentos .md"/]
        TRO["trocear el texto<br/>unos 1.200 caracteres<br/>con 200 de solape"]
        EMB["modelo.py<br/>crear_embedding()<br/>768 números por fragmento"]
        INS["base_de_datos.py<br/>guarda texto y vector<br/>con %s::vector"]
        DOCS --> TRO --> EMB --> INS
    end
    TABLA[("fragmentos_conocimiento<br/>documento · texto · embedding")]
    subgraph BUSQ["Búsqueda: probar_busqueda.py (etapa 2) y buscar_solucion() (etapa 3)"]
        CON["consulta<br/>el problema en pocas palabras"]
        EMQ["modelo.py<br/>crear_embedding()"]
        BUS["base_de_datos.py<br/>buscar_fragmentos()<br/>ORDER BY embedding &lt;=&gt; %s::vector<br/>LIMIT 5"]
        RES["los 5 fragmentos<br/>más parecidos"]
        CON --> EMQ --> BUS --> RES
    end
    INS --> TABLA
    TABLA -.-> BUS
```

En la etapa 3, esos 5 fragmentos vuelven al modelo dentro de la herramienta `buscar_solucion()`, y el agente responde solo con soluciones documentadas, como pide la sección 2.5.
