-- Etapa 2. Esquema del Agente de Soporte N1: las seis tablas del plan ("Modelo de datos").
-- PostgreSQL ejecuta este archivo la primera vez que se crea el volumen de datos,
-- antes que 02_datos_ficticios.sql (el número fija el orden).
-- Desde la etapa 3 se usan registro_agentes, clientes, fragmentos_conocimiento, tickets y mensajes;
-- registro_auditoria se usa desde la etapa 4. Todas se crean ya para no recrear la base en cada etapa.

-- pgvector: agrega el tipo "vector" y la búsqueda por parecido.
CREATE EXTENSION IF NOT EXISTS vector;

-- Registro del agente: quién es, qué puede hacer, quién responde por él y sus metas.
-- Curso: identidad (2.2), nivel de autonomía (1.2), registro contra el agent sprawl (2.7),
-- aprobación (2.6), línea base (3.7) y kill switch (1.2) y circuit breaker (4.5).
CREATE TABLE registro_agentes (
    id                       serial PRIMARY KEY,
    nombre                   text NOT NULL,
    rol                      text NOT NULL,
    alcance                  text NOT NULL,
    fuera_de_alcance         text NOT NULL,
    nivel_autonomia          text NOT NULL,
    dueno                    text NOT NULL,          -- el AI Agent Manager que responde por el agente
    area_responsable         text NOT NULL,
    permisos                 text NOT NULL,          -- cada permiso con su justificación
    restricciones            text NOT NULL,
    version_prompt           text,                   -- versión aprobada (etapa 5)
    aprobado_por             text,
    fecha_aprobacion         timestamptz,            -- la última validación
    fecha_ultima_auditoria   timestamptz,
    detenido                 boolean NOT NULL DEFAULT false,   -- el kill switch
    motivo_detencion         text,
    meta_resolucion_autonoma numeric NOT NULL,       -- porcentaje
    meta_escalamiento        numeric NOT NULL,       -- porcentaje máximo
    meta_minutos_resolucion  numeric NOT NULL,
    meta_csat                numeric NOT NULL,       -- de 1 a 5
    base_casos_por_dia       numeric,                -- línea base: cómo se atendía sin el agente
    base_minutos_por_caso    numeric,
    base_costo_por_caso      numeric,                -- en dólares
    creado_en                timestamptz NOT NULL DEFAULT now()
);

-- CRM simulado: el agente solo puede leerlo (permisos mínimos, sección 2.3).
CREATE TABLE clientes (
    id         serial PRIMARY KEY,
    codigo     text NOT NULL UNIQUE,                 -- el ID que da el cliente, por ejemplo C-001
    nombre     text NOT NULL,
    empresa    text NOT NULL,
    plan       text NOT NULL,
    historial  text NOT NULL DEFAULT ''
);

-- Base de conocimiento para el RAG: cada documento cortado en fragmentos, con su vector.
-- Curso: el agente responde solo con soluciones documentadas (sección 2.5).
-- Cada vector guarda con qué modelo se creó y de qué versión del documento viene:
-- vectores de modelos distintos no se pueden comparar (decisión D8).
-- vector(768) obliga a que cada vector tenga exactamente 768 números (decisión D5).
CREATE TABLE fragmentos_conocimiento (
    id                serial PRIMARY KEY,
    documento         text NOT NULL,                 -- nombre del archivo de base-de-conocimiento/
    seccion           text NOT NULL,                 -- sección del documento, para citar con precisión
    orden             int NOT NULL,                  -- posición del fragmento dentro del documento
    texto             text NOT NULL,
    embedding         vector(768) NOT NULL,
    modelo_embedding  text NOT NULL,                 -- por ejemplo gemini-embedding-001
    hash_documento    text NOT NULL,                 -- huella SHA-256 del documento al cargarlo
    cargado_en        timestamptz NOT NULL DEFAULT now()
);
-- Índice para buscar rápido por parecido (distancia de coseno).
CREATE INDEX ON fragmentos_conocimiento USING hnsw (embedding vector_cosine_ops);

-- Tickets: se usan desde la etapa 3. Escalamiento, muestreo y calificación son columnas, no tablas.
-- Curso: escalamiento (2.5), indicadores (3.2), muestreo (3.3) y equipo híbrido (Módulo 4).
CREATE TABLE tickets (
    id                    serial PRIMARY KEY,
    agente_id             int NOT NULL REFERENCES registro_agentes(id),
    cliente_id            int NOT NULL REFERENCES clientes(id),
    texto                 text NOT NULL,
    estado                text NOT NULL DEFAULT 'nuevo'
                          CHECK (estado IN ('nuevo', 'respondido', 'resuelto', 'resuelto_sin_confirmar', 'escalado')),
    creado_en             timestamptz NOT NULL DEFAULT now(),
    cerrado_en            timestamptz,
    respuesta             text,
    motivo_escalamiento   text,
    resumen_escalamiento  text,
    escalado_por          text CHECK (escalado_por IN ('modelo', 'regla')),
    minutos_persona       numeric,                   -- tiempo de la persona en un caso escalado
    tokens_entrada        int NOT NULL DEFAULT 0,
    tokens_salida         int NOT NULL DEFAULT 0,
    costo_tokens          numeric NOT NULL DEFAULT 0, -- en dólares
    csat                  int CHECK (csat BETWEEN 1 AND 5),
    en_muestra            boolean NOT NULL DEFAULT false,
    revisado_por          text,
    error_encontrado      boolean,
    categoria_error       text
);

-- Conversación de cada ticket, para que la persona que recibe un caso escalado vea todo.
CREATE TABLE mensajes (
    id         serial PRIMARY KEY,
    ticket_id  int NOT NULL REFERENCES tickets(id),
    quien      text NOT NULL CHECK (quien IN ('cliente', 'agente', 'persona')),
    texto      text NOT NULL,
    creado_en  timestamptz NOT NULL DEFAULT now()
);

-- Audit trail: qué decidió el agente y por qué (Módulo 1, pregunta 9); "con qué datos"
-- es una ampliación del proyecto. También las intervenciones humanas (sección 3.4).
-- Se usa desde la etapa 4.
-- ticket_id queda vacío en intervenciones que no son de un ticket (detener el agente, cambio externo).
CREATE TABLE registro_auditoria (
    id              bigserial PRIMARY KEY,
    agente_id       int NOT NULL REFERENCES registro_agentes(id),
    ticket_id       int REFERENCES tickets(id),
    paso            int,
    tipo            text NOT NULL CHECK (tipo IN ('modelo', 'herramienta', 'regla', 'intervencion', 'cambio_externo')),
    decision        text NOT NULL,
    datos_usados    jsonb,
    motivo          text,
    version_prompt  text,
    tokens          int,
    quien           text,                            -- la persona, en las intervenciones humanas
    creado_en       timestamptz NOT NULL DEFAULT now()
);
