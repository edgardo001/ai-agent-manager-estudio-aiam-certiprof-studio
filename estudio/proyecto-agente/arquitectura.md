# Proyecto de agente: arquitectura del Agente de Soporte N1

Material para construir de verdad un agente de IA a partir del curso. El agente es el Agente de Soporte N1: el agente de soporte técnico B2B de la sección 2.5 del Módulo 2, el mismo que usan como ejemplo las plantillas de `estudio/plantillas/`.

Qué viene del curso y qué no: las reglas que el agente debe cumplir (identidad, permisos mínimos, instrucciones JD+SOP, restricciones, escalamiento, validación antes de producción y métricas) salen de los Módulos 2 y 3. La arquitectura técnica, los contenedores, las tecnologías y los proveedores de modelos no vienen en el curso: son una propuesta para programarlo.

Orden de lectura: primero, la arquitectura general, que muestra qué pieza técnica responde a cada exigencia del curso; segundo, la arquitectura en contenedores, desde la API REST hacia atrás; tercero, el inventario de qué se instala, se obtiene, se descarga, se programa y se despliega; y cuarto, la secuencia de un caso.

Material relacionado: el texto del system prompt (JD+SOP) y la definición de una herramienta están en `../plantillas/05-instrucciones-del-agente.md`; los diagramas de los temas del curso, en `../diagramas.md`; y el índice de todo el material, en `../indice.md`.

## Arquitectura de un proyecto de agente: el Agente de Soporte N1 llevado a código

Muestra las piezas técnicas que hacen falta para construir de verdad un agente como el de soporte técnico de la sección 2.5, y a qué exigencia del curso responde cada una. Los conceptos de gestión salen del Módulo 2 (secciones 2.2 a 2.7) y del Módulo 3 (secciones 3.2 a 3.5); la arquitectura técnica, los componentes y las tecnologías no vienen en el curso: son una propuesta para quien quiera programarlo.

```mermaid
flowchart TD
    subgraph CANAL["1 · Canales de entrada"]
        WEB(["Chat web"])
        MAIL(["Correo o formulario"])
        API_IN(["Sistema de tickets"])
    end

    subgraph BACK["2 · Backend del agente: tu código"]
        GW["API de entrada<br/>autenticación · límite de uso"]
        GIN{{"Guardrail de entrada<br/>datos sensibles · intentos de manipulación"}}
        ORQ["Orquestador: el bucle del agente<br/>piensa · usa una herramienta · observa · repite"]
        INST[/"Instrucciones versionadas<br/>descripción del cargo + SOP"/]
        LLM[["Modelo de lenguaje vía API"]]
        MEM[("Memoria de la conversación")]
        GOUT{{"Guardrail de salida<br/>¿viola una restricción?"}}
        ESC{{"Reglas de escalamiento<br/>sin solución · cancelación · más de 8 min"}}
        RESP["Responde al cliente<br/>por el mismo canal"]
    end

    subgraph TOOLS["3 · Herramientas con permisos mínimos"]
        CRM[["CRM: solo lectura"]]
        KB[["Base de conocimiento<br/>búsqueda semántica"]]
        TK[["Crear o cerrar ticket"]]
    end

    subgraph HUM["4 · Humano en el circuito"]
        COLA["Cola de escalamiento<br/>traspaso con el contexto completo"]
        AGT["Persona de soporte"]
    end

    subgraph OBS["5 · Observabilidad y gobierno: el AI Agent Manager"]
        LOG[("Audit trail<br/>cada decisión, datos usados y motivo")]
        MET["Métricas de negocio<br/>resolución autónoma · CSAT · escalamiento · tiempo"]
        DASH["Dashboard y muestreo del 5% al 10%"]
        REG[("Registro de agentes<br/>dueño · nivel · versión")]
        EVAL["Pruebas antes de cada versión<br/>funcional · límites · adversarial<br/>escalamiento · métricas"]
        KILL["Kill switch<br/>apagar el agente sin desplegar"]
    end

    WEB & MAIL & API_IN --> GW --> GIN --> ORQ
    INST --> ORQ
    ORQ <--> LLM
    ORQ <--> MEM
    ORQ <--> CRM & KB & TK
    ORQ --> GOUT --> ESC
    ESC -- "no" --> RESP
    ESC -- "sí" --> COLA --> AGT
    ORQ -. "registra cada paso" .-> LOG
    LOG --> MET --> DASH
    EVAL -. "aprueba la versión" .-> INST
    REG -. "controla" .-> ORQ
    KILL -. "detiene" .-> ORQ
```

Cómo leerlo: los bloques 1 a 4 son el producto que se programa, y el bloque 5 es lo que convierte ese programa en un agente gobernable, que es justamente lo que enseña el curso. El orquestador es el corazón: recibe el caso, le pasa al modelo de lenguaje las instrucciones y el contexto, y repite el ciclo de pensar, usar una herramienta y observar el resultado hasta resolver o escalar. Los permisos mínimos se implementan dándole al agente solo tres herramientas, y el CRM en modo lectura; las restricciones y el escalamiento se implementan como reglas en código, no como algo que el modelo decide solo, porque el curso dice que cuándo interviene un humano es una decisión de governance. El audit trail es una tabla o un registro donde cada paso queda guardado, y de ahí salen las métricas del dashboard. Las pruebas de los cinco filtros de validación de la sección 2.6 se vuelven pruebas automáticas que se corren antes de publicar cada versión de las instrucciones.

Con qué se puede construir (esto no viene en el curso): el orquestador se puede programar directamente con el SDK del proveedor del modelo, que existe para Python, C#, Java y Node, o con un framework de agentes como LangGraph en Python, Semantic Kernel en C# y Java, o el Vercel AI SDK en Node. La base de conocimiento usa búsqueda semántica, por ejemplo PostgreSQL con la extensión pgvector; la memoria, Redis o la misma base de datos; el audit trail, una tabla en PostgreSQL; el dashboard, Grafana o Metabase; y el kill switch, una variable de configuración o un feature flag que el orquestador revisa antes de cada caso. El CRM y el sistema de tickets pueden ser simulados al principio, con una base de datos propia.

## Arquitectura técnica en contenedores: el Agente de Soporte N1 desde la API REST hacia atrás

Versión técnica del diagrama anterior, sin los canales de entrada, que son solo interfaz: parte de la API REST y muestra los contenedores de Docker, las tablas y los proveedores de modelos, Gemini con una clave de Google AI Studio u OpenRouter. Las reglas del agente salen del Módulo 2, sección 2.5, y las métricas del Módulo 3; toda la arquitectura, los contenedores y las tecnologías no vienen en el curso.

```mermaid
flowchart TD
    CLI(["Cliente REST<br/>curl, Postman o una interfaz futura"])

    API["contenedor api · backend REST<br/>POST /tickets · GET /tickets/:id<br/>GET /escalations · POST /admin/kill-switch"]

    RD[("contenedor redis<br/>cola de casos · memoria corta<br/>bandera del kill switch")]

    subgraph WKS["contenedor agent-worker"]
        WK["orquestador<br/>bucle: modelo, herramienta, observar<br/>tope de pasos y de tiempo"]
        LLMC["llm-client<br/>formato compatible con OpenAI<br/>se cambia base_url y modelo"]
        TOOLS["herramientas<br/>buscar cliente · buscar solución<br/>escalar a una persona"]
        GR{{"guardrails en código<br/>restricciones · reglas de escalamiento"}}
        WK <--> LLMC
        WK <--> TOOLS
        WK --> GR
    end

    subgraph EXT["Proveedores de modelos, fuera de Docker"]
        GEM[["Gemini API<br/>clave de Google AI Studio"]]
        OR[["OpenRouter API<br/>muchos modelos con una sola clave"]]
    end

    CRM["contenedor mock-crm<br/>REST de solo lectura"]
    ING["contenedor ingest · tarea puntual<br/>documentos a fragmentos y embeddings"]

    PG[("contenedor postgres con pgvector<br/>tickets · messages · kb_chunks<br/>audit_log · prompt_versions<br/>agent_registry · escalations")]

    subgraph OBS["Observabilidad y gobierno"]
        GF["contenedor grafana<br/>dashboard de métricas de negocio"]
        LF["contenedor langfuse, opcional<br/>traza de cada llamada al modelo"]
        CI["CI · pruebas de los 5 filtros<br/>conjunto fijo de casos de prueba"]
    end

    CLI -->|"HTTP con API key"| API
    API -->|"encola ticket_id"| RD
    RD -->|"toma el caso · kill switch"| WK
    LLMC --> GEM
    LLMC --> OR
    TOOLS -->|"solo lectura"| CRM
    TOOLS -->|"búsqueda vectorial · escalations"| PG
    API -->|"guarda y consulta tickets"| PG
    WK -->|"prompt aprobado · audit_log · escalations"| PG
    ING -->|"embeddings"| GEM
    ING --> PG
    PG --> GF
    WK -.-> LF
    CI -.->|"aprueba una versión del prompt"| PG
```

Cómo leerlo: la API no llama al modelo directamente; guarda el ticket, lo pone en una cola de Redis y responde de inmediato, porque una llamada al modelo puede tardar varios segundos y el agente puede necesitar varias. El agent-worker toma el caso y hace el bucle: le manda al modelo el prompt aprobado, que es el documento JD+SOP guardado en la tabla prompt_versions, y las herramientas disponibles; si el modelo pide una herramienta, el worker la ejecuta y le devuelve el resultado. Las herramientas son solo tres, buscar cliente, buscar solución y escalar a una persona, y las dos primeras son de solo lectura: es el principio de permisos mínimos. El texto exacto del prompt y la definición de una herramienta están en la plantilla 05, `../plantillas/05-instrucciones-del-agente.md`. Los guardrails son código normal, no parte del prompt: revisan las restricciones y las reglas de escalamiento, como los 8 minutos o la mención de cancelación, y si corresponde dejan el caso en la tabla escalations con todo el contexto para que lo tome una persona.

Sobre los modelos: tanto Gemini como OpenRouter ofrecen un punto de acceso compatible con el formato de OpenAI, así que un solo cliente sirve para los dos y cambiar de proveedor es cambiar la URL base, la clave y el nombre del modelo en la configuración. Para la búsqueda semántica de la base de conocimiento se necesita además un modelo de embeddings, por ejemplo el de Gemini. Para el gobierno: cada paso queda en audit_log, de donde Grafana calcula la resolución autónoma, el escalamiento, el tiempo y el CSAT; la bandera del kill switch en Redis se revisa antes de cada caso y de cada paso; y una versión nueva del prompt solo se marca como aprobada si pasa en CI las pruebas de los cinco filtros de la sección 2.6.

## Inventario del Agente de Soporte N1: qué se instala, se obtiene, se descarga, se programa y se despliega

Complementa el diagrama de contenedores: separa cada componente según de dónde sale, en el orden en que conviene trabajar. Nada de esto viene en el curso; las reglas que el código debe cumplir salen del Módulo 2, secciones 2.2 a 2.6, y las métricas del Módulo 3, sección 3.2.

```mermaid
flowchart TD
    subgraph INS["1 · Instalar en tu equipo"]
        I1["Docker Desktop"]
        I2["git y un editor"]
        I3["SDK de tu lenguaje<br/>Python, .NET, Java o Node"]
    end

    subgraph OBT["2 · Obtener: cuentas, claves y datos"]
        O1["Clave de API de Google AI Studio<br/>modelo de chat y de embeddings"]
        O2["Clave de API de OpenRouter, opcional<br/>para probar otros modelos"]
        O3["Documentos de la base de conocimiento<br/>preguntas y soluciones de soporte"]
        O4["Casos de prueba<br/>tickets de ejemplo con su resultado esperado"]
    end

    subgraph DES["3 · Descargar: imágenes de Docker ya hechas"]
        D1[("pgvector/pgvector<br/>PostgreSQL con búsqueda vectorial")]
        D2[("redis")]
        D3["grafana/grafana"]
        D4["langfuse, opcional<br/>trae su propio compose"]
    end

    subgraph DEV["4 · Desarrollar: tu código, una imagen por servicio"]
        V1["api<br/>endpoints REST · autenticación"]
        V2["agent-worker<br/>bucle del agente · llm-client<br/>herramientas · guardrails · audit_log"]
        V3["mock-crm<br/>REST de solo lectura con datos ficticios"]
        V4["ingest<br/>fragmenta documentos y crea embeddings"]
        V5["Archivos de configuración<br/>esquema SQL · prompt JD+SOP · .env"]
        V6["Pruebas de los 5 filtros<br/>se corren en CI antes de cada versión"]
    end

    subgraph DEP["5 · Desplegar"]
        P1["docker compose up<br/>en tu equipo"]
        P2["Crear tablas y cargar el prompt aprobado"]
        P3["Ejecutar ingest una vez"]
        P4["Probar con curl y revisar Grafana"]
        P5["Después: una máquina virtual en la nube<br/>con el mismo compose"]
        P1 --> P2 --> P3 --> P4 --> P5
    end

    INS --> OBT --> DES --> DEV --> DEP
```

Cómo leerlo: lo único que se programa es el bloque 4; el resto se instala, se descarga o se configura. Instalar: Docker Desktop, git, un editor y el SDK del lenguaje elegido. Obtener: una clave gratuita de Google AI Studio alcanza para empezar con Gemini, tanto para conversar como para los embeddings; la de OpenRouter sirve para comparar otros modelos cambiando solo la configuración. También hay que reunir los documentos de soporte que formarán la base de conocimiento y un conjunto de tickets de prueba con su resultado esperado, que son la materia prima de los cinco filtros de validación de la sección 2.6. Descargar: PostgreSQL con pgvector, Redis y Grafana no se programan, se usan como imágenes de Docker; Langfuse es opcional y más pesado, porque trae varios contenedores propios.

Desarrollar son cuatro servicios pequeños. La api recibe y consulta tickets. El agent-worker es el corazón: el bucle del agente, el cliente del modelo, las tres herramientas, los guardrails y el registro de cada paso. El mock-crm simula el CRM con datos ficticios, y el ingest es una tarea que se corre una vez para cargar la base de conocimiento. Con Python, por ejemplo, serían FastAPI para la api, la librería openai apuntando a la URL de Gemini o de OpenRouter, psycopg para PostgreSQL y redis-py; en C#, ASP.NET Core y un BackgroundService; en Java, Spring Boot; y en Node, Fastify o Express con la librería openai. Desplegar es levantar todo con docker compose, crear las tablas, cargar el prompt aprobado, ejecutar el ingest y probar con curl; más adelante, el mismo archivo compose funciona en una máquina virtual en la nube.

Esqueleto del archivo docker-compose.yml, para orientarse; las claves van en un archivo .env que nunca se sube al repositorio:

```yaml
services:
  api:
    build: ./api                      # tu código
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [postgres, redis]

  agent-worker:
    build: ./agent-worker             # tu código: bucle, herramientas, guardrails
    env_file: .env                    # LLM_BASE_URL, LLM_API_KEY, LLM_MODEL
    depends_on: [postgres, redis, mock-crm]

  mock-crm:
    build: ./mock-crm                 # tu código: CRM simulado

  ingest:
    build: ./ingest                   # tu código: se ejecuta una vez
    env_file: .env
    profiles: ["tareas"]              # docker compose run ingest
    depends_on: [postgres]

  postgres:
    image: pgvector/pgvector:pg16     # descargada
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes: ["pgdata:/var/lib/postgresql/data", "./sql:/docker-entrypoint-initdb.d"]

  redis:
    image: redis:7-alpine             # descargada

  grafana:
    image: grafana/grafana            # descargada
    ports: ["3000:3000"]
    depends_on: [postgres]

volumes:
  pgdata:
```

Para cambiar de proveedor de modelo basta con editar el .env: con Gemini, la URL base es la de su punto de acceso compatible con OpenAI, `https://generativelanguage.googleapis.com/v1beta/openai/`; con OpenRouter, `https://openrouter.ai/api/v1`; en los dos casos se indica la clave y el nombre del modelo.

## Secuencia de un caso en el Agente de Soporte N1

Muestra, paso a paso, qué pasa entre los contenedores del diagrama anterior cuando llega un ticket. Las condiciones de escalamiento salen del Módulo 2, sección 2.5; la secuencia técnica no viene en el curso.

```mermaid
sequenceDiagram
    autonumber
    participant C as Cliente REST
    participant A as api
    participant R as redis
    participant W as agent-worker
    participant P as postgres
    participant M as Gemini u OpenRouter
    participant K as mock-crm

    C->>A: POST /tickets
    A->>P: guarda el ticket, estado nuevo
    A->>R: encola ticket_id
    A-->>C: 202 Accepted con ticket_id
    W->>R: toma ticket_id
    W->>R: ¿kill switch activo?
    alt kill switch activo
        W->>P: escala a una persona
    else agente habilitado
        W->>P: lee el prompt JD+SOP aprobado
        loop hasta resolver, escalar o llegar al tope de pasos
            W->>M: mensajes y lista de herramientas
            M-->>W: respuesta o pedido de herramienta
            opt pide una herramienta
                W->>K: buscar cliente, solo lectura
                W->>P: buscar solución en kb_chunks
            end
            W->>P: registra el paso en audit_log
            W->>W: guardrails: restricción, cancelación, más de 8 min
        end
        alt resuelto
            W->>P: guarda la respuesta, estado resuelto
        else hay que escalar
            W->>P: crea la escalación con el contexto completo
        end
    end
    C->>A: GET /tickets/:id
    A-->>C: estado y respuesta
```

Cómo leerlo: el cliente recibe de inmediato un número de ticket y después consulta el resultado, o la API lo avisa con un webhook, una llamada de vuelta. Dentro del bucle, el modelo nunca toca la base de datos ni el CRM: solo pide herramientas, y el worker decide si las ejecuta. El tope de pasos evita que el agente quede dando vueltas y gastando llamadas; si se alcanza, el caso se escala.
