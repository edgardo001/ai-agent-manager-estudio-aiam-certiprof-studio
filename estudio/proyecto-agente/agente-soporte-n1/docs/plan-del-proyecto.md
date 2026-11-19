# Plan y reglas del proyecto: Agente de Soporte N1

Este es el documento que manda en el desarrollo del agente. Si `referencia/arquitectura.md` o `referencia/ruta-de-construccion.md` dicen otra cosa, vale lo que dice este archivo; la sección “Qué cambia respecto de la ruta y la arquitectura” dice exactamente en qué. Se actualiza cada vez que el usuario pide un cambio, y cada cambio se anota en el registro del final.

**Estado (2026-11-19):** etapas 0 a 3 terminadas y probadas por el usuario; la etapa 3 (herramientas y bucle del agente) ya tiene aplicada su revisión con EGM y de fidelidad al curso (`revisiones/2026-11-19-revision-etapa-3.md`). Lo probado en cada etapa está en `pruebas/`. Siguiente: los commits de la etapa 3 y la etapa 4.

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
8. El agente conversa con el modelo y usa sus herramientas; cada paso queda en el registro de auditoría: qué decidió y por qué (Módulo 1, pregunta 9) y, como ampliación del proyecto, con qué datos.
9. Las reglas graves las revisa el código, no el modelo: cancelación, descuentos, cambios de cuenta, tiempo. Si corresponde, el caso pasa a una persona con todo el contexto (sección 2.5 y Módulo 4, equipo híbrido). Los cambios de cuenta siempre esperan confirmación humana: es el punto de verificación obligatoria antes de una acción de alto impacto (sección 3.3).
10. Si el agente responde, el cliente confirma si se resolvió y lo califica de 1 a 5. Solo entonces cuenta como resuelto (decisión del proyecto, no viene en el curso).

**Después, el trabajo del AI Agent Manager (Módulo 3):**

11. **Revisa una muestra** del 10% de los casos y anota si hubo errores y de qué tipo, porque las métricas no ven los fallos silenciosos; además compara con los primeros 30 días para detectar la deriva de comportamiento (sección 3.3).
12. **Mira el dashboard:** en menos de 90 segundos sabe si el agente genera valor, con 5 paneles y un semáforo (sección 3.5).
13. **Decide si interviene o deja correr,** según 5 señales con valores fijos; si hay riesgo, revisa las instrucciones (sección 3.4) o detiene el agente con el kill switch (sección 1.2; la 4.5 lo llama circuit breaker).
14. **Calcula el valor:** costo por caso, horas ahorradas y ROI, para defender el agente ante la dirección (secciones 3.2 y 5.1 a 5.3).

## Reglas de desarrollo (decisiones del usuario)

1. **Lenguaje y framework:** Python con FastAPI, en su forma más simple: funciones normales, sin `async` ni inyección de dependencias, y modelos Pydantic pequeños solo donde llegan datos (ver `decisiones.md`, D7).
2. **Simple para poder seguirlo:** una persona debe poder seguir el código de principio a fin. Se permiten patrones o principios solo cuando simplifican; se evitan capas, abstracciones o indirecciones que obligan a saltar entre muchos archivos para entender un flujo. Ante la duda, lo que se lee de corrido.
3. **La menor cantidad de código posible,** cubriendo todo lo que exige el curso. Antes de agregar una librería, un archivo, una tabla o un servicio, se pregunta si el curso lo exige o si sin él no funciona.
4. **Código comentado:** cada archivo empieza con un comentario que dice qué hace y en qué etapa aparece. Cada función lleva un docstring corto en lenguaje simple que dice qué hace y a qué parte del curso responde, con módulo y sección (“Curso: protocolos de escalamiento, Módulo 2, sección 2.5.”). Si la función es puramente técnica, dice “Técnico: no viene del curso.” Los scripts `.bat` dicen en su comentario inicial en qué etapa aparecen. El prompt es texto para el modelo, no código: no lleva esos comentarios.
5. **Variables de entorno:** en `src/docker/.env`, que nunca se sube al repositorio. `src/docker/example.env` es la fuente oficial de los nombres, el orden y los comentarios de las variables, sin valores reales. El `.env` tiene siempre las mismas líneas que la plantilla y solo cambian los valores: `start-dev.bat` avisa si se separan y `python -m scripts.revisar_env --ordenar` los vuelve a alinear (D14).
6. **Docker Compose** en `src/docker/`.
7. **La documentación se actualiza con cada cambio (pedido del usuario):** este plan (estado, etapas y registro de cambios), `diagramas-del-codigo.md` cuando cambia el código, `decisiones.md` cuando se toma una decisión técnica, el `README.md` del proyecto, el mapa `docs/README.md` cuando cambia un documento y `docs/pruebas/` cuando se prueba algo. Ningún cambio de código se da por terminado sin su documentación.
8. **Nombres en español,** con el vocabulario del curso (`escalar_a_humano`, `buscar_solucion`, `registro_auditoria`); también las funciones de entrada de los scripts. Quedan en inglés solo los nombres que imponen las librerías.
9. **Frontend en HTML y JavaScript simple,** sin framework ni compilación, entregado por el mismo FastAPI.
10. **Documentos ficticios** en `src/base-de-conocimiento/`, generados a partir de una lista que el usuario aprueba antes. Nunca información real: el repositorio es público.
11. **Dos formas de levantar el proyecto (forma de trabajo del usuario):** `start-dev.bat` es el entorno de desarrollo: la app corre en local con un entorno virtual de Python (`src/backend/.venv`) y el resto de los servicios con Docker Compose. `start-qa.bat` levanta todo en Docker Compose, incluida la app. En el `docker-compose.yml`, el servicio del backend lleva el perfil `qa`: sin perfil, Compose levanta solo PostgreSQL (dev); con `--profile qa`, también el backend (qa). `clear.bat` libera espacio: borra el entorno virtual con sus librerías y las cachés de Python y de `pytest` y, detiene y borra los contenedores que levantó Docker Compose. Nunca borra las imágenes descargadas, como la de PostgreSQL, para que volver a empezar sea rápido, y conserva los volúmenes (los datos de la base), salvo que se ejecute `clear.bat --borrar-volumenes`, que además pide confirmación (decisiones del usuario); nunca borra el código, los documentos ni el `.env`.
12. **La consola se mantiene en todas las etapas (pedido del usuario):** `consola.py` sigue siendo la forma rápida de probar al agente aunque exista la API. La consola y la API llaman a la misma función del agente (`agente.py`, desde la etapa 3), así que lo que se prueba en la consola es lo que hace la API; la consola no necesita que la API esté corriendo (ver `decisiones.md`, D6).
13. **Solo licencias permisivas (regla muy importante del usuario):** toda librería, imagen de Docker o herramienta que use el proyecto debe tener licencia MIT, BSD, Apache 2.0 o similar (ISC, PostgreSQL, PSF, MIT-0, 0BSD). No se usan licencias con copyleft, como GPL, LGPL, AGPL o SSPL, ni licencias de “código disponible” como RSAL. Antes de agregar una librería se revisa su licencia y la de las librerías que trae consigo (ver “Licencias”). Excepciones aceptadas por el usuario: la MPL 2.0 de `certifi`, `tqdm` e `hypothesis`, porque no se modifican, y Grafana (AGPL), si se agrega, porque el proyecto no se vende como producto.
14. **Reglas del repositorio:** commits y push solo cuando el usuario los pide, uno por etapa; mensajes con el formato Conventional Commits, por ejemplo `feat(agente): agrega la base de conocimiento en pgvector` (ver `AGENTS.md`); sin firmas de agentes ni menciones del asistente.
15. **El agente y los scripts de asistencia van separados (pedido del usuario):** `src/backend/aplicacion/` guarda solo lo que forma parte del agente y entra en la imagen Docker; `src/backend/scripts/` guarda lo que se ejecuta suelto para preparar, probar o estimar. Los scripts pueden importar de `aplicacion`, nunca al revés: si el agente pasa a necesitar la lógica de un script, esa lógica se mueve a `aplicacion/`. Cada script nuevo se agrega a la tabla de `src/backend/scripts/README.md` (ver `decisiones.md`, D10).

## Estructura de carpetas

```text
estudio/proyecto-agente/
└── agente-soporte-n1/
    ├── README.md                       # qué es y cómo probarlo
    ├── start-dev.bat                   # dev: app en local (entorno virtual) y servicios en Docker
    ├── start-qa.bat                    # qa: todo en Docker, incluida la app (funciona desde la etapa 6)
    ├── clear.bat                       # limpieza: entorno virtual, cachés y contenedores; --borrar-volumenes, también los datos
    ├── docs/
    │   ├── README.md                   # el mapa de docs: qué leer primero y cómo se relacionan
    │   ├── plan-del-proyecto.md        # este archivo: las reglas y el diseño que mandan
    │   ├── diagramas-del-codigo.md     # archivos, funciones y quién llama a quién; se actualiza en cada etapa
    │   ├── decisiones.md               # decisiones técnicas: problema, opciones, elección y por qué
    │   ├── pruebas-adversariales.md    # estrategia de pruebas adversariales (Hypothesis) para las etapas 5 y 6
    │   ├── buenas-practicas.md         # prácticas de RAG y de agentes: cuáles se adoptan y en qué etapa
    │   ├── estrategia-de-pruebas.md    # los cinco tipos de prueba, separados y documentados
    │   ├── evals-del-llm.md            # plan de evaluaciones del modelo (evals) para la etapa 5
    │   ├── referencia/                 # versión futura (arquitectura.md) y diseño anterior (ruta-de-construccion.md)
    │   ├── pruebas/                    # registros de las pruebas manuales de cada etapa
    │   └── revisiones/                 # informes de revisión del plan y del código
    └── src/
        ├── base-de-conocimiento/       # documentos de soporte ficticios (.md)
        ├── .dockerignore               # etapa 6: deja fuera de la imagen el .env, el entorno virtual y las cachés
        ├── backend/
        │   ├── aplicacion/             # el agente en sí: paquete Python que entra en la imagen Docker
        │   ├── scripts/                # asistencia que se ejecuta suelta: carga, pruebas manuales, costos (D10)
        │   ├── tests/                  # pruebas: unitarias, integracion, adversariales, evals y e2e
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
                └── 02_datos_ficticios.sql  # agente, clientes y línea base; el historial de tickets, en la etapa 7
```

Los SQL llevan número porque PostgreSQL los ejecuta en orden alfabético, y el esquema debe ir antes que los datos. Solo se ejecutan la primera vez que se crea el volumen: mientras no haya datos reales, para cambiar el esquema se edita el SQL y se recrea todo con `docker compose down -v`.

El código corre de dos formas: en local, con `start-dev.bat` (servidor de base de datos `127.0.0.1`; no `localhost`, que en Windows tarda 2 segundos más, D12), y dentro de Docker, con `start-qa.bat` desde la etapa 6 (servidor `postgres`). Por eso, desde la etapa 2, `config.py` armará la conexión con la variable `POSTGRES_HOST`, que vale `127.0.0.1` por defecto y `postgres` dentro del compose. Desde la etapa 6, el backend se construye con la carpeta `src/` completa como contexto, porque necesita leer `frontend/src/` y `base-de-conocimiento/`; el archivo `src/.dockerignore` evita que el `.env` y el entorno virtual entren en la imagen. Del backend, el `Dockerfile` copia solo `aplicacion/` y `requirements.txt`: los scripts de asistencia quedan fuera (D10).

**El compose de la etapa 2:** un solo servicio, `postgres`, con la imagen `pgvector/pgvector:pg17`; usuario, contraseña y base salen del `.env` (`${POSTGRES_USER}`, `${POSTGRES_PASSWORD}`, `${POSTGRES_DB}`); la carpeta `postgres/` se monta en `/docker-entrypoint-initdb.d` para que los SQL se ejecuten al crear el volumen; los datos quedan en un volumen con nombre; y el puerto se publica solo en el equipo (`127.0.0.1:5432:5432`). `POSTGRES_PASSWORD` es obligatoria: la imagen no arranca sin ella.

## Qué cambia respecto de la ruta y la arquitectura

`referencia/arquitectura.md` muestra la versión completa a futuro, y `referencia/ruta-de-construccion.md` explica cada pieza con código de referencia de un diseño anterior. Para esta versión mandan estas equivalencias:

| Tema | Ruta o arquitectura | Esta versión |
|---|---|---|
| Documentos de soporte | `kb/` | `src/base-de-conocimiento/` |
| Prompt | `prompts/soporte-n1.md` | `src/backend/aplicacion/prompt_soporte_n1.md` |
| Esquema | `sql/001_esquema.sql`, tablas en inglés | `src/docker/postgres/01_esquema.sql`, tablas en español (ver “Modelo de datos”) |
| Variables | `.env.example` | `src/docker/example.env` |
| Compose | en la raíz, con credenciales escritas | en `src/docker/`, con variables del `.env` |
| Clientes del CRM | `datos/clientes.json` o servicio mock-crm | tabla `clientes` |
| Código | paquete con imports relativos | dos paquetes en `backend/`: `aplicacion/` (el agente) y `scripts/` (asistencia), con imports absolutos (`from aplicacion import config`); se ejecutan desde `src/backend` con `python -m aplicacion.consola` o `python -m scripts.<nombre>` (D10) |
| Conexión a PostgreSQL | `psycopg` (licencia LGPL), `pgvector` y `numpy` | `pg8000` (licencia BSD), por la licencia; los vectores se envían como texto y se convierten en SQL con `::vector`, sin librerías extra (ver `decisiones.md`, D1 y D2) |
| Embeddings | librería `google-genai` y `GEMINI_API_KEY` | la misma librería `openai` y la misma clave del chat |
| API | asíncrona, responde `202` y una cola atiende | síncrona: atiende en el mismo pedido |
| Etapa 7 | Redis, worker, Grafana, kill switch en Redis | frontend y supervisión; lo demás queda postergado |
| Seguridad | `API_CLAVE` | sin autenticación en el frontend ni en el backend, solo en el equipo local (ver `decisiones.md`, D4) |
| Archivos de código | `llm.py`, `embeddings.py`, `db.py`, `auditoria.py`, `ingest.py`, `bucle.py`, `guardrails.py` | `modelo.py` (chat y embeddings), `base_de_datos.py` (conexión y auditoría), `cargar_conocimiento.py`, `agente.py`, `reglas.py` |
| Tablas | `kb_documentos`, `kb_chunks`, `escalations`, `audit_log`, `prompt_versions` | `fragmentos_conocimiento` (con columna `documento`), columnas de escalamiento en `tickets`, `registro_auditoria`, `version_prompt` en `registro_agentes` |
| Conexión a la base | `DATABASE_URL` | variables `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` y `POSTGRES_HOST`; `base_de_datos.py` arma la conexión con ellas |
| Embeddings, parámetros | 768 números, normalizados, `task_type` | 768 números pedidos con el parámetro `dimensions` (comprobado el 2026-11-18: Gemini lo acepta por su punto de acceso compatible con OpenAI), sin normalizar porque la distancia de coseno no lo necesita, sin `task_type`; corte por secciones del documento, luego por párrafos y, si un párrafo es muy largo, por caracteres (1.200 con 200 de solape), con el título y la sección antepuestos; índice HNSW; 5 resultados por búsqueda |

## Etapas de esta versión

| Etapa | Qué se construye | Archivos nuevos y archivos que cambian | Listo cuando |
|---|---|---|---|
| 0 | Conexión con el modelo | `config.py`, `modelo.py`, `prueba_conexion.py`, `example.env`, `start-dev.bat`, `start-qa.bat`, `clear.bat` | el modelo responde un saludo |
| 1 | Agente en la terminal con su JD+SOP | `consola.py`, `prompt_soporte_n1.md` | ante “quiero cancelar” responde que una persona seguirá el caso |
| 2 | Base de conocimiento en pgvector (el RAG) | nuevos: `docker-compose.yml`, `01_esquema.sql`, `02_datos_ficticios.sql`, `base_de_datos.py` (`conectar()`, `buscar_fragmentos()`), `cargar_conocimiento.py`, `probar_busqueda.py`, los documentos aprobados; cambian: `modelo.py` (`crear_embedding()`), `config.py` (variables `POSTGRES_*` y `LLM_MODELO_EMBEDDINGS`), `requirements.txt` (`pg8000`) | cada embedding tiene 768 números y “no puedo entrar” encuentra el documento de contraseñas |
| 3 | Herramientas y bucle del agente, con las prácticas adoptadas en `buenas-practicas.md` (citar la fuente, datos separados de las instrucciones, tope de tokens, herramientas desconocidas rechazadas) | nuevos: `herramientas.py` (las tres herramientas; `buscar()` de `probar_busqueda.py` pasa aquí y la usa `buscar_solucion()`), `agente.py`; cambian: `modelo.py` (acepta las herramientas y devuelve los tokens usados), `base_de_datos.py` (funciones de clientes y tickets: todo el SQL sigue en este archivo), `consola.py` (pide el código del cliente y crea el ticket), `estimar_costos.py` (usa los tokens reales de los tickets en vez de los supuestos), `prompt_soporte_n1.md` (el programa le agrega la lista de lo que no atiende, leída de `registro_agentes.fuera_de_alcance`, que es su única fuente) | resuelve con documentos o escala con el contexto completo |
| 4 | Reglas en código, auditoría y kill switch | nuevos: `reglas.py` (incluye `escalar_vencidos()`); cambian: `base_de_datos.py` (`registrar_paso()`), `agente.py` (la huella de las instrucciones en cada paso, con la versión, el proveedor y el modelo; si falta el archivo del prompt, escala; D15) | cada ticket se puede explicar con el registro de auditoría, incluida la versión exacta de las instrucciones que lo atendió |
| 5 | Evals, pruebas adversariales de las reglas y aprobación del prompt | `tests/evals/`, `tests/adversariales/`, `scripts/aprobar_prompt.py` (guarda la huella aprobada y el texto, D15); cambian: `agente.py` (compara la huella en cada mensaje y, con la barrera activa, escala si no coincide), `base_de_datos.py`, `01_esquema.sql` (columna de la huella aprobada) | pasan las pruebas, la versión queda aprobada con nombre y un prompt cambiado sin aprobar no atiende tickets |
| 6 | API REST y Docker | `api.py`, `Dockerfile`, `src/.dockerignore`, perfil `qa` en el compose | con curl se crea un ticket, se responde y se califica, tanto con `start-dev.bat` como con `start-qa.bat` |
| 7 | Frontend y supervisión | `frontend/src/`, `supervision.py` | el dashboard dice en menos de 90 segundos si el agente genera valor |

## Modelo de datos

Seis tablas, la versión mínima que cubre el curso. Escalaciones, revisiones del muestreo y calificaciones son columnas del ticket, no tablas aparte. Cada tabla tiene un `id` numérico; las uniones son `tickets.agente_id`, `tickets.cliente_id`, `mensajes.ticket_id`, `registro_auditoria.agente_id` y `registro_auditoria.ticket_id`.

- **`registro_agentes`:** nombre, rol, alcance, `fuera_de_alcance` (lo que el agente no atiende), nivel de autonomía, dueño (el AI Agent Manager), `area_responsable`, permisos con la justificación de cada uno, restricciones, `version_prompt`, `aprobado_por`, `fecha_aprobacion` (la última validación), `fecha_ultima_auditoria`, `detenido` (el kill switch), `motivo_detencion`, metas o métricas de éxito (resolución autónoma, escalamiento, tiempo, CSAT) y línea base (casos por día, minutos por caso y costo por caso antes del agente). Curso: secciones 1.2, 2.2, 2.6, 2.7 y 3.7, y responsabilidades 3 y 5 del Módulo 2.
- **`clientes`:** el CRM simulado, de solo lectura para el agente: `codigo` (el ID visible que da el cliente, con el formato `C-001`), nombre, empresa, plan contratado e historial. Curso: sección 2.3.
- **`fragmentos_conocimiento`:** documento, `seccion`, orden, texto, `embedding vector(768)`, `modelo_embedding`, `hash_documento` (huella SHA-256 del documento) y `cargado_en`. Curso: sección 2.5, base de conocimiento; el control de modelo, versión y fecha es una práctica de RAG que no viene en el curso (decisión D8).
- **`tickets`:** `agente_id`, `cliente_id`, texto, `estado`, `creado_en`, `cerrado_en`, `respuesta`, `motivo_escalamiento`, `resumen_escalamiento`, `escalado_por` (el modelo o una regla), `minutos_persona` (tiempo de la persona que atendió un caso escalado), `tokens_entrada`, `tokens_salida`, `costo_tokens`, `csat` (1 a 5), `en_muestra`, `revisado_por`, `error_encontrado` y `categoria_error`. Curso: secciones 2.5, 3.2, 3.3 y Módulo 4.
- **`mensajes`:** la conversación de cada ticket (quién habló y qué dijo), para que la persona que recibe un caso escalado vea todo el contexto.
- **`registro_auditoria`:** `agente_id`, `ticket_id` (vacío en las intervenciones que no son de un ticket: detener o reactivar el agente y registrar un cambio externo), paso, tipo (modelo, herramienta, regla, intervención, cambio externo), decisión, datos usados, motivo, versión del prompt, tokens, quién (para las intervenciones humanas) y fecha. Curso: Módulo 1, pregunta 9 (audit trail), y sección 3.4 (intervenciones).

## Cómo funciona cada regla

- **Estados del ticket:** `nuevo`, `respondido` (el agente contestó), `resuelto` (el cliente confirmó) o `escalado` (pasó a una persona). Si el cliente no confirma en 24 horas, el ticket queda `resuelto_sin_confirmar` y no cuenta en la resolución autónoma, para no inflar la métrica (decisión del proyecto, no viene en el curso, inspirada en los fallos silenciosos de la sección 3.3). Lo marca `escalar_vencidos()` (etapa 4).
- **Los 8 minutos (decisión del usuario, 2026-11-19):** se mide el tiempo que el agente tarda en atender **cada mensaje** del cliente, desde que llega; el tiempo que el cliente se demora en contestar no cuenta. Así, el cliente que vuelve 10 minutos después a decir “sigue igual” recibe el segundo intento que pide el paso 5 del SOP del prompt. El curso dice “si el tiempo de resolución supera 8 minutos” (sección 2.5) sin decir desde cuándo; la forma de medirlo es del proyecto. El modelo no tiene reloj: lo controla el código (etapa 4). El código revisa el tiempo antes de cada paso, y cada llamada al modelo tiene un límite de 60 segundos, sin reintentos automáticos, para que nunca quede colgada. Además, al abrir la cola o el dashboard, `escalar_vencidos()` (en `reglas.py`) escala los tickets cuyo último mensaje es del cliente y lleva más de 8 minutos sin respuesta (el agente se cayó a mitad); los tickets `respondido` esperan al cliente y, a las 24 horas sin confirmar, pasan a `resuelto_sin_confirmar`. La cola de escalaciones muestra cuánto lleva esperando cada caso frente a `MINUTOS_RESPUESTA_TRASPASO`, el tiempo de respuesta acordado para el traspaso (sección 4.3, paso 3).
- **Escalar a una persona:** `escalar_a_humano` es código, no texto del modelo: arma el contexto (cliente, conversación, herramientas usadas, motivo, quién escaló y resumen), lo guarda en el ticket y escribe el aviso al cliente; desde la etapa 4, también registra el paso en la auditoría. Si falla una herramienta, el ticket se escala por regla (decisión del usuario, 2026-11-19).
- **Kill switch:** se revisa al empezar cada ticket y antes de cada paso. Con el agente detenido, los tickets no se rechazan: pasan a una persona con el motivo “agente detenido” (decisión del proyecto, no viene en el curso: el humano atiende lo que el agente no puede, como en el equipo híbrido de la sección 4.2). Cada detención y reactivación queda en la auditoría con quién, cuándo y por qué. Curso: el kill switch aparece en la sección 1.2 (exigido para el Nivel 4) y el circuit breaker en la sección 4.5; para un agente de Nivel 3 es un control más estricto que el mínimo, que el proyecto incluye para practicarlo.
- **Aprobación del prompt (D15):** el programa lee `prompt_soporte_n1.md` en cada mensaje, y git guarda su historia. Una versión se usa solo si pasó las pruebas y el usuario la aprobó (secciones 2.6 y 2.7): `aprobar_prompt.py` corre las pruebas y, si pasan, guarda en `registro_agentes` la huella de las instrucciones completas (el archivo más “Lo que no atiendes”), la versión, quién la aprobó y la fecha, y deja el texto aprobado en la auditoría. En cada mensaje, el agente compara la huella del prompt que va a usar con la aprobada y, si no coincide, escala por regla; en desarrollo y en las evals solo lo anota. La primera línea del prompt lleva su número de versión, como etiqueta para las personas. Un cambio de modelo o de proveedor queda anotado, sin bloquear.
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

**Costo y valor (secciones 3.2 y 5.1 a 5.3):** el curso define el costo por caso como la inversión total del proceso dividida por el volumen; el proyecto usa una versión simplificada: el costo de tokens, más los minutos de las personas en los casos escalados por su costo por hora, dividido por el número de tickets. Las horas ahorradas son los casos resueltos solos por los minutos por caso de la línea base (fórmula del proyecto; el curso pide las horas, no la fórmula). Los riesgos y la próxima fase del business case (sección 5.3) se muestran como un texto fijo del dashboard. Los precios por millón de tokens y el costo por hora de una persona van en el `.env`. Solo el horizonte 1 del curso (eficiencia) se mide con datos; el NPS y los horizontes 2 y 3 se muestran como proyección, porque un proyecto de estudio no tiene datos para medirlos. La línea base de `02_datos_ficticios.sql` es ficticia y va marcada así. Los tickets históricos, también ficticios, se agregan en la etapa 7, junto con el dashboard que los usa, para que muestre tendencias desde el primer día.

## Pruebas

Cinco tipos de prueba, cada uno en su carpeta de `src/backend/tests/` y documentado (decisión del usuario): unitarias, de integración, adversariales de robustez, evals del modelo y de punta a punta (e2e). La estrategia, qué cubre cada tipo, cuánto cuesta y cuándo se escribe están en `estrategia-de-pruebas.md`; las evals tienen su plan en `evals-del-llm.md` y las adversariales en `pruebas-adversariales.md`.

Lo esencial para gastar pocas llamadas al modelo:

1. **Sin modelo y gratis:** unitarias (incluidas las reglas en código: cancelación, descuento, cambio de cuenta, 8 minutos con el límite en 0 y kill switch), de integración y adversariales. Se corren a cada cambio.
2. **Con el modelo real (evals):** al menos un caso por dimensión de la sección 2.6 y uno por cada condición de escalamiento del SOP (sin resolución documentada, cancelación y tiempo), con `temperature=0`, repitiendo cada caso 3 veces y valiendo la mayoría; y unos 20 tickets con una mezcla realista, comparados con las metas: resolución autónoma de 80% o más, escalamiento de 20% o menos y tiempo promedio de 3 minutos o menos. El CSAT no se puede medir en las pruebas, porque lo da el cliente.
3. **De punta a punta:** pocos casos del recorrido completo, por la API.

Antes de empezar, las pruebas que lo necesitan verifican que PostgreSQL responde y que la base de conocimiento está cargada.

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
| `pytest` y `PyYAML` | MIT y MIT | `pytest` desde la etapa 3; `PyYAML`, etapa 5 |
| `hypothesis` y su dependencia `sortedcontainers` | MPL 2.0 y Apache 2.0 | etapas 5 y 6; aceptada por el usuario como excepción, porque no se modifica, igual que `certifi` y `tqdm` |
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
| Prácticas de RAG a gran escala: PDF y OCR, búsqueda híbrida, reranking, carga incremental, permisos por documento | documentos en Markdown, búsqueda por significado y recarga completa | a escala pequeña no cambian el resultado (7 de 7 búsquedas correctas) y suman código o costo | cada una tiene su señal en `decisiones.md`, D8 |
| Framework de evals (`deepeval`, `ragas`, `inspect-ai`) | `pytest` y un juez propio de pocas líneas | no suma librerías y deja ver cómo se calcula cada métrica | cuando los casos o las métricas crezcan tanto que el juez propio deje de ser simple; antes, revisar su licencia |
| Anonimizar datos sensibles antes de enviarlos al modelo | datos ficticios, permisos mínimos y la restricción de no compartir datos de otros clientes | ningún dato del proyecto es real | cuando el agente atienda clientes reales o se carguen documentos con datos personales: detectarlos en el propio equipo (patrones con dígito verificador para RUT, correos y teléfonos; un modelo local de reconocimiento de entidades para nombres y direcciones, por ejemplo con Presidio, MIT, revisando la licencia del modelo de idioma, porque los de español de spaCy son GPL; detalle en `anonimizacion-de-datos.md`), reemplazarlos por etiquetas antes de cargarlos o de enviar el texto al modelo, revisar que las respuestas no los muestren y guardar en la auditoría solo lo necesario |
| Leer el prompt desde la base (en vez del archivo) | el archivo dentro de la imagen, con git y la huella aprobada (D15) | crearía dos fuentes de verdad para el mismo texto | cuando haya que cambiar el prompt sin reconstruir la imagen, varias personas o agentes editen prompts, o quien audita no tenga acceso a git |
| Traza completa de cada llamada al modelo | el registro de auditoría con la huella del prompt, los datos usados y el modelo (D15) | de 20 a 80 KB por ticket, copia hasta seis veces los datos del cliente y no permite repetir una respuesta exacta | cuando un caso del muestreo no se pueda explicar con la auditoría; con Langfuse, no con una tabla propia, y después de resolver la anonimización |
| Gestor de secretos (OpenBao) para las claves de API | las claves en el archivo de configuración local, fuera de git y de la imagen, más el guardarraíl del usuario | con un solo equipo y una persona, la credencial para leer el vault quedaría en el mismo lugar que las claves | cuando el sistema salga del equipo local (la misma señal que la autenticación), haya varios servidores o personas con acceso a las claves, o haga falta rotarlas y auditar quién las usa; antes, confirmar su licencia (MPL 2.0) y pedir la excepción. Para el prompt no se retoma (D15) |
| `task_type` de los embeddings | embeddings sin tipo, por la librería `openai` | se ahorra una librería y una clave | si la búsqueda encuentra mal los documentos |
| Ollama (modelos en el propio equipo, MIT) | Gemini u OpenRouter por internet | un modelo local que use bien herramientas necesita memoria y suele ser más lento sin tarjeta gráfica | cuando se quiera costo cero por token o que los datos no salgan del equipo; los embeddings con `nomic-embed-text` (768 números, Apache 2.0) ya se pueden combinar con el chat de otro proveedor (D13). Detalle en `proveedores-de-modelos.md` |
| Respaldo si el proveedor del chat se cae | si el modelo falla, el ticket se escala por regla (etapa 3) | primero hay que poder comparar modelos con las evals (etapa 5) | si las caídas siguen siendo frecuentes después de la etapa 6 (el 2026-11-19 hubo dos llamadas de más de 60 segundos y un error 503 de Gemini): primero, OpenRouter como proveedor del chat, con su enrutamiento, sin código; después, si hace falta, un proveedor de respaldo en `modelo.py` que cambie solo al empezar un mensaje. Balancear entre proveedores no se recomienda, porque mezcla dos agentes en las métricas del Módulo 3 (`proveedores-de-modelos.md`) |

## Decisiones del usuario

- **Por defecto (2026-11-18):** carpeta `agente-soporte-n1`; un commit por etapa.
- **Recomendaciones de la revisión aceptadas (2026-11-18):** modelo de datos mínimo; el usuario aprueba cada versión del prompt con su nombre, y el programa lee el archivo; sin clave de API, solo en local; un ticket se resuelve cuando el cliente lo confirma y lo califica, con cierre por inactividad que no cuenta como resolución autónoma; NPS como proyección; el agente pasa a Nivel 3; embeddings con la librería `openai`; pruebas en tres grupos (hoy, cinco tipos: ver “Pruebas”), unos 20 casos y 3 repeticiones en los de las 5 dimensiones; documentos ficticios generados a partir de una lista que el usuario aprueba.

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
- 2026-11-18: etapa 2 escrita: 8 documentos ficticios de Nubesoft aprobados por el usuario, `01_esquema.sql` con las seis tablas, `02_datos_ficticios.sql` (el agente, 6 clientes y la línea base; el historial de tickets pasa a la etapa 7, donde se usa), `docker-compose.yml`, `base_de_datos.py`, `cargar_conocimiento.py`, `probar_busqueda.py`, `crear_embedding()` en `modelo.py` y `pg8000` en `requirements.txt`. Se comprobó que Gemini entrega embeddings de 768 números. `start-dev.bat` espera a que PostgreSQL esté listo.
- 2026-11-18: decisión del usuario: las pruebas incluyen pruebas adversariales; se documenta la estrategia en `pruebas-adversariales.md` (adaptada a FastAPI desde el ejemplo del usuario con Flask) y se agrega el grupo 4 de pruebas. Hypothesis es MPL 2.0: pendiente de que el usuario la acepte.
- 2026-11-18: el usuario acepta Hypothesis (MPL 2.0) como excepción, porque no se modifica.
- 2026-11-18: decisión del usuario: el proyecto tendrá evals del modelo; se documenta su plan en `evals-del-llm.md` (a partir de un prompt de ejemplo del usuario, adaptado al proyecto): `pytest` con un juez propio en vez de un framework, evaluación en tres capas, golden dataset en JSONL con campos en español, umbrales del curso y del proyecto, y lo que se puede ir dejando listo.
- 2026-11-18: decisión del usuario: también pruebas unitarias y de punta a punta, y todas las pruebas documentadas y separadas. Se crea `estrategia-de-pruebas.md` con cinco tipos (unitarias, integración, adversariales, evals y e2e), una carpeta con su `README.md` por tipo en `src/backend/tests/`, y la sección “Pruebas” del plan remite a ella.
- 2026-11-18: el usuario preguntó si el RAG tiene las prácticas estándar. Decisión D8: se agregan a `fragmentos_conocimiento` el modelo de embeddings, las dimensiones, la huella del documento y la fecha de carga, y la búsqueda solo compara vectores del mismo modelo; PDF y OCR, corte por secciones, búsqueda híbrida, reranking, carga incremental y permisos por documento se postergan. Probado: 7 de 7.
- 2026-11-18: el usuario aporta material de referencia sobre RAG y patrones de agentes. Lo relevante se resume en `buenas-practicas.md`, sin citar las fuentes (pedido del usuario): casi todo ya está; se adoptan 7 prácticas pequeñas en las etapas 3, 4 y 5, y el resto se posterga o no aplica. El material original no se sube (`.gitignore`).
- 2026-11-18: ideas tomadas de un RAG de ejemplo compartido por el usuario (sin copiar código, sin licencia): se agregan a `buenas-practicas.md` y a `evals-del-llm.md` (evaluar la búsqueda sola, datos esperados con alternativas, casos de varios documentos, modo detallado de la consola). Queda propuesto, sin aplicar, cortar los documentos por secciones.
- 2026-11-18: el usuario aprueba cortar los documentos por secciones (luego por párrafos y, si hace falta, por caracteres con solape), con el título antepuesto y la columna `seccion` para citar. Implementado en la etapa 2: 23 fragmentos y 7 de 7 búsquedas correctas, con parecidos más altos.
- 2026-11-18: el usuario prueba la etapa 2 completa (limpieza, arranque, carga y búsqueda) con el mismo resultado: queda cerrada. Sus búsquedas propias pasan a ser casos de las evals (tema correcto sin solución, pregunta ambigua). Decisión del usuario: los registros de pruebas no incluyen rutas completas ni logs de errores; los incidentes se resumen en una línea.
- 2026-11-18: el usuario acepta las recomendaciones de la revisión de la etapa 2 (EGM y fidelidad al curso), con un cambio propio: `clear.bat` nunca borra las imágenes descargadas; detiene y borra los contenedores y solo borra los volúmenes con `--borrar-volumenes`. Decisiones: el SQL de clientes y tickets va en `base_de_datos.py`; la lista de lo que el agente no atiende se agrega al prompt desde `registro_agentes.fuera_de_alcance`; se elimina la columna `dimensiones` (redundante con `vector(768)`); la fuente se cita en la respuesta desde la etapa 3 y en la auditoría desde la etapa 4. Correcciones: `trocear()` ya no repite el pedazo final; carga y búsqueda manejan errores de conexión y una base vacía, y cierran la conexión siempre; `conectar()` espera como máximo 10 segundos; un documento vacío se omite; `start-dev.bat` revisa que exista el `.env`; citas al curso precisadas (kill switch, audit trail, umbrales de las evals). La etapa 3 queda detallada en la tabla de etapas.
- 2026-11-18: preguntas del usuario sobre los vectores (por qué 768, si dependen del fragmento, cuánto cuesta calcularlos) y sobre cómo anonimizar datos sin un modelo remoto: se documentan en `embeddings-y-vectores.md` y `anonimizacion-de-datos.md`. Decisión del usuario: lo que es del proyecto se documenta en el proyecto, no en el material del curso.
- 2026-11-18: a pedido del usuario, la eliminación de la columna `dimensiones` pasa a ser la decisión D9, con las consultas que muestran dónde guarda la base el 768 (el tipo `vector(768)` y `vector_dims()`).
- 2026-11-18: a pedido del usuario, `estimar_costos.py` estima sin llamar al modelo el costo de cargar X documentos de X tamaño y el de cada consulta, en tres escenarios de demanda y con el pico frente al límite de la cuenta (`docs/costos.md`). Nuevas variables: `PRECIO_MILLON_TOKENS_EMBEDDINGS`, `LLAMADAS_POR_CONSULTA` y `LIMITE_LLAMADAS_POR_MINUTO`. También se documenta cómo cambiar el tamaño del vector sin reconstruir la base y que DBeaver no muestra el 768 (D9).
- 2026-11-19: a pedido del usuario, el código del backend se separa en dos paquetes: `aplicacion/` (config, modelo, base de datos, prompt y consola; desde la etapa 3, el agente, sus herramientas, las reglas y la API) y `scripts/` (prueba de conexión, carga del conocimiento, prueba de búsqueda, costos y, en la etapa 5, la aprobación del prompt). Se ejecutan con `python -m` desde `src/backend`; `RUTA_PROMPT` pasa a `config.py`; regla 15 y decisión D10. Probado de nuevo: 23 fragmentos y 7 de 7.
- 2026-11-19: etapa 3 escrita: `herramientas.py` (las tres herramientas, con `leer_argumentos()` que rechaza las desconocidas y los argumentos inválidos; `buscar_cliente` sin parámetros, porque el cliente sale del ticket), `agente.py` (`atender_mensaje()`, con un máximo de 6 llamadas al modelo por mensaje y el tope `TOPE_TOKENS_POR_TICKET`; si el modelo falla, se escala), prompt versión 2 (fuente citada, sin pasos propios, datos separados de las instrucciones), consola con código de cliente, ticket y modo `--detallado`, `estimar_costos.py` con los tokens reales y las primeras pruebas unitarias e integración (30). Decisiones D11 (el mensaje de Gemini vuelve tal cual, con su firma; confirma quien llama) y D12 (`127.0.0.1` en vez de `localhost`). La comparación con y sin RAG de `buenas-practicas.md`, que era opcional, queda pendiente.
- 2026-11-19: revisión de la etapa 3 (EGM y fidelidad al curso) aplicada con las decisiones del usuario: los 8 minutos se miden desde cada mensaje del cliente; si falla una herramienta, se escala por regla; los pasos usan solo los cinco tipos de `registro_auditoria` y los tokens se guardarán sumados en su columna `tokens`. Cambios: el bucle usa un diccionario `turno` (enganche único para la auditoría de la etapa 4), lee la versión del prompt, atiende primero un pedido válido de escalar, no ejecuta herramientas que superan el tope o en la última vuelta, escala si la respuesta llega vacía, cortada o filtrada (`finish_reason`) y si falla una herramienta; la consola ya no queda atrapada en un ticket borrado por el `rollback`; `marcar_como_datos()` cambia `<` por `&lt;`; `guardar_respuesta()` no pisa un ticket escalado; prompt versión 3 (el modelo no mide el tiempo); citas al curso corregidas; pruebas nuevas, incluida la lectura de la respuesta de `openai`; documentación sin conteos repetidos.
- 2026-11-19: a pedido del usuario, antes de la etapa 4: el chat y los embeddings tienen cada uno su proveedor (D13), para probar el chat con OpenRouter sin recargar la base; `scripts/prueba_conexion.py` prueba también las herramientas y el tamaño del vector. Nuevo `proveedores-de-modelos.md` (cómo saber si un modelo acepta herramientas, cómo probar OpenRouter, Ollama, respaldo ante caídas y por qué no balancear); Ollama y el respaldo quedan en la tabla de lo postergado.
- 2026-11-19: prueba con OpenRouter (capa gratuita): con `nvidia/nemotron-3-ultra-550b-a55b:free`, el agente se comportó igual que con Gemini en los cuatro casos de la etapa 3; se agregó `LLM_MAXIMO_TOKENS_SALIDA` (`pruebas/2026-11-19-openrouter.md`). El `.env` del usuario quedó con el chat en OpenRouter y los embeddings en Gemini.
- 2026-11-19: a pedido del usuario, `lecciones-aprendidas.md` reúne lo que enseñaron las etapas 0 a 3 y la prueba con OpenRouter, cada lección con un enlace a su detalle; se agrega una lección por cada prueba o revisión que deje algo.
- 2026-11-19: a pedido del usuario, el proveedor se elige por nombre (`LLM_PROVEEDOR` y `LLM_EMBEDDINGS_PROVEEDOR`, con `GEMINI_API_KEY` y `OPENROUTER_API_KEY`) y el `.env` queda alineado con `example.env`: `scripts/revisar_env.py` compara y ordena, y `start-dev.bat` avisa (D14, regla 5). El `.env` del usuario se migró y se ordenó sin mostrar claves.
- 2026-11-19: análisis con EGM de dónde vive el prompt maestro (`revisiones/2026-11-19-revision-prompt-maestro.md`); el usuario aprobó B+ (D15): el prompt sigue en el archivo con git, y una huella de las instrucciones completas se registra desde la etapa 4 y hace cumplir la aprobación desde la 5; un cambio de modelo solo queda anotado; el número de versión se mantiene como etiqueta. Se agregaron a lo postergado leer el prompt desde la base, la traza completa y OpenBao para las claves. Corregido un pendiente de la etapa 3: `modelo.py` acepta `temperatura`.
