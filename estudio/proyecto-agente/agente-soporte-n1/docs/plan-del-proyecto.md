# Plan y reglas del proyecto: Agente de Soporte N1

Este es el documento que manda en el desarrollo del agente. Si `referencia/arquitectura.md` o `referencia/ruta-de-construccion.md` dicen otra cosa, vale lo que dice este archivo; la sección “Qué cambia respecto de la ruta y la arquitectura” dice exactamente en qué. Se actualiza cada vez que el usuario pide un cambio, y cada cambio se anota en el registro del final.

**Estado (2026-11-18):** etapas 0 y 1 listas y probadas por el usuario con el modelo real, `gemini-3.1-flash-lite` (ver `pruebas/2026-11-18-etapas-0-y-1.md`). Siguiente: etapa 2, la base de conocimiento.

**Propósito (decisión del usuario):** entender en simple el flujo completo de un agente gobernado por las reglas del curso y el esfuerzo que hay detrás. El proyecto tiene lo mínimo que haga falta para eso: ni más piezas, ni menos que las que exige el curso.

**Principio rector (decisión del usuario, manda sobre todas las reglas):** todos los conceptos del curso, a escala pequeña. Cada exigencia del curso tiene su pieza en el proyecto, pero con la infraestructura mínima: PostgreSQL resuelve todo lo que pueda (datos, vectores, banderas, métricas y tendencias). Las herramientas de escala (colas, workers, cachés, plataformas de monitoreo) se postergan hasta que el volumen las justifique, porque suman complejidad sin enseñar nada nuevo del curso; la tabla de lo postergado dice cuándo agregar cada una.

## El flujo completo, en simple

Todo el proyecto se resume en este recorrido. Cada paso dice qué parte del curso aplica.

**Antes de que el agente atienda a nadie (Módulo 2):**

1. **Se define quién es el agente:** nombre, rol, alcance, permisos, restricciones y cuándo escala; queda anotado en el registro de agentes, con su dueño, su área y su nivel de autonomía (secciones 2.2, 2.7 y 1.2).
2. **Se escriben sus instrucciones:** el system prompt JD+SOP, que dice qué lograr y cómo, paso a paso (sección 2.5).
3. **Se le dan solo tres herramientas:** buscar al cliente, buscar una solución documentada y pasar el caso a una persona (sección 2.3, permisos mínimos).
4. **Se cargan los documentos de soporte** que el agente puede consultar: la base de conocimiento. Con el paso 8, esto forma un RAG: el agente busca en esos documentos antes de responder (el término no viene en el curso; ver el glosario).
5. **Se prueba antes de usarlo:** casos funcionales, de límites, adversariales, de escalamiento y de métricas. Si pasan, el AI Agent Manager, el usuario, aprueba esa versión con su nombre (sección 2.6).
6. **Se guarda la línea base:** cómo se atendía sin el agente, para poder comparar después (secciones 3.7, 5.2 y 5.3).

**Cada vez que llega un ticket:**

7. El cliente escribe su problema. El agente revisa si está detenido (kill switch) y si el caso ya superó 8 minutos.
8. El agente conversa con el modelo y usa sus herramientas; cada paso queda en el registro de auditoría: qué decidió, con qué datos y por qué (Módulo 1, pregunta 9).
9. Las reglas graves las revisa el código, no el modelo: cancelación, descuentos, cambios de cuenta, tiempo. Si corresponde, el caso pasa a una persona con todo el contexto (sección 2.5 y Módulo 4, equipo híbrido). Los cambios de cuenta siempre esperan confirmación humana: es el punto de verificación obligatoria antes de una acción de alto impacto (sección 3.3).
10. Si el agente responde, el cliente confirma si se resolvió y lo califica de 1 a 5. Solo entonces cuenta como resuelto (decisión del proyecto, no viene en el curso).

**Después, el trabajo del AI Agent Manager (Módulo 3):**

11. **Revisa una muestra** del 10% de los casos y anota si hubo errores y de qué tipo, porque las métricas no ven los fallos silenciosos; además compara con los primeros 30 días para detectar la deriva de comportamiento (sección 3.3).
12. **Mira el dashboard:** en menos de 90 segundos sabe si el agente genera valor, con 5 paneles y un semáforo (sección 3.5).
13. **Decide si interviene o deja correr,** según 5 señales con valores fijos; si hay riesgo, revisa las instrucciones (sección 3.4) o detiene el agente con el kill switch (secciones 1.2 y 4.5).
14. **Calcula el valor:** costo por caso, horas ahorradas y ROI, para defender el agente ante la dirección (secciones 3.2 y 5.1 a 5.3).

## Reglas de desarrollo (decisiones del usuario)

1. **Lenguaje y framework:** Python con FastAPI, en su forma más simple: funciones normales, sin `async` ni inyección de dependencias, y modelos Pydantic pequeños solo donde llegan datos (ver `decisiones.md`, D7).
2. **Simple para poder seguirlo:** una persona debe poder seguir el código de principio a fin. Se permiten patrones o principios solo cuando simplifican; se evitan capas, abstracciones o indirecciones que obligan a saltar entre muchos archivos para entender un flujo. Ante la duda, lo que se lee de corrido.
3. **La menor cantidad de código posible,** cubriendo todo lo que exige el curso. Antes de agregar una librería, un archivo, una tabla o un servicio, se pregunta si el curso lo exige o si sin él no funciona.
4. **Código comentado:** cada archivo empieza con un comentario que dice qué hace y en qué etapa aparece. Cada función lleva un docstring corto en lenguaje simple que dice qué hace y a qué parte del curso responde, con módulo y sección (“Curso: protocolos de escalamiento, Módulo 2, sección 2.5.”). Si la función es puramente técnica, dice “Técnico: no viene del curso.” Los scripts `.bat` dicen en su comentario inicial en qué etapa aparecen. El prompt es texto para el modelo, no código: no lleva esos comentarios.
5. **Variables de entorno:** en `src/docker/.env`, que nunca se sube al repositorio. `src/docker/example.env` es la fuente oficial de los nombres de las variables, con comentarios y sin valores reales.
6. **Docker Compose** en `src/docker/`.
7. **La documentación se actualiza con cada cambio (pedido del usuario):** este plan (estado, etapas y registro de cambios), `diagramas-del-codigo.md` cuando cambia el código, `decisiones.md` cuando se toma una decisión técnica, el `README.md` del proyecto, el mapa `docs/README.md` cuando cambia un documento y `docs/pruebas/` cuando se prueba algo. Ningún cambio de código se da por terminado sin su documentación.
8. **Nombres en español,** con el vocabulario del curso (`escalar_a_humano`, `buscar_solucion`, `registro_auditoria`); también las funciones de entrada de los scripts. Quedan en inglés solo los nombres que imponen las librerías.
9. **Frontend en HTML y JavaScript simple,** sin framework ni compilación, entregado por el mismo FastAPI.
10. **Documentos ficticios** en `src/base-de-conocimiento/`, generados a partir de una lista que el usuario aprueba antes. Nunca información real: el repositorio es público.
11. **Dos formas de levantar el proyecto (forma de trabajo del usuario):** `start-dev.bat` es el entorno de desarrollo: la app corre en local con un entorno virtual de Python (`src/backend/.venv`) y el resto de los servicios con Docker Compose. `start-qa.bat` levanta todo en Docker Compose, incluida la app. En el `docker-compose.yml`, el servicio del backend lleva el perfil `qa`: sin perfil, Compose levanta solo PostgreSQL (dev); con `--profile qa`, también el backend (qa). `clear.bat` libera espacio: borra el entorno virtual con sus librerías y las cachés de Python y de `pytest` y, si el usuario confirma, los contenedores, volúmenes (los datos de la base) e imágenes de Docker del proyecto; nunca borra el código, los documentos ni el `.env`.
12. **La consola se mantiene en todas las etapas (pedido del usuario):** `consola.py` sigue siendo la forma rápida de probar al agente aunque exista la API. La consola y la API llaman a la misma función del agente (`agente.py`, desde la etapa 3), así que lo que se prueba en la consola es lo que hace la API; la consola no necesita que la API esté corriendo (ver `decisiones.md`, D6).
13. **Solo licencias permisivas (regla muy importante del usuario):** toda librería, imagen de Docker o herramienta que use el proyecto debe tener licencia MIT, BSD, Apache 2.0 o similar (ISC, PostgreSQL, PSF, MIT-0, 0BSD). No se usan licencias con copyleft, como GPL, LGPL, AGPL o SSPL, ni licencias de “código disponible” como RSAL. Antes de agregar una librería se revisa su licencia y la de las librerías que trae consigo (ver “Licencias”). Excepciones aceptadas por el usuario: la MPL 2.0 de `certifi` y `tqdm`, porque no se modifican, y Grafana (AGPL), si se agrega, porque el proyecto no se vende como producto.
14. **Reglas del repositorio:** commits y push solo cuando el usuario los pide, uno por etapa; mensajes con el formato Conventional Commits, por ejemplo `feat(agente): agrega la base de conocimiento en pgvector` (ver `AGENTS.md`); sin firmas de agentes ni menciones del asistente.

## Estructura de carpetas

```text
estudio/proyecto-agente/
└── agente-soporte-n1/
    ├── README.md                       # qué es y cómo probarlo
    ├── start-dev.bat                   # dev: app en local (entorno virtual) y servicios en Docker
    ├── start-qa.bat                    # qa: todo en Docker, incluida la app (funciona desde la etapa 6)
    ├── clear.bat                       # limpieza: entorno virtual, cachés y, si se confirma, Docker
    ├── docs/
    │   ├── README.md                   # el mapa de docs: qué leer primero y cómo se relacionan
    │   ├── plan-del-proyecto.md        # este archivo: las reglas y el diseño que mandan
    │   ├── diagramas-del-codigo.md     # archivos, funciones y quién llama a quién; se actualiza en cada etapa
    │   ├── decisiones.md               # decisiones técnicas: problema, opciones, elección y por qué
    │   ├── referencia/                 # versión futura (arquitectura.md) y diseño anterior (ruta-de-construccion.md)
    │   ├── pruebas/                    # registros de las pruebas manuales de cada etapa
    │   └── revisiones/                 # informes de revisión del plan y del código
    └── src/
        ├── base-de-conocimiento/       # documentos de soporte ficticios (.md)
        ├── .dockerignore               # etapa 6: deja fuera de la imagen el .env, el entorno virtual y las cachés
        ├── backend/
        │   ├── src/                    # todo el código Python, archivos sueltos sin paquetes
        │   ├── tests/                  # pruebas
        │   ├── requirements.txt
        │   └── Dockerfile              # etapa 6
        ├── frontend/
        │   └── src/                    # HTML, JavaScript y CSS
        └── docker/
            ├── docker-compose.yml      # etapa 2: postgres; etapa 6: se suma el backend
            ├── .env                    # valores reales, ignorado por git
            ├── example.env             # fuente oficial de las variables
            └── postgres/
                ├── 01_esquema.sql          # tablas (se ejecuta primero)
                └── 02_datos_ficticios.sql  # agente, clientes, línea base e historial
```

Los SQL llevan número porque PostgreSQL los ejecuta en orden alfabético, y el esquema debe ir antes que los datos. Solo se ejecutan la primera vez que se crea el volumen: mientras no haya datos reales, para cambiar el esquema se edita el SQL y se recrea todo con `docker compose down -v`.

El código corre de dos formas: en local, con `start-dev.bat` (servidor de base de datos `localhost`), y dentro de Docker, con `start-qa.bat` desde la etapa 6 (servidor `postgres`). Por eso, desde la etapa 2, `config.py` armará la conexión con la variable `POSTGRES_HOST`, que vale `localhost` por defecto y `postgres` dentro del compose. Desde la etapa 6, el backend se construye con la carpeta `src/` completa como contexto, porque necesita leer `frontend/src/` y `base-de-conocimiento/`; el archivo `src/.dockerignore` evita que el `.env` y el entorno virtual entren en la imagen.

**El compose de la etapa 2:** un solo servicio, `postgres`, con la imagen `pgvector/pgvector:pg17`; usuario, contraseña y base salen del `.env` (`${POSTGRES_USER}`, `${POSTGRES_PASSWORD}`, `${POSTGRES_DB}`); la carpeta `postgres/` se monta en `/docker-entrypoint-initdb.d` para que los SQL se ejecuten al crear el volumen; los datos quedan en un volumen con nombre; y el puerto se publica solo en el equipo (`127.0.0.1:5432:5432`). `POSTGRES_PASSWORD` es obligatoria: la imagen no arranca sin ella.

## Qué cambia respecto de la ruta y la arquitectura

`referencia/arquitectura.md` muestra la versión completa a futuro, y `referencia/ruta-de-construccion.md` explica cada pieza con código de referencia de un diseño anterior. Para esta versión mandan estas equivalencias:

| Tema | Ruta o arquitectura | Esta versión |
|---|---|---|
| Documentos de soporte | `kb/` | `src/base-de-conocimiento/` |
| Prompt | `prompts/soporte-n1.md` | `src/backend/src/prompt_soporte_n1.md` |
| Esquema | `sql/001_esquema.sql`, tablas en inglés | `src/docker/postgres/01_esquema.sql`, tablas en español (ver “Modelo de datos”) |
| Variables | `.env.example` | `src/docker/example.env` |
| Compose | en la raíz, con credenciales escritas | en `src/docker/`, con variables del `.env` |
| Clientes del CRM | `datos/clientes.json` o servicio mock-crm | tabla `clientes` |
| Código | paquete con imports relativos | archivos sueltos en `backend/src/`, se ejecutan con `python src/archivo.py` |
| Conexión a PostgreSQL | `psycopg` (licencia LGPL), `pgvector` y `numpy` | `pg8000` (licencia BSD), por la licencia; los vectores se envían como texto y se convierten en SQL con `::vector`, sin librerías extra (ver `decisiones.md`, D1 y D2) |
| Embeddings | librería `google-genai` y `GEMINI_API_KEY` | la misma librería `openai` y la misma clave del chat |
| API | asíncrona, responde `202` y una cola atiende | síncrona: atiende en el mismo pedido |
| Etapa 7 | Redis, worker, Grafana, kill switch en Redis | frontend y supervisión; lo demás queda postergado |
| Seguridad | `API_CLAVE` | sin autenticación en el frontend ni en el backend, solo en el equipo local (ver `decisiones.md`, D4) |
| Archivos de código | `llm.py`, `embeddings.py`, `db.py`, `auditoria.py`, `ingest.py`, `bucle.py`, `guardrails.py` | `modelo.py` (chat y embeddings), `base_de_datos.py` (conexión y auditoría), `cargar_conocimiento.py`, `agente.py`, `reglas.py` |
| Tablas | `kb_documentos`, `kb_chunks`, `escalations`, `audit_log`, `prompt_versions` | `fragmentos_conocimiento` (con columna `documento`), columnas de escalamiento en `tickets`, `registro_auditoria`, `version_prompt` en `registro_agentes` |
| Conexión a la base | `DATABASE_URL` | variables `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` y `POSTGRES_HOST`; `config.py` arma la conexión |
| Embeddings, parámetros | 768 números, normalizados, `task_type` | 768 números pedidos con el parámetro `dimensions` (se comprueba en la etapa 2; si el proveedor no lo acepta, se ajusta la columna al tamaño que entregue), sin normalizar porque la distancia de coseno no lo necesita, sin `task_type`; fragmentos de unos 1.200 caracteres con 200 de solape; índice HNSW; 5 resultados por búsqueda |

## Etapas de esta versión

| Etapa | Qué se construye | Archivos nuevos y archivos que cambian | Listo cuando |
|---|---|---|---|
| 0 | Conexión con el modelo | `config.py`, `modelo.py`, `prueba_conexion.py`, `example.env`, `start-dev.bat`, `start-qa.bat`, `clear.bat` | el modelo responde un saludo |
| 1 | Agente en la terminal con su JD+SOP | `consola.py`, `prompt_soporte_n1.md` | ante “quiero cancelar” responde que una persona seguirá el caso |
| 2 | Base de conocimiento en pgvector (el RAG) | nuevos: `docker-compose.yml`, `01_esquema.sql`, `02_datos_ficticios.sql`, `base_de_datos.py` (`conectar()`, `buscar_fragmentos()`), `cargar_conocimiento.py`, `probar_busqueda.py`, los documentos aprobados; cambian: `modelo.py` (`crear_embedding()`), `config.py` (variables `POSTGRES_*` y `LLM_MODELO_EMBEDDINGS`), `requirements.txt` (`pg8000`) | cada embedding tiene 768 números y “no puedo entrar” encuentra el documento de contraseñas |
| 3 | Herramientas y bucle del agente | `herramientas.py`, `agente.py` | resuelve con documentos o escala con el contexto completo |
| 4 | Reglas en código, auditoría y kill switch | nuevos: `reglas.py` (incluye `escalar_vencidos()`); cambia: `base_de_datos.py` (`registrar_paso()`) | cada ticket se puede explicar con el registro de auditoría |
| 5 | Pruebas y aprobación del prompt | `tests/`, `aprobar_prompt.py` | pasan las pruebas y la versión queda aprobada con nombre |
| 6 | API REST y Docker | `api.py`, `Dockerfile`, `src/.dockerignore`, perfil `qa` en el compose | con curl se crea un ticket, se responde y se califica, tanto con `start-dev.bat` como con `start-qa.bat` |
| 7 | Frontend y supervisión | `frontend/src/`, `supervision.py` | el dashboard dice en menos de 90 segundos si el agente genera valor |

## Modelo de datos

Seis tablas, la versión mínima que cubre el curso. Escalaciones, revisiones del muestreo y calificaciones son columnas del ticket, no tablas aparte. Cada tabla tiene un `id` numérico; las uniones son `tickets.agente_id`, `tickets.cliente_id`, `mensajes.ticket_id`, `registro_auditoria.agente_id` y `registro_auditoria.ticket_id`.

- **`registro_agentes`:** nombre, rol, alcance, `fuera_de_alcance` (lo que el agente no atiende), nivel de autonomía, dueño (el AI Agent Manager), `area_responsable`, permisos con la justificación de cada uno, restricciones, `version_prompt`, `aprobado_por`, `fecha_aprobacion` (la última validación), `fecha_ultima_auditoria`, `detenido` (el kill switch), `motivo_detencion`, metas o métricas de éxito (resolución autónoma, escalamiento, tiempo, CSAT) y línea base (casos por día, minutos por caso y costo por caso antes del agente). Curso: secciones 1.2, 2.2, 2.6, 2.7 y 3.7, y responsabilidades 3 y 5 del Módulo 2.
- **`clientes`:** el CRM simulado, de solo lectura para el agente: `codigo` (el ID visible que da el cliente, con el formato `C-001`), nombre, empresa, plan contratado e historial. Curso: sección 2.3.
- **`fragmentos_conocimiento`:** documento, orden, texto y `embedding vector(768)`. Curso: sección 2.5, base de conocimiento.
- **`tickets`:** `agente_id`, `cliente_id`, texto, `estado`, `creado_en`, `cerrado_en`, `respuesta`, `motivo_escalamiento`, `resumen_escalamiento`, `escalado_por` (el modelo o una regla), `minutos_persona` (tiempo de la persona que atendió un caso escalado), `tokens_entrada`, `tokens_salida`, `costo_tokens`, `csat` (1 a 5), `en_muestra`, `revisado_por`, `error_encontrado` y `categoria_error`. Curso: secciones 2.5, 3.2, 3.3 y Módulo 4.
- **`mensajes`:** la conversación de cada ticket (quién habló y qué dijo), para que la persona que recibe un caso escalado vea todo el contexto.
- **`registro_auditoria`:** `agente_id`, `ticket_id` (vacío en las intervenciones que no son de un ticket: detener o reactivar el agente y registrar un cambio externo), paso, tipo (modelo, herramienta, regla, intervención, cambio externo), decisión, datos usados, motivo, versión del prompt, tokens, quién (para las intervenciones humanas) y fecha. Curso: Módulo 1, pregunta 9 (audit trail), y sección 3.4 (intervenciones).

## Cómo funciona cada regla

- **Estados del ticket:** `nuevo`, `respondido` (el agente contestó), `resuelto` (el cliente confirmó) o `escalado` (pasó a una persona). Si el cliente no confirma en 24 horas, el ticket queda `resuelto_sin_confirmar` y no cuenta en la resolución autónoma, para no inflar la métrica (decisión del proyecto, no viene en el curso, inspirada en los fallos silenciosos de la sección 3.3). Lo marca `escalar_vencidos()` junto con los tickets que superaron los 8 minutos.
- **Los 8 minutos:** se miden desde `creado_en`. El código revisa el tiempo antes de cada paso, y cada llamada al modelo tiene un límite de 60 segundos, sin reintentos automáticos, para que nunca quede colgada. Además, al abrir la cola o el dashboard, `escalar_vencidos()` (en `reglas.py`) escala los tickets vencidos. La cola de escalaciones muestra cuánto lleva esperando cada caso frente a `MINUTOS_RESPUESTA_TRASPASO`, el tiempo de respuesta acordado para el traspaso (sección 4.3, paso 3).
- **Escalar a una persona:** `escalar_a_humano` es código, no texto del modelo: arma el contexto (cliente, conversación, herramientas usadas, motivo, quién escaló y resumen), lo guarda en el ticket y registra el paso en la auditoría.
- **Kill switch:** se revisa al empezar cada ticket y antes de cada paso. Con el agente detenido, los tickets no se rechazan: pasan a una persona con el motivo “agente detenido” (decisión del proyecto, no viene en el curso: el humano atiende lo que el agente no puede, como en el equipo híbrido de la sección 4.2). Cada detención y reactivación queda en la auditoría con quién, cuándo y por qué. Curso: el kill switch aparece en la sección 1.2 (exigido para el Nivel 4) y el circuit breaker en la sección 4.5; para un agente de Nivel 3 es un control más estricto que el mínimo, que el proyecto incluye para practicarlo.
- **Aprobación del prompt:** el programa lee `prompt_soporte_n1.md`, y git guarda su historia. Una versión se usa solo si pasó las pruebas y el usuario la aprobó: `aprobar_prompt.py` corre las pruebas y, si pasan, guarda en `registro_agentes` la versión, quién la aprobó y la fecha (sección 2.6). La primera línea del prompt lleva su número de versión.
- **Nivel de autonomía: Nivel 3, Augmentación.** El curso define el Nivel 3 como el agente que combina herramientas, adapta su enfoque y completa objetivos de varios pasos, que es lo que hace este agente; el Nivel 2 es para tareas bien definidas, como clasificar tickets (sección 1.2). Además, el curso pide sus cinco indicadores de negocio para agentes de Nivel 3 o 4 (sección 3.2). Las plantillas de `estudio/plantillas/` todavía lo describen en Nivel 2; se corrige cuando se revisen.
- **Roles del equipo híbrido (sección 4.5):** en este proyecto el usuario cumple los tres: Agent Owner (responde por el agente), Quality Reviewer (revisa el muestreo) y Ethics Reviewer (puede detener el agente).

## La supervisión del Módulo 3, concreta

**Muestreo (sección 3.3):** al cerrar cada ticket, se marca `en_muestra` al azar con la probabilidad de `PORCENTAJE_MUESTREO_REVISION` (10%). En la página de revisión, el usuario lee el caso y anota si hubo error y su categoría, de una lista cerrada (lista del proyecto; el curso pide categorías, pero no da una lista): solución incorrecta, información inventada, debió escalar y no escaló, escaló sin necesidad, incumplió una restricción y otro.

**Deriva de comportamiento (sección 3.3, Tipo 2):** una consulta compara el muestreo, el CSAT y la tasa de escalamiento de las últimas semanas con los de los primeros 30 días del agente. No hace falta otra tabla.

**CSAT:** la calificación de 1 a 5 que da el cliente al confirmar el ticket.

**Las 5 señales y el semáforo (sección 3.4):**

| Señal | Se interviene cuando |
|---|---|
| Tasa de escalamiento | sube 5% (el proyecto lo interpreta como 5 puntos) y supera la meta del 20%, o se mantiene alta 3 o más días |
| CSAT | baja 0,2 puntos en una semana y coincide con un cambio en las instrucciones o en el volumen o tipo de casos |
| Tiempo de resolución | sube 20% de forma sostenida, sin más volumen que lo explique |
| Cambio externo | siempre: el usuario lo registra a mano y revisa las instrucciones |
| Muestreo | 3 errores en los últimos 50 casos revisados que comparten categoría (lo calcula el sistema) o muestran un patrón en las instrucciones (lo decide el usuario) |

Semáforo (la regla de colores es del proyecto; el curso solo dice “dentro de parámetros, requieren atención, alerta activa”): verde si no hay señales; amarillo si hay una señal que aún no cumple la condición de intervenir (por ejemplo, sube el escalamiento pero lleva menos de 3 días); rojo si alguna exige intervenir o si el agente está detenido.

**Los 5 paneles del dashboard (sección 3.5):** 1, semáforo del agente; 2, resolución autónoma, escalamiento, tiempo promedio y costo por caso frente a la línea base, con tendencia de las últimas 2 semanas; 3, resultado del muestreo: casos revisados, errores por categoría y tendencia; 4, alertas de las 5 señales, en una lista priorizada, cada una con fecha y hora, descripción y acción recomendada, más los escalamientos contados por motivo, para ver si los traspasos se repiten en el mismo punto (sección 4.6); 5, valor acumulado: horas ahorradas, casos resueltos solos, ahorro frente a la línea base e impacto en NPS como proyección. Las tendencias salen de agrupar los tickets por día; no hacen falta tablas extra.

**Costo y valor (secciones 3.2 y 5.1 a 5.3):** el curso define el costo por caso como la inversión total del proceso dividida por el volumen; el proyecto usa una versión simplificada: el costo de tokens, más los minutos de las personas en los casos escalados por su costo por hora, dividido por el número de tickets. Las horas ahorradas son los casos resueltos solos por los minutos por caso de la línea base (fórmula del proyecto; el curso pide las horas, no la fórmula). Los riesgos y la próxima fase del business case (sección 5.3) se muestran como un texto fijo del dashboard. Los precios por millón de tokens y el costo por hora de una persona van en el `.env`. Solo el horizonte 1 del curso (eficiencia) se mide con datos; el NPS y los horizontes 2 y 3 se muestran como proyección, porque un proyecto de estudio no tiene datos para medirlos. La línea base y los tickets históricos de `02_datos_ficticios.sql` son ficticios y van marcados así, para que el dashboard muestre tendencias desde el primer día.

## Pruebas (etapa 5)

Tres grupos, para gastar pocas llamadas al modelo:

1. **Reglas en código, sin modelo:** cancelación, descuento, cambio de cuenta, 8 minutos (con el límite en 0) y kill switch. Son gratis y siempre dan el mismo resultado.
2. **Las 5 dimensiones de la sección 2.6, con el modelo real:** al menos un caso por dimensión y uno por cada condición de escalamiento del SOP (sin resolución documentada, cancelación y tiempo), con `temperature=0`, y cada caso se repite 3 veces y vale la mayoría.
3. **Métricas:** unos 20 tickets con una mezcla realista (la mayoría con solución documentada), comparados con las metas: resolución autónoma de 80% o más, escalamiento de 20% o menos y tiempo promedio de 3 minutos o menos. El CSAT no se puede medir en las pruebas, porque lo da el cliente.

Antes de empezar, las pruebas verifican que PostgreSQL responde y que la base de conocimiento está cargada.

## Qué pide el curso y dónde se cubre

| Exigencia del curso | Sección | Dónde se cubre | Etapa |
|---|---|---|---|
| Nivel de autonomía definido (Nivel 3) | 1.2 | `registro_agentes` | 2 |
| Identidad: nombre, rol, alcance y fuera de alcance, permisos, restricciones, escalamiento y métricas de éxito | 2.2 | `registro_agentes` y prompt | 1 y 2 |
| Permisos mínimos | 2.3 | tres herramientas; el cliente sale del ticket, no del modelo | 3 |
| Instrucciones JD+SOP | 2.5 | `prompt_soporte_n1.md`; el componente 7, las métricas, vive en `registro_agentes` | 1 |
| Validación antes de producción y aprobación del manager | 2.6 | pruebas y `aprobar_prompt.py` | 5 |
| Registro de agentes contra el agent sprawl | 2.7 | `registro_agentes` | 2 |
| Audit trail | Módulo 1, pregunta 9 | `registro_auditoria` | 4 |
| Escalamiento con contexto completo | 2.5 y Módulo 4 | `escalar_a_humano` y cola de escalaciones | 3 y 7 |
| Indicadores de negocio y CSAT | 3.2 | consultas de `supervision.py` | 7 |
| Muestreo contra fallos silenciosos | 3.3 | `en_muestra` y página de revisión | 7 |
| Deriva de comportamiento contra los primeros 30 días | 3.3 | consulta de `supervision.py` | 7 |
| Verificación obligatoria antes de una acción de alto impacto | 3.3 | los cambios de cuenta esperan confirmación humana | 4 |
| Señales de intervención | 3.4 | `supervision.py` | 7 |
| Kill switch o circuit breaker | 1.2 y 4.5 | `detenido` en `registro_agentes` | 4 |
| Dashboard de 5 paneles | 3.5 | página del frontend | 7 |
| Línea base | 3.2, 3.7, 5.2 y 5.3 | `registro_agentes` y datos ficticios | 2 |
| Tiempo de respuesta del traspaso y traspasos por motivo | 4.3 y 4.6 | `MINUTOS_RESPUESTA_TRASPASO`, cola de escalaciones y panel 4 | 7 |
| Roles asignados: Agent Owner, Quality Reviewer, Ethics Reviewer | 4.5 | el usuario cumple los tres | 2 |
| Costo por caso, horas ahorradas y ROI | 3.2 y 5.1 a 5.3 | tokens guardados y fórmulas de `supervision.py` | 3 y 7 |

## Licencias

Revisión del 2026-11-18, leída de los metadatos de cada paquete instalado (`pip show`). Antes de agregar una librería se repite la revisión con ella y con las que trae consigo.

| Pieza | Licencia | Estado |
|---|---|---|
| `openai` | Apache 2.0 | en uso |
| `python-dotenv` | BSD 3 | en uso |
| `pg8000` y sus dependencias (`scramp`, `asn1crypto`, `python-dateutil`) | BSD 3, MIT-0, MIT, BSD 3 | etapa 2 |
| `fastapi`, `starlette`, `pydantic` | MIT, BSD 3, MIT | etapa 6 |
| `uvicorn` | BSD 3 | etapa 6 |
| `pytest`, `PyYAML` | MIT, MIT | etapa 5 |
| Dependencias de `openai`: `httpx`, `httpcore`, `anyio`, `distro`, `jiter`, `sniffio`, `idna`, `typing_extensions` | BSD, MIT o Apache 2.0, PSF | en uso |
| Dependencias de `openai`: `certifi` y `tqdm` | MPL 2.0 (`tqdm`: MPL 2.0 y MIT) | en uso; aceptadas por el usuario, porque no se modifican |
| Imagen `pgvector/pgvector` (PostgreSQL y la extensión pgvector) | Licencia PostgreSQL, permisiva | etapa 2 |
| `psycopg` | LGPL 3.0 | descartada: se reemplaza por `pg8000` |
| `pgvector` (librería de Python) y `numpy` | MIT y BSD | no hacen falta: los vectores se convierten en SQL con `::vector` (ver `decisiones.md`, D2) |

La MPL 2.0 es un copyleft débil por archivo: solo obliga a compartir los cambios hechos a los propios archivos de esa librería, y no afecta al código del proyecto. `certifi` (los certificados para conectarse por HTTPS) y `tqdm` vienen obligatoriamente con `openai`; el usuario las aceptó porque no se modifican.

El porqué de `pg8000`, de guardar los vectores como texto convertido con `::vector` y de cada excepción está explicado, con sus opciones y ejemplos, en `decisiones.md` (decisiones D1, D2 y D3).

## Lo que se deja fuera en esta versión, por qué y cuándo agregarlo

Lo que se saca no se descarta: se posterga, y esta tabla recuerda por qué y qué señal indica que llegó el momento.

| Pieza postergada | Qué se usa en su lugar | Por qué se saca ahora | Cuándo agregarla |
|---|---|---|---|
| Cola de casos (Valkey) | la API atiende el ticket en el mismo pedido | con pocos tickets la cola no aporta y suma un servicio | cuando la atención de un ticket tarde más de 30 segundos con frecuencia, o lleguen varios tickets a la vez. Se usará Valkey (decisión del usuario): una copia de Redis con licencia BSD, que funciona igual; Redis desde la versión 8 usa AGPL, RSAL o SSPL |
| agent-worker separado | el bucle corre dentro del backend | sin cola, el worker no tiene trabajo propio | junto con Valkey |
| Kill switch en Valkey | columna `detenido` en `registro_agentes` | la base de datos ya existe y basta para una bandera | con Valkey, o con varios servidores |
| mock-crm como servicio | tabla `clientes` | un servicio aparte simularía lo mismo con más código | cuando se conecte un CRM real |
| Grafana | dashboard propio en el frontend | el curso pide 5 paneles concretos que se arman con pocas consultas | con más agentes, o si se necesitan alertas automáticas e historia larga. Licencia: Grafana es AGPL; el usuario lo acepta como excepción porque el proyecto no se vende como producto |
| Langfuse | `registro_auditoria` | el curso pide el audit trail, no una plataforma de trazas | cuando haga falta analizar en detalle prompts, tokens y latencia. Qué es: una herramienta de código abierto que registra cada llamada al modelo (el prompt enviado, la respuesta, los tokens, el costo y la demora) y la muestra en una interfaz web para buscar y comparar. Licencia: MIT, salvo sus módulos empresariales, que no se usarían |
| CI automático | pruebas a mano con `pytest` | no hay flujo de despliegue | cuando el código se publique o lo modifiquen varias personas |
| Autenticación del frontend y del backend | todo corre solo en el equipo local (`127.0.0.1`), sin claves ni usuarios | es un proyecto para entender el curso, y el curso no exige autenticación; con un frontend estático, una clave quedaría expuesta | cuando el sistema se exponga fuera del equipo: en una capa superior, por ejemplo un API gateway o un proxy con autenticación delante del backend, sin cambiar el código del agente; ahí conviene separar el acceso de los clientes del acceso del administrador (kill switch, aprobación del prompt) |
| `task_type` de los embeddings | embeddings sin tipo, por la librería `openai` | se ahorra una librería y una clave | si la búsqueda encuentra mal los documentos |

## Decisiones del usuario

- **Por defecto (2026-11-18):** carpeta `agente-soporte-n1`; un commit por etapa.
- **Recomendaciones de la revisión aceptadas (2026-11-18):** modelo de datos mínimo; el usuario aprueba cada versión del prompt con su nombre, y el programa lee el archivo; sin clave de API, solo en local; un ticket se resuelve cuando el cliente lo confirma y lo califica, con cierre por inactividad que no cuenta como resolución autónoma; NPS como proyección; el agente pasa a Nivel 3; embeddings con la librería `openai`; pruebas en tres grupos, unos 20 casos y 3 repeticiones en los de las 5 dimensiones; documentos ficticios generados a partir de una lista que el usuario aprueba.

## Registro de cambios

- 2026-11-18: versión inicial con las reglas del usuario (Python con FastAPI, código simple y comentado con referencia al curso, `.env` y `example.env`, Docker Compose en `docker`, estructura de carpetas `src/backend/src`, `src/frontend/src` y `src/docker`, la menor cantidad de código cubriendo todo el curso) y las propuestas y preguntas abiertas.
- 2026-11-18: respuestas del usuario: se aceptan las simplificaciones solo para esta versión, con una tabla de lo postergado, por qué y cuándo agregarlo; frontend en HTML y JavaScript simple; nombres en español; documentos ficticios en `src/base-de-conocimiento/`.
- 2026-11-18: aclaración del usuario sobre la regla 2: no se prohíben patrones ni principios; el criterio es que el código se mantenga simple para poder seguirlo.
- 2026-11-18: se crea `agente-soporte-n1/` con la estructura acordada y las etapas 0 y 1; se aplican las decisiones por defecto y se agrega `.env` al `.gitignore`.
- 2026-11-18: a pedido del usuario, los documentos del proyecto pasan a `agente-soporte-n1/docs/`.
- 2026-11-18: el usuario acepta las recomendaciones de la revisión con elephant-goldfish-model y pide entender el flujo completo en simple, con lo mínimo que ayude a entender el curso. Se reescribe el plan: flujo completo en 14 pasos, equivalencias con la ruta, tabla de etapas propia, modelo de datos de seis tablas, cómo funciona cada regla, supervisión del Módulo 3 concreta (muestreo, 5 señales, semáforo, 5 paneles, costo y valor), pruebas en tres grupos, columna de etapa en la cobertura, clave de API y `task_type` postergados, y el agente pasa a Nivel 3.
- 2026-11-18: forma de trabajo del usuario: `start-dev.bat` (app en local con entorno virtual y servicios en Docker Compose) y `start-qa.bat` (todo en Docker Compose); el backend lleva el perfil `qa` en el compose. Se crea `start-dev.bat`; `start-qa.bat` llega en la etapa 6.
- 2026-11-18: regla muy importante del usuario: solo licencias permisivas (MIT, BSD, Apache o similares). Revisión de licencias: `psycopg` (LGPL) se reemplaza por `pg8000` (BSD) y se quitan `pgvector` y `numpy`; `certifi` y `tqdm` (MPL 2.0, dependencias obligatorias de `openai`) quedan a decisión del usuario; Redis y Grafana, postergados, tienen licencias no permisivas y se anotan sus alternativas. Se crea `start-qa.bat`, que funciona desde la etapa 6.
- 2026-11-18: decisiones del usuario sobre licencias: se aceptan `certifi` y `tqdm` (MPL 2.0), porque no se modifican; la cola postergada usará Valkey (BSD) en vez de Redis; Grafana se acepta como excepción (AGPL), porque el proyecto no se vende; Langfuse (MIT) sin problema. Se explica en el plan cómo se guardan los vectores con `pg8000` y `::vector`.
- 2026-11-18: a pedido del usuario se crea `decisiones.md`, con el razonamiento de las decisiones técnicas: D1 (`pg8000` en vez de `psycopg`, solo por la licencia; ninguna de las dos maneja vectores por sí sola), D2 (vectores como texto convertido con `::vector`, sin `pgvector` ni `numpy`) y D3 (excepciones y reemplazos de la regla de licencias). Se corrige la explicación del plan, que mezclaba las dos primeras.
- 2026-11-18: a pedido del usuario se crea `clear.bat` para liberar espacio. El usuario confirma `pg8000` (decisión D1).
- 2026-11-18: decisión del usuario: ni el frontend ni el backend llevan autenticación en esta versión, por ser un proyecto para entender el curso; se deja para una capa superior (API gateway o similar) cuando se exponga fuera del equipo (decisión D4).
- 2026-11-18: el usuario pregunta si el proyecto incluye un RAG. Sí: la base de conocimiento y la herramienta `buscar_solucion` (etapas 2 y 3) forman un RAG; se anota en el flujo y se agrega “RAG” al glosario.
- 2026-11-18: el usuario elige el modelo `gemini-3.1-flash-lite` (texto: 0,25 dólares de entrada y 1,50 de salida por millón de tokens); queda como decisión D5 y como valores por defecto en `example.env`. La etapa 0 quedó probada con el modelo real.
- 2026-11-18: el usuario prueba las etapas 0 y 1 y quedan aprobadas; el registro está en `pruebas/2026-11-18-etapas-0-y-1.md`. La prueba muestra que, sin herramienta, el agente afirma haber escalado y le muestra al cliente el resumen interno: confirma que `escalar_a_humano` debe ser código (etapas 3 y 4).
- 2026-11-18: pedido del usuario: la consola se mantiene como herramienta de prueba en todas las etapas; la consola y la API usan la misma función del agente (regla 12 y decisión D6). Las reglas de licencias y del repositorio pasan a ser la 13 y la 14.
- 2026-11-18: se crea `diagramas-del-codigo.md` (código de hoy, un mensaje de la consola, el código al terminar la versión 1 y las seis tablas), que se actualiza al terminar cada etapa. El usuario prueba `clear.bat` y `start-qa.bat`: correctos.
- 2026-11-18: revisión de consistencia (elephant-goldfish-model) y de fidelidad al curso, guardadas en `revisiones/`. Se agrega el principio rector (todos los conceptos del curso, a escala pequeña); `arquitectura.md` y `ruta-de-construccion.md` pasan a `referencia/` con avisos; se corrigen citas (audit trail: Módulo 1, pregunta 9; kill switch: secciones 1.2 y 4.5; línea base: 3.2, 3.7, 5.2 y 5.3; señales y paneles completos) y se marca lo que es decisión del proyecto; se completa la etapa 2 (llaves y tipos de las tablas, compose, `POSTGRES_PASSWORD`, equivalencias, archivos que cambian) y se cubren a escala pequeña la deriva de comportamiento, la verificación obligatoria, el tiempo de respuesta del traspaso, los traspasos por motivo, los roles y los campos del registro del agente.
- 2026-11-18: pedido del usuario: la regla 7 pasa a exigir que toda la documentación del proyecto se actualice con cada cambio.
- 2026-11-18: el usuario confirma FastAPI frente a Flask, en su forma más simple; se registra como decisión D7, con una explicación de Pydantic.
- 2026-11-18: decisión del usuario: los commits siguen Conventional Commits 1.0.0 (regla 14).
