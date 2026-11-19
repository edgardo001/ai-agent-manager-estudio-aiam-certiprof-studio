# Plan y reglas del proyecto: Agente de Soporte N1

Este es el documento que manda en el desarrollo del agente: si otro documento dice otra cosa, vale lo que dice este archivo. `referencia/arquitectura.md` muestra hacia dónde podría crecer el sistema; un diseño anterior, con su ruta de construcción y una tabla de equivalencias, fue reemplazado por este plan, y git lo conserva. Se actualiza cada vez que el usuario pide un cambio, y cada cambio se anota en el registro del final.

**Estado (2026-11-19):** etapa actual, la 3 (herramientas y bucle del agente), terminada y probada, con su revisión aplicada. Siguiente paso: la etapa 4 (reglas en código, auditoría y kill switch). Lo probado en cada etapa está en `pruebas/`. Los tres pendientes que el usuario pidió cerrar antes de empezarla quedaron resueltos el 2026-11-19 (MEMORY.md de la raíz): el sandbox se activa cuando cambie a un modelo o herramienta en que confíe menos; las claves, de cuentas gratuitas, quedan sin restricción ni tope; y no se agregan más claves, con el respaldo entre proveedores postergado (modelos-y-costos.md, sección 4b).

**Propósito (decisión del usuario):** entender en simple el flujo completo de un agente gobernado por las reglas del curso y el esfuerzo que hay detrás. El proyecto tiene lo mínimo que haga falta para eso: ni más piezas, ni menos que las que exige el curso.

**Principio rector (decisión del usuario, manda sobre todas las reglas):** todos los conceptos del curso, a escala pequeña. Cada exigencia del curso tiene su pieza en el proyecto, pero con la infraestructura mínima: PostgreSQL resuelve todo lo que pueda (datos, vectores, banderas, métricas y tendencias). Las herramientas de escala (colas, workers, cachés, plataformas de monitoreo) se postergan hasta que el volumen las justifique, porque suman complejidad sin enseñar nada nuevo del curso; la tabla de lo postergado dice cuándo agregar cada una.

**Palabras que se usan en todo el proyecto:**

- **JD+SOP:** Job Description más Standard Operating Procedure (descripción del puesto más procedimiento paso a paso). Es la forma de escribir las instrucciones del agente que enseña el curso (sección 2.5): qué debe lograr y cómo. En el proyecto es el system prompt, `prompt_soporte_n1.md`.
- **EGM (elephant-goldfish-model):** la herramienta de revisión de calidad que instaló el usuario. Sus revisores leen el material sin contexto previo y dejan un informe en `revisiones/`. No viene en el curso.
- **Nubesoft:** la empresa ficticia de software B2B cuyo soporte atiende el agente. Sus clientes y sus documentos son inventados, porque el repositorio es público.
- **“Nivel”, en tres sentidos:** “N1” es el nivel 1 de soporte, la primera línea que atiende los casos simples, y da nombre al agente; el **Nivel 3 de autonomía** (Augmentación) es la escala del curso (sección 1.2) en la que está clasificado el agente; y los niveles de la **escalera de complejidad** de `rag.md` (sección 7) son una guía técnica que no viene del curso.

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

1. **Lenguaje y framework:** Python con FastAPI, en su forma más simple (D7).
2. **Simple para poder seguirlo:** una persona debe poder seguir el código de principio a fin. Se permiten patrones o principios solo cuando simplifican; se evitan capas, abstracciones o indirecciones que obligan a saltar entre muchos archivos para entender un flujo. Ante la duda, lo que se lee de corrido.
3. **La menor cantidad de código posible,** cubriendo todo lo que exige el curso. Antes de agregar una librería, un archivo, una tabla o un servicio, se pregunta si el curso lo exige o si sin él no funciona.
4. **Código comentado:** cada archivo empieza con un comentario que dice qué hace y en qué etapa aparece. Cada función lleva un docstring corto en lenguaje simple que dice qué hace y a qué parte del curso responde, con módulo y sección (“Curso: protocolos de escalamiento, Módulo 2, sección 2.5.”). Si la función es puramente técnica, dice “Técnico: no viene del curso.” Los scripts `.bat` dicen en su comentario inicial en qué etapa aparecen. El prompt es texto para el modelo, no código: no lleva esos comentarios.
5. **Variables de entorno:** en `src/docker/.env`, que nunca se sube; `src/docker/example.env` es la fuente oficial de sus nombres, orden y comentarios, y los dos tienen siempre las mismas líneas (D14).
6. **Docker Compose** en `src/docker/`.
7. **La documentación se actualiza con cada cambio (pedido del usuario):** este plan (estado, etapas y registro de cambios), `diagramas-del-codigo.md` cuando cambia el código, `decisiones.md` cuando se toma una decisión técnica, `lecciones-aprendidas.md` cuando una prueba, una revisión o una consulta deja algo que vale la pena recordar, el `README.md` del proyecto, el mapa `docs/README.md` cuando cambia un documento y `docs/pruebas/` cuando se prueba algo. Ningún cambio de código se da por terminado sin su documentación.
8. **Nombres en español,** con el vocabulario del curso (`escalar_a_humano`, `buscar_solucion`, `registro_auditoria`); también las funciones de entrada de los scripts. Quedan en inglés solo los nombres que imponen las librerías.
9. **Frontend en HTML y JavaScript simple,** sin framework ni compilación, entregado por el mismo FastAPI.
10. **Documentos ficticios** en `src/base-de-conocimiento/`, generados a partir de una lista que el usuario aprueba antes. Nunca información real: el repositorio es público.
11. **Dos formas de levantar el proyecto (forma de trabajo del usuario):** `start-dev.bat` (la app en local, con entorno virtual, y PostgreSQL en Docker) y `start-qa.bat` (todo en Docker, con el perfil `qa` del compose); `clear.bat` libera espacio. Qué hace y qué conserva cada uno está en el `README.md` del proyecto.
12. **La consola se mantiene en todas las etapas (pedido del usuario):** la consola y la API llaman a la misma función del agente, así que lo que se prueba en la consola es lo que hace la API (D6).
13. **Solo licencias permisivas (regla muy importante del usuario):** MIT, BSD, Apache 2.0 o similar; nada con copyleft (GPL, LGPL, AGPL, SSPL) ni de “código disponible” (RSAL). Antes de agregar una librería se revisa la suya y la de sus dependencias; la tabla está en “Licencias” y las excepciones aceptadas, en D3.
14. **Reglas del repositorio:** commits y push solo cuando el usuario los pide, uno por etapa; mensajes con el formato Conventional Commits, por ejemplo `feat(agente): agrega la base de conocimiento en pgvector` (ver `AGENTS.md`); sin firmas de agentes ni menciones del asistente.
15. **El agente y los scripts de asistencia van separados (pedido del usuario):** `aplicacion/` es el agente y entra en la imagen Docker; `scripts/` se ejecuta suelto y puede importar de `aplicacion`, nunca al revés; cada script nuevo va en la tabla de `src/backend/scripts/README.md` (D10).
16. **Registros de pruebas (decisión del usuario):** los de `docs/pruebas/` guardan los resultados y lo que enseñan, sin rutas completas del equipo ni logs de errores; un incidente se resume en una línea, con su solución.
17. **Material de referencia del usuario:** no se sube al repositorio ni se cita; lo relevante se resume en `rag.md`, con qué se adopta, en qué etapa y por qué.

## Estructura de carpetas

```text
estudio/proyecto-agente/
└── agente-soporte-n1/
    ├── README.md                       # qué es y cómo probarlo
    ├── start-dev.bat                   # dev: app en local (entorno virtual) y servicios en Docker
    ├── start-qa.bat                    # qa: todo en Docker, incluida la app (funciona desde la etapa 6)
    ├── clear.bat                       # limpieza: entorno virtual, cachés y contenedores; --borrar-volumenes, también los datos
    ├── docs/                           # la documentación; su mapa es docs/README.md
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

El código corre de dos formas: en local, con `start-dev.bat` (servidor de base de datos `127.0.0.1`; no `localhost`, que en Windows tarda 2 segundos más, D12), y dentro de Docker, con `start-qa.bat` desde la etapa 6 (servidor `postgres`). Por eso `config.py` arma la conexión con la variable `POSTGRES_HOST`, que vale `127.0.0.1` por defecto y `postgres` dentro del compose. Desde la etapa 6, el backend se construye con la carpeta `src/` completa como contexto, porque necesita leer `frontend/src/` y `base-de-conocimiento/`; el archivo `src/.dockerignore` evita que el `.env` y el entorno virtual entren en la imagen. Del backend, el `Dockerfile` copia solo `aplicacion/` y `requirements.txt`: los scripts de asistencia quedan fuera (D10).

**El compose de la etapa 2:** un solo servicio, `postgres`, con la imagen `pgvector/pgvector:pg17`; usuario, contraseña y base salen del `.env` (`${POSTGRES_USER}`, `${POSTGRES_PASSWORD}`, `${POSTGRES_DB}`); la carpeta `postgres/` se monta en `/docker-entrypoint-initdb.d` para que los SQL se ejecuten al crear el volumen; los datos quedan en un volumen con nombre; y el puerto se publica solo en el equipo (`127.0.0.1:5432:5432`). `POSTGRES_PASSWORD` es obligatoria: la imagen no arranca sin ella.

## Etapas de esta versión

| Etapa | Qué se construye | Archivos nuevos y archivos que cambian | Listo cuando |
|---|---|---|---|
| 0 | Conexión con el modelo | `config.py`, `modelo.py`, `prueba_conexion.py`, `example.env`, `start-dev.bat`, `start-qa.bat`, `clear.bat` | el modelo responde un saludo |
| 1 | Agente en la terminal con su JD+SOP | `consola.py`, `prompt_soporte_n1.md` | ante “quiero cancelar” responde que una persona seguirá el caso |
| 2 | Base de conocimiento en pgvector (el RAG) | nuevos: `docker-compose.yml`, `01_esquema.sql`, `02_datos_ficticios.sql`, `base_de_datos.py` (`conectar()`, `buscar_fragmentos()`), `cargar_conocimiento.py`, `probar_busqueda.py`, los documentos aprobados; cambian: `modelo.py` (`crear_embedding()`), `config.py` (variables `POSTGRES_*` y `LLM_MODELO_EMBEDDINGS`), `requirements.txt` (`pg8000`) | cada embedding tiene 768 números y “no puedo entrar” encuentra el documento de contraseñas |
| 3 | Herramientas y bucle del agente, con las prácticas adoptadas en `rag.md` (citar la fuente, datos separados de las instrucciones, tope de tokens, herramientas desconocidas rechazadas) | nuevos: `herramientas.py` (las tres herramientas; `buscar()` de `probar_busqueda.py` pasa aquí y la usa `buscar_solucion()`), `agente.py`; cambian: `modelo.py` (acepta las herramientas y devuelve los tokens usados), `base_de_datos.py` (funciones de clientes y tickets: todo el SQL sigue en este archivo), `consola.py` (pide el código del cliente y crea el ticket), `estimar_costos.py` (usa los tokens reales de los tickets en vez de los supuestos), `prompt_soporte_n1.md` (el programa le agrega la lista de lo que no atiende, leída de `registro_agentes.fuera_de_alcance`, que es su única fuente) | resuelve con documentos o escala con el contexto completo |
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

### Muestreo (sección 3.3)

Al cerrar cada ticket, se marca `en_muestra` al azar con la probabilidad de `PORCENTAJE_MUESTREO_REVISION` (10%). En la página de revisión, el usuario lee el caso y anota si hubo error y su categoría, de una lista cerrada (lista del proyecto; el curso pide categorías, pero no da una lista): solución incorrecta, información inventada, debió escalar y no escaló, escaló sin necesidad, incumplió una restricción y otro.

### Deriva de comportamiento (sección 3.3, Tipo 2)

Una consulta compara el muestreo, el CSAT y la tasa de escalamiento de las últimas semanas con los de los primeros 30 días del agente. No hace falta otra tabla.

### CSAT

La calificación de 1 a 5 que da el cliente al confirmar el ticket.

### Las 5 señales y el semáforo (sección 3.4)

| Señal | Se interviene cuando |
|---|---|
| Tasa de escalamiento | sube 5% (el proyecto lo interpreta como 5 puntos) y supera la meta del 20%, o se mantiene alta 3 o más días |
| CSAT | baja 0,2 puntos en una semana y coincide con un cambio en las instrucciones o en el volumen o tipo de casos |
| Tiempo de resolución | sube 20% de forma sostenida, sin más volumen que lo explique |
| Cambio externo | siempre: el usuario lo registra a mano y revisa las instrucciones |
| Muestreo | 3 errores en los últimos 50 casos revisados que comparten categoría (lo calcula el sistema) o muestran un patrón en las instrucciones (lo decide el usuario) |

Semáforo (la regla de colores es del proyecto; el curso solo dice “dentro de parámetros, requieren atención, alerta activa”): verde si no hay señales; amarillo si hay una señal que aún no cumple la condición de intervenir (por ejemplo, sube el escalamiento pero lleva menos de 3 días); rojo si alguna exige intervenir o si el agente está detenido.

### Los 5 paneles del dashboard (sección 3.5)

1, semáforo del agente; 2, resolución autónoma, escalamiento, tiempo promedio y costo por caso frente a la línea base, con tendencia de las últimas 2 semanas; 3, resultado del muestreo: casos revisados, errores por categoría y tendencia; 4, alertas de las 5 señales, en una lista priorizada, cada una con fecha y hora, descripción y acción recomendada, más los escalamientos contados por motivo, para ver si los traspasos se repiten en el mismo punto (sección 4.6); 5, valor acumulado: horas ahorradas, casos resueltos solos, ahorro frente a la línea base e impacto en NPS como proyección. Las tendencias salen de agrupar los tickets por día; no hacen falta tablas extra.

### Costo y valor (secciones 3.2 y 5.1 a 5.3)

El curso define el costo por caso como la inversión total del proceso dividida por el volumen; el proyecto usa una versión simplificada: el costo de tokens, más los minutos de las personas en los casos escalados por su costo por hora, dividido por el número de tickets. Las horas ahorradas son los casos resueltos solos por los minutos por caso de la línea base (fórmula del proyecto; el curso pide las horas, no la fórmula). Los riesgos y la próxima fase del business case (sección 5.3) se muestran como un texto fijo del dashboard. Los precios por millón de tokens y el costo por hora de una persona van en el `.env`. Solo el horizonte 1 del curso (eficiencia) se mide con datos; el NPS y los horizontes 2 y 3 se muestran como proyección, porque un proyecto de estudio no tiene datos para medirlos. La línea base de `02_datos_ficticios.sql` es ficticia y va marcada así. Los tickets históricos, también ficticios, se agregan en la etapa 7, junto con el dashboard que los usa, para que muestre tendencias desde el primer día.

## Pruebas

Cinco tipos de prueba, cada uno en su carpeta de `src/backend/tests/` (decisión del usuario): qué cubre cada tipo, cuánto cuesta y cuándo se escribe está en `estrategia-de-pruebas.md`, y las evals, con sus metas y umbrales, en `evals-del-llm.md`. Para gastar pocas llamadas al modelo, las pruebas sin modelo (unitarias, de integración y adversariales, incluidas las reglas en código) se corren a cada cambio, y las que usan el modelo real (evals y de punta a punta) antes de aprobar una versión del prompt o al cerrar una etapa. El CSAT no se puede medir en las pruebas, porque lo da el cliente.

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
| `hypothesis` y su dependencia `sortedcontainers` | MPL 2.0 y Apache 2.0 | etapas 5 y 6; excepción aceptada (D3) |
| Dependencias de `openai`: `httpx`, `httpcore`, `anyio`, `distro`, `jiter`, `sniffio`, `idna`, `typing_extensions` | BSD, MIT o Apache 2.0, PSF | en uso |
| Dependencias de `openai`: `certifi` y `tqdm` | MPL 2.0 (`tqdm`: MPL 2.0 y MIT) | en uso; excepción aceptada (D3) |
| Imagen `pgvector/pgvector` (PostgreSQL y la extensión pgvector) | Licencia PostgreSQL, permisiva | etapa 2 |
| `psycopg` | LGPL 3.0 | descartada: se reemplaza por `pg8000` |
| `pgvector` (librería de Python) y `numpy` | MIT y BSD | no hacen falta: los vectores se convierten en SQL con `::vector` (ver `decisiones.md`, D2) |

Las excepciones aceptadas y su porqué (la MPL 2.0 y Grafana), y el porqué de `pg8000` y de los vectores como texto, están en `decisiones.md` (D1, D2 y D3).

## Lo que se deja fuera en esta versión, por qué y cuándo agregarlo

Lo que se saca no se descarta: se posterga, y esta tabla recuerda por qué y qué señal indica que llegó el momento.

| Pieza postergada | Qué se usa en su lugar | Por qué se saca ahora | Cuándo agregarla |
|---|---|---|---|
| Cola de casos (Valkey, la copia de Redis con licencia BSD, D3) | la API atiende el ticket en el mismo pedido | con pocos tickets la cola no aporta y suma un servicio | cuando la atención de un ticket tarde más de 30 segundos con frecuencia, o lleguen varios tickets a la vez |
| agent-worker separado | el bucle corre dentro del backend | sin cola, el worker no tiene trabajo propio | junto con Valkey |
| Kill switch en Valkey | columna `detenido` en `registro_agentes` | la base de datos ya existe y basta para una bandera | con Valkey, o con varios servidores |
| mock-crm como servicio | tabla `clientes` | un servicio aparte simularía lo mismo con más código | cuando se conecte un CRM real |
| Grafana (AGPL, excepción aceptada, D3) | dashboard propio en el frontend | el curso pide 5 paneles concretos que se arman con pocas consultas | con más agentes, o si se necesitan alertas automáticas e historia larga |
| Langfuse (MIT; registra cada llamada al modelo y la muestra en una web para buscar y comparar) | `registro_auditoria` | el curso pide el audit trail, no una plataforma de trazas | cuando haga falta analizar en detalle prompts, tokens y latencia |
| CI automático | pruebas a mano con `pytest` | no hay flujo de despliegue | cuando el código se publique o lo modifiquen varias personas |
| Autenticación del frontend y del backend | todo corre solo en el equipo local (`127.0.0.1`) | el curso no la exige; con un frontend estático, una clave quedaría expuesta | cuando el sistema se exponga fuera del equipo (D4) |
| Prácticas de RAG a gran escala: PDF y OCR, búsqueda híbrida, reranking, carga incremental, permisos por documento | documentos en Markdown, búsqueda por significado y recarga completa | a escala pequeña no cambian el resultado y suman código o costo | cada una con su señal en D8 |
| Framework de evals (`deepeval`, `ragas`, `inspect-ai`) | `pytest` y un juez propio de pocas líneas | no suma librerías y deja ver cómo se calcula cada métrica | cuando el juez propio deje de ser simple (`evals-del-llm.md`) |
| Anonimizar datos sensibles antes de enviarlos al modelo | datos ficticios, permisos mínimos y la restricción de no compartir datos de otros clientes | ningún dato del proyecto es real | cuando el agente atienda clientes reales o se carguen documentos con datos personales (`referencia/anonimizacion-de-datos.md`) |
| Leer el prompt desde la base | el archivo, con git y la huella aprobada | crearía dos fuentes de verdad para el mismo texto | cuando haya que cambiar el prompt sin reconstruir la imagen o quien audita no tenga acceso a git (D15) |
| Traza completa de cada llamada al modelo | la auditoría con la huella del prompt, los datos usados y el modelo | ocupa mucho, copia los datos del cliente y no permite repetir una respuesta | cuando un caso del muestreo no se pueda explicar con la auditoría (D15) |
| Gestor de secretos (OpenBao) para las claves de API | las claves en el archivo de configuración local, fuera de git y de la imagen | con un equipo y una persona, la credencial del vault quedaría junto a las claves | cuando el sistema salga del equipo local, varias personas usen las claves o haga falta rotarlas; antes, confirmar su licencia (D15) |
| `task_type` de los embeddings | embeddings sin tipo, por la librería `openai` | se ahorra una librería y una clave | si la búsqueda encuentra mal los documentos |
| Ollama (modelos en el propio equipo, MIT) | Gemini u OpenRouter por internet | un modelo local que use bien herramientas necesita memoria y es lento sin tarjeta gráfica | cuando se quiera costo cero por token o que los datos no salgan del equipo (`modelos-y-costos.md`, sección 4) |
| Respaldo si el proveedor del chat se cae | si el modelo falla, el ticket se escala por regla | primero hay que poder comparar modelos con las evals | si las caídas siguen siendo frecuentes después de la etapa 6 (`modelos-y-costos.md`, sección 4) |

## Registro de cambios

Una línea por cambio, con la regla o la decisión que lo explica; el detalle está en git, en `decisiones.md` y en `revisiones/`.

- 2026-11-18: versión inicial con las reglas del usuario (reglas 1 a 6 y 8 a 10); las simplificaciones valen solo para esta versión, con la tabla de lo postergado; la regla 2 permite patrones si simplifican.
- 2026-11-18: se crea `agente-soporte-n1/` con las etapas 0 y 1, la carpeta `docs/` y las decisiones por defecto (un commit por etapa, regla 14).
- 2026-11-18: revisión del plan aceptada (`revisiones/2026-11-18-revision-egm-del-plan.md`): flujo en 14 pasos, seis tablas, aprobación del prompt con nombre, sin clave de API, resolución confirmada por el cliente con cierre por inactividad, NPS como proyección, Nivel 3 y embeddings con la librería `openai`.
- 2026-11-18: `start-dev.bat`, `start-qa.bat` y `clear.bat` (regla 11).
- 2026-11-18: solo licencias permisivas (regla 13): `pg8000`, vectores como texto, excepciones y reemplazos (D1, D2 y D3); nace `decisiones.md`.
- 2026-11-18: sin autenticación (D4); el proyecto incluye un RAG (pasos 4 y 8 del flujo); modelo `gemini-3.1-flash-lite` (D5); etapas 0 y 1 probadas.
- 2026-11-18: la consola se mantiene (regla 12, D6); nace `diagramas-del-codigo.md`.
- 2026-11-18: revisión de consistencia y de fidelidad al curso (`revisiones/2026-11-18-revision-consistencia-y-curso.md`): principio rector, carpeta `referencia/` y citas al curso corregidas.
- 2026-11-18: la documentación se actualiza con cada cambio (regla 7); FastAPI (D7); Conventional Commits (regla 14).
- 2026-11-18: cinco tipos de prueba, con adversariales y evals (`estrategia-de-pruebas.md` y `evals-del-llm.md`); Hypothesis aceptada (D3).
- 2026-11-18: etapa 2 escrita y probada, con las prácticas de RAG (D8), el corte por secciones y sin columna `dimensiones` (D9); revisión de la etapa 2 aplicada (`revisiones/2026-11-18-revision-etapa-2.md`).
- 2026-11-18: material de referencia del usuario resumido sin citarlo (regla 17); registros de pruebas sin rutas ni logs (regla 16); lo del proyecto se documenta en el proyecto, no en el material del curso.
- 2026-11-18: vectores, anonimización y estimación de costos documentados (hoy en `rag.md`, `referencia/anonimizacion-de-datos.md` y `modelos-y-costos.md`).
- 2026-11-19: el backend se separa en `aplicacion/` y `scripts/` (regla 15, D10).
- 2026-11-19: etapa 3 escrita y probada (D11 y D12); su revisión aplicada (`revisiones/2026-11-19-revision-etapa-3.md`): los 8 minutos se miden por mensaje y la falla de una herramienta escala por regla.
- 2026-11-19: el chat y los embeddings con su proveedor (D13), probado con OpenRouter; proveedor elegido por nombre y configuración alineada con la plantilla (D14, regla 5).
- 2026-11-19: nace `lecciones-aprendidas.md` (regla 7).
- 2026-11-19: el prompt maestro sigue en archivo y git, con una huella que hace cumplir la aprobación (D15, `revisiones/2026-11-19-revision-prompt-maestro.md`); se postergan leerlo desde la base, la traza completa y OpenBao.
- 2026-11-19: simplificación de la documentación (`revisiones/2026-11-19-revision-simplificacion.md`): nacen `rag.md` y `modelos-y-costos.md`, las pruebas adversariales pasan a `estrategia-de-pruebas.md`, la anonimización a `referencia/`, se eliminan la ruta de construcción y la tabla de equivalencias, y se agregan las reglas 16 y 17.
- 2026-11-19: consulta del usuario sobre usar varias claves: decidió no agregarlas (riesgo de bloqueo) y mantener postergado el respaldo entre proveedores; los cupos de OpenRouter y las opciones legítimas quedaron en modelos-y-costos.md, sección 4b.
- 2026-11-19: cerrados los tres pendientes previos a la etapa 4 (sandbox para cuando cambie de modelo, claves gratuitas sin restricción, sin claves adicionales).
