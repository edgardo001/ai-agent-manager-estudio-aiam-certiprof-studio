# Diagramas del código

Diagramas del código del proyecto: qué archivos y funciones existen, y quién llama a quién. A diferencia de `referencia/arquitectura.md`, que muestra el sistema completo a futuro, este archivo muestra el código real de esta versión y se actualiza al terminar cada etapa.

El proyecto no usa clases: por la regla 2 del plan (código simple de seguir), cada archivo de `src/backend/aplicacion/` y de `src/backend/scripts/` agrupa funciones sueltas sobre un mismo tema, y un archivo llama a las funciones de otro. Por eso los diagramas muestran archivos y funciones, no clases.

**Estado:** etapas 0 y 1 terminadas y probadas; etapa 2 terminada, probada por el usuario y corregida tras su revisión (2026-11-18). El 2026-11-19 el código se separó en `aplicacion/` y `scripts/` (D10) y se volvió a probar: 23 fragmentos y 7 de 7.

## 1. El código de hoy (etapas 0 a 2)

Los archivos del código de hoy, los scripts de inicio y limpieza, el `.env`, la base de datos y la conexión con Gemini. Las flechas se leen “usa a”.

```mermaid
flowchart LR
    subgraph LANZ["Scripts de inicio y limpieza"]
        DEV["start-dev.bat<br/>entorno virtual, levanta PostgreSQL<br/>y abre la consola"]
        QA["start-qa.bat<br/>avisa que llega en la etapa 6"]
        CLR["clear.bat<br/>borra el entorno virtual y las cachés<br/>y los contenedores; con --borrar-volumenes,<br/>también los datos"]
    end

    subgraph SCR["src/backend/scripts/ (asistencia, se ejecutan sueltos)"]
        PRU["prueba_conexion.py<br/>probar_conexion()"]
        CAR["cargar_conocimiento.py<br/>fragmentar_documento() · cortar_por_parrafos()<br/>trocear() · cargar_conocimiento()"]
        PBU["probar_busqueda.py<br/>buscar() · probar_busqueda()"]
        EST["estimar_costos.py<br/>estimar_embeddings() · estimar_consulta()<br/>estimar_costos()"]
    end

    subgraph BACK["src/backend/aplicacion/ (el agente)"]
        CON["consola.py<br/>conversar()<br/>cargar_instrucciones()"]
        MOD["modelo.py<br/>preguntar_al_modelo()<br/>crear_embedding()"]
        BD["base_de_datos.py<br/>conectar() · guardar_fragmento()<br/>buscar_fragmentos()"]
        CFG["config.py<br/>leer() · faltan_variables()<br/>RUTA_PROMPT"]
        PROMPT[/"prompt_soporte_n1.md<br/>el JD+SOP, versión 1"/]
    end

    DOCS[/"src/base-de-conocimiento/<br/>8 documentos ficticios"/]
    ENV[/"src/docker/.env"/]
    PG[("PostgreSQL con pgvector<br/>docker-compose.yml<br/>01_esquema.sql · 02_datos_ficticios.sql")]
    GEM[["Gemini API<br/>chat y embeddings"]]

    DEV --> CON
    DEV -->|docker compose| PG
    CON -->|lee| PROMPT
    CON -->|cada mensaje| MOD
    PRU --> MOD
    CAR -->|lee| DOCS
    CAR --> MOD
    CAR --> BD
    PBU --> MOD
    PBU --> BD
    MOD -->|HTTPS| GEM
    BD --> PG
    CON --> CFG
    PRU --> CFG
    CAR --> CFG
    PBU --> CFG
    EST -->|mide los fragmentos| CAR
    EST -->|largo del prompt| PROMPT
    EST --> CFG
    MOD --> CFG
    BD --> CFG
    CFG -->|lee| ENV
```

El código está en dos carpetas (decisión D10): `aplicacion/` es el agente en sí, lo que entra en la imagen Docker; `scripts/` son herramientas de asistencia que se ejecutan sueltas con `python -m scripts.<nombre>` desde `src/backend`. Los scripts usan la aplicación, pero la aplicación nunca usa un script.

Qué hace cada uno, primero la aplicación y después los scripts:

- **`consola.py`**: la puerta de entrada para probar. `conversar()` lee lo que usted escribe, guarda la conversación y muestra la respuesta; `cargar_instrucciones()` lee el prompt. Todavía no usa la base de conocimiento: eso llega con las herramientas, en la etapa 3.
- **`prueba_conexion.py`** (script): `probar_conexion()` manda un saludo para comprobar la clave y el modelo.
- **`cargar_conocimiento.py`** (script, etapa 2): `fragmentar_documento()` corta cada documento por secciones; si una sección es muy larga, `cortar_por_parrafos()` la divide por párrafos, y `trocear()` corta por caracteres un párrafo demasiado largo. `cargar_conocimiento()` calcula los vectores y los guarda. Se corre cuando cambian los documentos.
- **`probar_busqueda.py`** (script, etapa 2): `buscar()` busca una consulta en la base; `probar_busqueda()` prueba una lista de consultas y dice si cada una encuentra el documento esperado.
- **`estimar_costos.py`** (script): estima, sin llamar al modelo, el costo de cargar documentos y el de cada consulta, en tres escenarios de demanda (`costos.md`).
- **`modelo.py`**: el único lugar que habla con Gemini. `preguntar_al_modelo()` conversa; `crear_embedding()` convierte textos en vectores de 768 números.
- **`base_de_datos.py`** (etapa 2): el único lugar que habla con PostgreSQL. `conectar()` abre la conexión; `guardar_fragmento()` y `buscar_fragmentos()` guardan y buscan en la base de conocimiento.
- **`config.py`**: `leer()` toma un valor del `.env`; `faltan_variables()` avisa si falta la clave, el modelo o la contraseña de la base; `RUTA_PROMPT` dice dónde está el prompt, para que la consola, la API y los scripts lo lean sin depender unos de otros.
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

Mapa de lo que se construirá. Los archivos en verde ya existen (etapas 0 a 2); los grises son los previstos en el plan, y sus nombres de funciones pueden ajustarse al programarlos.

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
        MOD["modelo.py<br/>preguntar_al_modelo()<br/>crear_embedding()"]
    end

    SUP["supervision.py<br/>paneles · 5 señales · semáforo<br/>muestreo · costo y valor"]
    BD["base_de_datos.py<br/>conectar() · buscar_fragmentos()<br/>registrar_paso(), etapa 4"]

    subgraph TAREAS["Scripts que se corren a mano"]
        CAR["cargar_conocimiento.py"]
        APR["aprobar_prompt.py"]
        TST["tests/<br/>cinco tipos de pruebas"]
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
    class CON,MOD,PRU,BD,CAR,PBU existe
    class API,FRONT,AGE,REG,HER,SUP,APR,TST previsto
```

No se dibuja `config.py`, que ya existe, porque casi todos los archivos lo usan para leer el `.env`. Cómo leerlo: todo pasa por `agente.py`, que es el único lugar donde está el bucle del agente; la consola y la API son dos puertas hacia la misma función (decisión D6). El agente nunca habla directo con la base de datos ni con Gemini: lo hace a través de `base_de_datos.py` y `modelo.py`. `supervision.py` no atiende tickets: calcula lo que el AI Agent Manager mira en el dashboard (Módulo 3).

## 4. Modelo entidad-relación: las seis tablas

Es el esquema real de `src/docker/postgres/01_esquema.sql` (etapa 2), con todas sus columnas. `PK` es la llave primaria (el identificador de cada fila) y `FK` una llave foránea (la columna que apunta a otra tabla).

```mermaid
erDiagram
    registro_agentes ||--o{ tickets : "atiende"
    clientes ||--o{ tickets : "abre"
    tickets ||--o{ mensajes : "tiene"
    tickets |o--o{ registro_auditoria : "deja pasos en"
    registro_agentes ||--o{ registro_auditoria : "registra"

    registro_agentes {
        serial id PK
        text nombre
        text rol
        text alcance
        text fuera_de_alcance
        text nivel_autonomia
        text dueno "el AI Agent Manager"
        text area_responsable
        text permisos "con su justificación"
        text restricciones
        text version_prompt
        text aprobado_por
        timestamptz fecha_aprobacion
        timestamptz fecha_ultima_auditoria
        boolean detenido "el kill switch"
        text motivo_detencion
        numeric meta_resolucion_autonoma
        numeric meta_escalamiento
        numeric meta_minutos_resolucion
        numeric meta_csat
        numeric base_casos_por_dia "línea base"
        numeric base_minutos_por_caso "línea base"
        numeric base_costo_por_caso "línea base"
        timestamptz creado_en
    }
    clientes {
        serial id PK
        text codigo UK "C-001"
        text nombre
        text empresa
        text plan
        text historial
    }
    tickets {
        serial id PK
        int agente_id FK
        int cliente_id FK
        text texto
        text estado "nuevo, respondido, resuelto..."
        timestamptz creado_en
        timestamptz cerrado_en
        text respuesta
        text motivo_escalamiento
        text resumen_escalamiento
        text escalado_por "modelo o regla"
        numeric minutos_persona
        int tokens_entrada
        int tokens_salida
        numeric costo_tokens
        int csat "1 a 5"
        boolean en_muestra
        text revisado_por
        boolean error_encontrado
        text categoria_error
    }
    mensajes {
        serial id PK
        int ticket_id FK
        text quien "cliente, agente o persona"
        text texto
        timestamptz creado_en
    }
    registro_auditoria {
        bigserial id PK
        int agente_id FK
        int ticket_id FK "vacío en intervenciones"
        int paso
        text tipo "modelo, herramienta, regla..."
        text decision
        jsonb datos_usados
        text motivo
        text version_prompt
        int tokens
        text quien
        timestamptz creado_en
    }
    fragmentos_conocimiento {
        serial id PK
        text documento
        text seccion
        int orden
        text texto
        vector embedding "768 números"
        text modelo_embedding "gemini-embedding-001"
        text hash_documento "huella SHA-256"
        timestamptz cargado_en
    }
```

Cómo leer las relaciones:

- **Un agente atiende muchos tickets,** y **un cliente abre muchos tickets:** cada ticket guarda `agente_id` y `cliente_id`.
- **Un ticket tiene muchos mensajes:** la conversación completa, para que la persona que recibe un caso escalado vea todo.
- **El registro de auditoría** siempre apunta a un agente y casi siempre a un ticket; `ticket_id` queda vacío en las intervenciones que no son de un ticket, como detener el agente o registrar un cambio externo (por eso la línea hacia `tickets` empieza con un círculo: puede no haber ticket).
- **`fragmentos_conocimiento` no se une con ninguna tabla:** es la biblioteca del RAG, que consulta `buscar_fragmentos()`. Cada vector guarda con qué modelo se creó y de qué versión del documento viene, y la búsqueda solo compara vectores del mismo modelo (decisión D8).
- **`clientes.codigo`** es único (`UK`): es el ID que da el cliente, como `C-001`; `id` es el número interno que usan las uniones.

Qué tabla cubre qué parte del curso: `registro_agentes`, la identidad, el nivel de autonomía, el registro contra el agent sprawl, la aprobación, la línea base y el kill switch (secciones 1.2, 2.2, 2.6, 2.7 y 3.7; la 4.5 lo llama circuit breaker); `clientes`, el CRM de solo lectura (2.3); `fragmentos_conocimiento`, las soluciones documentadas (2.5); `tickets`, el escalamiento, los indicadores, el muestreo y el costo (2.5, 3.2, 3.3 y Módulo 5); `mensajes`, el traspaso con contexto (Módulo 4); y `registro_auditoria`, el audit trail y las intervenciones (Módulo 1, pregunta 9, y sección 3.4).

## 5. El RAG de la etapa 2: cargar y buscar documentos

Cómo llegan los documentos de soporte a pgvector y cómo se buscan. Es la versión 1, con `pg8000` y los vectores enviados como texto con `::vector` (decisiones D1 y D2). Se construye en la etapa 2.

```mermaid
flowchart LR
    subgraph CARGA["Carga: cargar_conocimiento.py, se corre cuando cambian los documentos"]
        DOCS[/"base-de-conocimiento/<br/>documentos .md"/]
        TRO["fragmentar_documento()<br/>por secciones; si es muy larga,<br/>por párrafos y luego por caracteres"]
        EMB["modelo.py<br/>crear_embedding()<br/>768 números por fragmento"]
        INS["base_de_datos.py<br/>guarda texto, vector con %s::vector,<br/>modelo y huella"]
        DOCS --> TRO --> EMB --> INS
    end
    TABLA[("fragmentos_conocimiento<br/>documento · sección · texto · embedding")]
    subgraph BUSQ["Búsqueda: probar_busqueda.py (etapa 2) y buscar_solucion() (etapa 3)"]
        CON["consulta<br/>el problema en pocas palabras"]
        EMQ["modelo.py<br/>crear_embedding()"]
        BUS["base_de_datos.py<br/>buscar_fragmentos()<br/>solo vectores del mismo modelo<br/>ORDER BY embedding &lt;=&gt; %s::vector<br/>LIMIT 5"]
        RES["los 5 fragmentos<br/>más parecidos"]
        CON --> EMQ --> BUS --> RES
    end
    INS --> TABLA
    TABLA -.-> BUS
```

En la etapa 3, esos 5 fragmentos vuelven al modelo dentro de la herramienta `buscar_solucion()`, y el agente responde solo con soluciones documentadas, como pide la sección 2.5.
