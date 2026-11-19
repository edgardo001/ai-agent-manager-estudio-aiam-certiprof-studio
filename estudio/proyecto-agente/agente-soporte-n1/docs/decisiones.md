# Decisiones técnicas del proyecto

Registro de las decisiones técnicas que necesitan una explicación: qué problema había, qué opciones se consideraron, qué se eligió, por qué y qué implica. Sirve para entender el proyecto, no solo para construirlo. Las reglas generales están en `plan-del-proyecto.md`; aquí va el razonamiento detrás de algunas de ellas. Cada decisión nueva se agrega al final, con su fecha.

## D1. Librería para conectar Python con PostgreSQL: `pg8000`

**Fecha:** 2026-11-18. **Estado:** vigente, confirmada por el usuario el mismo día después de conocer la comparación.

**El problema:** el programa necesita una librería que conecte Python con PostgreSQL: que envíe consultas SQL y traiga los resultados. Cumple el mismo papel que un driver JDBC en Java o Npgsql en C#.

**Las opciones:**

| | `psycopg` | `pg8000` |
|---|---|---|
| Qué es | el estándar de Python para PostgreSQL | una alternativa escrita solo en Python |
| Popularidad | muy alta, con muchos ejemplos en internet | menor, con menos ejemplos, pero activa y mantenida desde hace años |
| Forma de uso | interfaz estándar de bases de datos de Python | la misma interfaz: `connect`, `cursor.execute(sql, parametros)`, `fetchall()` |
| Soporte nativo del tipo `vector` | no | no |
| Licencia | LGPL 3.0 | BSD 3 |

**La decisión:** `pg8000`.

**Por qué:** solo por la licencia. La regla del usuario exige licencias MIT, BSD, Apache o similares, y la LGPL no lo es. Para lo que necesita este proyecto, que es ejecutar SQL y leer resultados, las dos librerías son equivalentes.

**Una aclaración importante:** ninguna de las dos maneja vectores por sí sola. Elegir `pg8000` no resuelve el tema de los vectores; eso es la decisión D2, y funcionaría igual con cualquiera de las dos.

**Qué implica:** el código se ve casi igual que con `psycopg`; al buscar ejemplos en internet habrá que buscar los de `psycopg` y adaptarlos, que suele ser directo. Usar `psycopg` sin modificarla, como librería instalada, normalmente no obligaría a liberar el código del proyecto, y por eso muchos proyectos permisivos la usan; si el usuario quisiera aceptarla como excepción, el cambio es de una línea en `requirements.txt`.

## D2. Cómo se guardan y se buscan los vectores: texto convertido con `::vector`

**Fecha:** 2026-11-18. **Estado:** vigente.

**El problema:** un embedding es una lista de números (768 en este proyecto), por ejemplo `[0.12, -0.03, 0.88, …]`. PostgreSQL, con la extensión pgvector, lo guarda en una columna de tipo `vector`. Pero ni `psycopg` ni `pg8000` saben enviar una lista de Python como un `vector`: hay que hacer esa conversión de alguna forma.

**Las opciones:**

1. **Agregar la librería `pgvector` de Python**, que le enseña al driver a convertir la lista. Es lo más común en los ejemplos de internet, pero suma dos librerías (`pgvector` y `numpy`) solo para esa conversión.
2. **Enviar la lista como texto y que PostgreSQL la convierta.** Python transforma la lista en un texto como `"[0.12,-0.03,0.88]"`, lo envía como cualquier parámetro, y en el SQL se escribe `%s::vector`. En PostgreSQL, `::` significa “convierte a este tipo”.

**La decisión:** la opción 2.

**Por qué:** la regla de la menor cantidad de código y de librerías. El resultado es el mismo con una línea de Python y sin dependencias nuevas.

```python
vector_texto = "[" + ",".join(str(x) for x in embedding) + "]"

# Guardar un fragmento con su vector (versión corta de guardar_fragmento())
cursor.execute(
    "INSERT INTO fragmentos_conocimiento "
    "(documento, seccion, orden, texto, embedding, modelo_embedding, hash_documento) "
    "VALUES (%s, %s, %s, %s, %s::vector, %s, %s)",
    (documento, seccion, orden, texto, vector_texto, modelo, huella))

# Buscar los 5 fragmentos más parecidos a la pregunta (versión corta de buscar_fragmentos())
cursor.execute(
    "SELECT texto FROM fragmentos_conocimiento WHERE modelo_embedding = %s "
    "ORDER BY embedding <=> %s::vector LIMIT 5",
    (modelo, vector_pregunta_texto))
```

El operador `<=>` mide qué tan distintos son dos vectores (la distancia de coseno): ordenar de menor a mayor trae primero los fragmentos más parecidos a la pregunta.

**Qué implica:** para leer un vector desde la base de datos llegaría como texto, pero este proyecto nunca necesita leerlos: solo los guarda y los compara dentro de PostgreSQL. Si algún día hiciera falta trabajar con los vectores en Python, se reconsideraría la opción 1.

## D3. Excepciones a la regla de licencias

**Fecha:** 2026-11-18. **Estado:** vigente.

**La regla:** toda librería, imagen o herramienta debe tener licencia MIT, BSD, Apache 2.0 o similar (ver la regla 13 del plan y la sección “Licencias”).

**Las excepciones aceptadas por el usuario:**

- **`certifi` y `tqdm` (MPL 2.0):** vienen obligatoriamente con la librería `openai`. La MPL 2.0 es un copyleft débil por archivo: solo obliga a compartir los cambios hechos a los propios archivos de esas librerías, y no se van a modificar. Evitarlas exigiría dejar `openai` y programar las llamadas HTTP a mano.
- **`hypothesis` (MPL 2.0), para las pruebas adversariales de robustez:** aceptada el 2026-11-18 por el mismo motivo: no se modifica.
- **Grafana (AGPL), si se agrega más adelante:** el proyecto no se vende como producto, así que la AGPL no afecta su uso.

**Los reemplazos:**

- **Valkey en vez de Redis**, para la cola postergada: Redis, desde la versión 8, usa AGPL, RSAL o SSPL; Valkey es una copia de Redis con licencia BSD que funciona igual.
- **`pg8000` en vez de `psycopg`** (ver D1).

## D4. Sin autenticación en esta versión

**Fecha:** 2026-11-18. **Estado:** vigente, decisión del usuario.

**El problema:** el frontend y el backend permiten crear tickets, ver conversaciones, aprobar el prompt y detener el agente. En un sistema real, eso exige saber quién entra y qué puede hacer.

**Las opciones:**

1. **Una clave simple en la API.** Con un frontend en HTML y JavaScript estático, la clave terminaría escrita en un archivo `.js` del repositorio público, o habría que programar una pantalla para pedirla. Además, una sola clave serviría para todo: el mismo cliente que crea tickets podría apagar el agente.
2. **Usuarios y contraseñas dentro del proyecto.** Sumaría tablas, pantallas y código que no enseñan nada del curso.
3. **Sin autenticación, solo en el equipo local,** y dejar la seguridad de acceso para una capa superior cuando haga falta.

**La decisión:** la opción 3.

**Por qué:** es un proyecto para entender todo lo necesario del curso, y el curso no exige autenticación. El backend se publica solo en `127.0.0.1`, así que nadie fuera del equipo puede usarlo.

**Qué implica:** el proyecto no se puede exponer a internet tal como está. Cuando haga falta, la autenticación se agrega en una capa superior, por ejemplo un API gateway o un proxy con autenticación delante del backend, sin cambiar el código del agente. En ese momento conviene separar el acceso de los clientes (crear y ver sus tickets) del acceso del administrador, el AI Agent Manager (kill switch, aprobación del prompt, revisión del muestreo y dashboard). Está anotado en la tabla de lo postergado del plan.

## D5. Modelo de lenguaje: Gemini 3.1 Flash Lite

**Fecha:** 2026-11-18. **Estado:** vigente, elección del usuario.

**El modelo:** `gemini-3.1-flash-lite`, de Google, usado por su punto de acceso compatible con OpenAI. Google lo describe como su modelo más eficiente en costo, pensado para tareas agénticas de alto volumen, traducción y procesamiento simple de datos. Fecha de lanzamiento: 7 de mayo de 2026.

**Precios (Google AI Studio, consultados el 2026-11-18), en dólares por millón de tokens:** texto, imagen y video, 0,25 de entrada y 1,50 de salida; audio, 0,50 de entrada y 1,50 de salida. El proyecto solo usa texto.

**Por qué importa para el curso:** con estos precios se calcula el costo de tokens de cada ticket, que es parte del costo por caso (Módulo 3, sección 3.2) y del ROI (Módulo 5). Un modelo barato y rápido calza con un agente de soporte de nivel 1, que atiende muchos casos simples.

**Una aclaración:** los precios no configuran el modelo ni se le envían; Google cobra lo mismo. Son datos para un cálculo: el programa solo recibe cuántos tokens usó cada respuesta y, con el precio, los convierte en dólares (tokens de entrada por 0,25 más tokens de salida por 1,50, dividido por un millón). Van en el `.env` porque cambian si Google cambia el precio o si se cambia de modelo, y así no hay que tocar el código.

**El modelo de embeddings y los 768 números:** `gemini-embedding-001`, por el mismo punto de acceso. Cada modelo de embeddings entrega vectores de un tamaño propio, que no es un estándar: este entrega 3.072 números si no se le pide otra cosa, y acepta pedir menos con el parámetro `dimensions`; el proyecto pide 768. Se eligió 768 porque el índice HNSW de pgvector admite hasta 2.000 dimensiones y porque un vector más corto ocupa menos y se compara más rápido, con una pérdida de calidad pequeña (Google entrena este modelo para que los primeros números concentren lo más importante). El tamaño queda fijo en dos lugares: `DIMENSIONES_EMBEDDING` en `modelo.py` y `vector(768)` en `01_esquema.sql`. Cambiar de modelo de embeddings, o de proveedor, obliga a revisar su tamaño: si es otro, se cambian esos dos valores, se cambia el tipo de la columna y se recargan los documentos, sin reconstruir la base (ver `embeddings-y-vectores.md`, sección 6). La base no guarda el tamaño en una columna aparte (ver D9). Explicación completa, con una prueba y el costo de calcularlos, en `embeddings-y-vectores.md`.

**Dónde está anotado:** `LLM_MODEL` (este sí configura a qué modelo se le habla), `PRECIO_MILLON_TOKENS_ENTRADA` y `PRECIO_MILLON_TOKENS_SALIDA`, en `src/docker/example.env` (valores por defecto) y en el `.env`. Si cambia el modelo o su precio, se actualizan esos tres valores y esta decisión, con la fecha.

## D6. La consola se mantiene junto a la API

**Fecha:** 2026-11-18. **Estado:** vigente, pedido del usuario.

**El problema:** desde la etapa 6, el agente se usa a través de una API REST con FastAPI y, en la etapa 7, a través del frontend. Probar cada cambio por esas vías es más lento que conversar en la terminal, que al usuario le resultó cómodo y simple de revisar.

**La decisión:** `consola.py` se mantiene en todas las etapas. La lógica del agente vive en un solo lugar, `agente.py` (desde la etapa 3), y tiene dos puertas de entrada: la consola y la API.

```
consola.py  ──┐
              ├──►  agente.py (bucle, herramientas, reglas y auditoría)
api.py      ──┘     ◄── la API de FastAPI y, a través de ella, el frontend
```

**Por qué:** es más simple de seguir (una sola versión del agente, regla 2) y no duplica código (regla 3). Lo que se prueba en la consola es exactamente lo que hace la API.

**Qué implica:** la consola llama directo a `agente.py`, sin pasar por la API, así que funciona aunque la API no esté corriendo. Desde la etapa 3, cuando use `agente.py`, también necesita PostgreSQL, que levanta `start-dev.bat`; en la etapa 2 la búsqueda se prueba aparte con `probar_busqueda.py`. En la etapa 3 la consola cambia una vez: pide el código del cliente (por ejemplo `C-001`), crea el ticket y pasa cada mensaje a `agente.py`. Después, a medida que el agente gane reglas y auditoría, la consola las tendrá también, sin cambios propios.

## D7. FastAPI para la API REST, en su forma más simple

**Fecha:** 2026-11-18. **Estado:** vigente, elección del usuario.

**El problema:** desde la etapa 6, el agente necesita una API REST para que la use el frontend. Las dos opciones más comunes en Python son Flask y FastAPI, y el usuario quería saber cuál simplifica más el proyecto.

**Las opciones:**

| | Flask | FastAPI |
|---|---|---|
| Conceptos nuevos | menos: rutas y `request` | rutas y modelos de datos con Pydantic, en su forma simple |
| Validación de lo que llega | a mano, con `if` | automática |
| Página para probar la API | no trae; se usa curl o el frontend | trae `/docs`, una página web para probar cada endpoint con clics |
| Licencia | BSD | MIT |

Para este proyecto, la cantidad de código es casi la misma con las dos.

**La decisión:** FastAPI, usado en su forma más simple: funciones normales (`def`, sin `async`), sin inyección de dependencias y con modelos Pydantic pequeños solo donde llegan datos.

**Por qué:** la página `/docs` permite probar la API en el navegador, endpoint por endpoint, con la misma comodidad que hoy da la consola, y antes de que exista el frontend. Además, valida los datos sin escribir código de revisión.

**Qué es Pydantic:** una librería para describir cómo deben verse los datos que llegan y comprobarlos automáticamente. Se escribe una clase pequeña:

```python
from pydantic import BaseModel

class TicketNuevo(BaseModel):
    """Lo que debe traer un ticket nuevo."""
    cliente: str   # el código del cliente, por ejemplo "C-001"
    texto: str     # el problema, en palabras del cliente
```

Al usarla en un endpoint, FastAPI valida lo que llega (si falta un campo o el tipo no corresponde, responde con un error claro), lo entrega listo para usar (`datos.cliente`, `datos.texto`) y lo muestra en `/docs` con un ejemplo. Sin Pydantic, cada endpoint tendría que revisar los datos a mano con varios `if`.

**Qué implica:** se esperan dos o tres clases de este tipo en `api.py`, de dos o tres líneas cada una: crear un ticket, confirmarlo y calificarlo, y registrar una revisión del muestreo. No se usan funciones avanzadas de Pydantic. FastAPI y Pydantic tienen licencia MIT; uvicorn, el servidor que la ejecuta, BSD.

## D8. Alcance del RAG: qué prácticas de un RAG estándar tiene el proyecto

**Fecha:** 2026-11-18. **Estado:** vigente, aprobada por el usuario.

**El problema:** un RAG de producción suele cargar miles de documentos (por ejemplo, PDF), extraer su texto con OCR y el de sus imágenes, cortarlo en fragmentos con solape y guardar cada fragmento como texto y como vector, junto con el modelo de embeddings y otros datos de control. El usuario preguntó si el proyecto tiene todo eso. Siguiendo el principio rector (todos los conceptos, a escala pequeña), se separó lo que conviene tener ahora de lo que se posterga.

**Lo que el proyecto tiene:**

| Práctica | Cómo está en el proyecto |
|---|---|
| Fragmentos cortados con sentido | en tres niveles (`fragmentar_documento()`): por secciones del Markdown; si una sección pasa de 1.200 caracteres, por párrafos completos; y si un solo párrafo pasa de ese tamaño, por caracteres con 200 de solape (`trocear()`). Cada fragmento lleva antepuesto “Título - Sección”, para que se entienda solo |
| Texto y vector de cada fragmento | columnas `texto` y `embedding` |
| Origen de cada fragmento | columnas `documento`, `seccion` y `orden`; permiten citar con precisión, por ejemplo “error-de-sincronizacion.md > Códigos de error frecuentes” |
| Índice para buscar por parecido | índice HNSW con distancia de coseno |
| Modelo de cada vector | columna `modelo_embedding`; la búsqueda solo compara vectores del mismo modelo que la consulta, porque vectores de modelos distintos no se pueden comparar. El tamaño lo fija `vector(768)` (ver D5); la columna `dimensiones` se eliminó por redundante (D9) |
| Versión del documento cargada | columna `hash_documento`: huella SHA-256 que cambia si cambia una sola letra del documento |
| Fecha de carga | columna `cargado_en` |
| Citar la fuente de cada respuesta | en dos pasos (decisión del usuario): en la etapa 3, `buscar_solucion` entrega cada fragmento con su documento y su sección, y el agente cita el documento en su respuesta; en la etapa 4, la auditoría guarda el documento, la sección y la huella de los fragmentos usados. El audit trail del curso (Módulo 1, pregunta 9) pide qué decidió el agente y por qué; guardar “con qué datos” es una ampliación del proyecto |

**Lo que no tiene, a propósito:** un umbral mínimo de parecido. La prueba de la etapa 2, con el corte por secciones, mostró que una consulta sin documento (“máquina de café”) dio 0,70, más que la respuesta correcta más baja (0,69); la prueba anterior, sin secciones, había dado 0,64 frente a 0,66: decidir si el fragmento resuelve el caso lo hace el modelo, leyéndolo y siguiendo su SOP (sección 2.5).

**Lo que se posterga,** cada práctica con su motivo y cuándo agregarla, en la tabla de lo postergado del plan:

| Práctica | Por qué no ahora | Cuándo agregarla |
|---|---|---|
| Leer PDF, OCR de documentos escaneados y texto de imágenes | los documentos del proyecto ya son texto en Markdown, y el curso pide soluciones documentadas, no un formato; es la pieza más grande y costosa de un RAG real | cuando la base de conocimiento venga de PDF o de documentos escaneados |
| Búsqueda híbrida (palabras exactas más significado) | la búsqueda por significado encontró 7 de 7 | si fallan consultas con códigos exactos, como “S-09”; PostgreSQL lo permite sin servicios extra |
| Reordenar resultados con un segundo modelo (reranking) | suma llamadas al modelo en cada búsqueda | si las evals muestran que el documento correcto aparece, pero no primero |
| Carga incremental (solo lo que cambió) | recargar todo tarda segundos | cuando haya muchos documentos; la huella `hash_documento` ya permite saber cuáles cambiaron |
| Permisos por documento | todos los documentos son públicos para el agente | cuando haya documentos que solo algunos clientes o agentes puedan ver |

**Cambio del mismo día: corte por secciones.** Primero se había postergado cortar por secciones, porque cada documento cabía en un solo fragmento. Después de revisar un RAG de ejemplo, el usuario aprobó adoptarlo: hace que cada fragmento trate un solo tema y que la cita sea precisa. Resultado de la prueba: los 8 documentos pasaron de 8 a 23 fragmentos, las 7 consultas siguieron encontrando su documento con parecidos más altos (de 0,69 a 0,91, antes de 0,66 a 0,83), y la consulta “error S-09” encontró exactamente la sección de códigos de error. La sección que más se parece a una consulta suele ser la introducción, que describe el problema; los pasos de la solución están en otra sección, y por eso el agente recibe los 5 fragmentos más parecidos y no solo uno.

**Qué implica:** cambiar el modelo de embeddings obliga a recargar los documentos con `cargar_conocimiento.py`; mientras tanto, la búsqueda no mezcla vectores viejos con nuevos. El usuario aportará más documentos de buenas prácticas, que se evaluarán con este mismo criterio.

**Nota de la revisión de la etapa 3 (2026-11-19):** el índice HNSW busca los vecinos más cercanos y después aplica el filtro por modelo, así que si la tabla llegara a mezclar fragmentos de dos modelos, una búsqueda podría traer menos de 5. Hoy no pasa, porque `cargar_conocimiento.py` borra todo y carga con un solo modelo.

## D9. Sin columna `dimensiones`: el tamaño del vector lo guarda el tipo de la columna

**Fecha:** 2026-11-18. **Estado:** vigente, aprobada por el usuario en la revisión de la etapa 2.

**El problema:** D8 agregó a `fragmentos_conocimiento` una columna `dimensiones` con la cantidad de números de cada vector. La revisión de la etapa 2 la marcó como redundante, y el usuario preguntó dónde queda entonces el 768 en la base, porque no lo veía en otra columna.

**Dónde está el 768 en la base:** en el **tipo** de la columna `embedding`, que es `vector(768)`, igual que `varchar(50)` guarda el largo máximo de un texto. No aparece como dato en cada fila, pero la base lo conoce y lo hace cumplir:

```sql
-- El tipo de la columna (también lo muestra "\d fragmentos_conocimiento" en psql)
SELECT format_type(atttypid, atttypmod) FROM pg_attribute
WHERE attrelid = 'fragmentos_conocimiento'::regclass AND attname = 'embedding';
-- resultado: vector(768)

-- El tamaño de cada vector guardado, calculado al vuelo
SELECT documento, seccion, vector_dims(embedding) FROM fragmentos_conocimiento;
-- resultado: 768 en cada fila

-- Intentar guardar un vector de otro tamaño
INSERT INTO fragmentos_conocimiento (documento, seccion, orden, texto, embedding, modelo_embedding, hash_documento)
VALUES ('x', 'x', 0, 'x', '[1,2,3]', 'x', 'x');
-- resultado: ERROR: expected 768 dimensions, not 3
```

Las tres consultas se probaron el 2026-11-18 contra la base del proyecto.

**Ojo con DBeaver:** el DDL que genera DBeaver muestra `embedding public.vector NOT NULL`, sin el 768, porque no muestra el tamaño de los tipos que agrega una extensión. La base sí lo tiene: el DDL que genera PostgreSQL con `pg_dump -s -t fragmentos_conocimiento` dice `embedding public.vector(768) NOT NULL`, y la primera consulta de arriba devuelve `vector(768)`. Para ver el tamaño, conviene usar esas consultas y no el DDL de DBeaver.

**Las opciones:**

1. **Mantener la columna `dimensiones`:** deja el número a la vista en cada fila, pero siempre valdría 768, porque la base rechaza cualquier otro tamaño. Es un dato repetido que podría quedar desalineado si alguien cambia el tipo y no la columna.
2. **Eliminarla y leer el tamaño del tipo de la columna o con `vector_dims()`**.

**La decisión:** la opción 2.

**Por qué:** la regla de la menor cantidad de código (regla 3 del plan) y una sola fuente para cada dato. La columna no aportaba información que la base no tuviera ya, ni protegía de nada que `vector(768)` no proteja.

**Qué implica:** para ver el tamaño se usa una de las consultas de arriba. Lo que sí hay que guardar por fila es el modelo (`modelo_embedding`), porque dos modelos distintos pueden entregar el mismo tamaño y aun así sus vectores no se pueden comparar (D8). Cambiar de tamaño no exige reconstruir la base: se borran los fragmentos, se cambia el tipo de la columna con `ALTER TABLE` y se recarga (procedimiento probado en `embeddings-y-vectores.md`, sección 6).


## D10. El agente y los scripts de asistencia, en dos paquetes separados

**Fecha:** 2026-11-19. **Estado:** vigente, pedido del usuario (opción A de tres analizadas).

**El problema:** todo el código Python estaba en `src/backend/src/`, en archivos sueltos. Junto al agente (`config.py`, `modelo.py`, `base_de_datos.py`, `consola.py`) se fueron sumando scripts que se ejecutan aparte (`prueba_conexion.py`, `cargar_conocimiento.py`, `probar_busqueda.py`, `estimar_costos.py`), y con el tiempo no se iba a recordar cuáles eran parte de la API y cuáles eran de asistencia. Sacarlos a otro proyecto no servía, porque usan la configuración, el modelo y la base de datos del agente.

**Las opciones:** primero, dos paquetes hermanos en `src/backend/` (`aplicacion/` y `scripts/`) que se ejecutan con `python -m`; segundo, agregar solo `scripts/` y dejar `src/` como estaba, lo que obliga a cada script a modificar `sys.path` o a definir `PYTHONPATH` para encontrar el código del agente; tercero, dejar todo junto y distinguirlo con prefijos y un README, que no separa nada en la práctica ni sirve para dejar los scripts fuera de Docker.

**La decisión:** la primera opción.

```
src/backend/
├── aplicacion/   el agente: config, modelo, base de datos, prompt, consola; luego agente, herramientas, reglas y API
├── scripts/      asistencia: prueba de conexión, carga del conocimiento, prueba de búsqueda, costos; luego aprobar_prompt
└── tests/
```

Los imports son absolutos (`from aplicacion import config`) y todo se ejecuta desde `src/backend`: `python -m aplicacion.consola` o `python -m scripts.<nombre>`. La dependencia va en un solo sentido: los scripts usan la aplicación, la aplicación nunca usa un script. `RUTA_PROMPT` pasó de `consola.py` a `config.py`, porque `estimar_costos.py` dependía de la consola solo para saber dónde estaba el prompt.

**Por qué:** es la forma estándar de Python, sin trucos de rutas que después no se recuerdan; los scripts siguen compartiendo el entorno virtual, `requirements.txt` y el `.env`; y en la etapa 6 el `Dockerfile` copia solo `aplicacion/`, así que los scripts quedan fuera de la imagen sin configurar nada más. Revierte la equivalencia anterior del plan (“archivos sueltos, `python src/archivo.py`”), que se eligió por simplicidad cuando había pocos archivos.

**Qué implica:** un script nuevo va en `scripts/`, su comentario inicial empieza con “Script de asistencia” y se agrega a la tabla de `src/backend/scripts/README.md`. Si el agente pasa a necesitar la lógica de un script, esa lógica se mueve a `aplicacion/`: así pasó en la etapa 3 con `buscar()` de `probar_busqueda.py`, que ahora vive en `aplicacion/herramientas.py` y la usa la herramienta `buscar_solucion()`. Se probó el 2026-11-19: los imports, el estimador de costos, la carga (8 documentos, 23 fragmentos), la búsqueda (7 de 7), la conexión con el modelo y la consola.

## D11. Cómo conversa el bucle del agente con el modelo y con la base

**Fecha:** 2026-11-19. **Estado:** vigente, etapa 3.

**El problema:** el bucle del agente (`agente.py`) habla con Gemini varias veces por mensaje y escribe en varias tablas. Hubo que decidir dos cosas: cómo se devuelve al modelo lo que él mismo pidió, y quién confirma (commit) lo escrito en la base.

**Primera parte, el mensaje del modelo va tal cual.** Los modelos Gemini 3 agregan a cada pedido de herramienta una “firma de pensamiento” (`extra_content.google.thought_signature`) y exigen recibirla de vuelta en la llamada siguiente. Se probó el 2026-11-19 contra la API: sin la firma, Gemini responde error 400 (“Function call is missing a thought_signature”). Por eso `conversar_con_herramientas()` devuelve el mensaje con `model_dump(exclude_none=True)`, que conserva ese campo, y el bucle lo agrega a la conversación sin tocarlo. Las opciones descartadas eran armar el mensaje a mano con los campos conocidos (pierde la firma) o usar la librería de Google (otra dependencia, y se pierde la compatibilidad con OpenRouter).

**Segunda parte, confirma quien llama.** Las funciones de `base_de_datos.py`, `herramientas.py` y `agente.py` escriben, pero no hacen `commit`. Lo hace quien abrió la conexión al terminar cada mensaje: hoy la consola y, desde la etapa 6, la API. La opción descartada era confirmar dentro de cada función.

**Por qué:** un mensaje del cliente queda guardado completo o no queda (si algo falla a mitad, la consola hace `rollback` y no quedan tickets a medias), y las pruebas de integración pueden usar la base real y deshacer todo al final (`tests/conftest.py`), sin una base aparte para pruebas.

**Qué implica:** toda puerta de entrada nueva (la API de la etapa 6) debe confirmar o deshacer al terminar cada pedido. Desde la etapa 4, los pasos del registro de auditoría van en la misma transacción: son “todo o nada” por mensaje. Para que una falla no borre justo los pasos que la explican, toda falla que se pueda prever (el modelo, una herramienta, un tope) termina en un escalamiento por regla que sí se confirma; solo una falla de la propia base de datos deshace el mensaje. Los números de ticket que usaron las pruebas no se reutilizan (PostgreSQL no retrocede sus contadores con un `rollback`), así que los tickets reales pueden saltar números; no afecta a nada.

## D12. `127.0.0.1` en vez de `localhost` para conectarse a PostgreSQL

**Fecha:** 2026-11-19. **Estado:** vigente, encontrado al correr las pruebas de la etapa 3.

**El problema:** cada conexión a PostgreSQL tardaba 2 segundos. En Windows, `localhost` se intenta primero por IPv6 (`::1`), pero el compose publica el puerto solo en `127.0.0.1` (decisión D4); el intento por IPv6 se pierde y recién después se usa IPv4. Medido el 2026-11-19: 2,04 segundos con `localhost` y 0,03 con `127.0.0.1`. Las 30 pruebas bajaron de 38 a 5 segundos.

**La decisión:** `POSTGRES_HOST=127.0.0.1` en `example.env`, en el `.env` del usuario y como valor por defecto de `config.py`. Dentro de Docker (etapa 6) sigue siendo `postgres`.

**Por qué:** es el mismo equipo y la misma restricción de seguridad (solo accesible desde este equipo); solo se evita el intento inútil por IPv6. Publicar también en `::1` sumaba configuración sin ganar nada.

## D13. El chat y los embeddings, cada uno con su proveedor

**Fecha:** 2026-11-19. **Estado:** vigente, pedido del usuario (probar OpenRouter antes de la etapa 4).

**El problema:** el usuario quiere probar el agente con OpenRouter, y más adelante con Ollama, mezclar proveedores y tener respaldo si uno se cae. Hasta ahora el chat y los embeddings usaban la misma URL y la misma clave: cambiar el chat a OpenRouter cambiaba también los embeddings, y los 23 fragmentos guardados con `gemini-embedding-001` dejaban de servir, porque los vectores solo se comparan con los de su mismo modelo (D8).

**Las opciones:** primero, variables propias para los embeddings (`LLM_EMBEDDINGS_BASE_URL` y `LLM_EMBEDDINGS_API_KEY`), que si quedan vacías usan las del chat; segundo, recargar la base con un modelo de embeddings de OpenRouter cada vez que se cambie el chat; tercero, una capa de “proveedores” con perfiles con nombre en el código.

**La decisión:** la primera. `conectar_modelo(para_embeddings=True)` usa la configuración de los embeddings; el chat sigue con `LLM_BASE_URL`, `LLM_API_KEY` y `LLM_MODEL`.

**Por qué:** son dos variables y cuatro líneas de código; el chat se cambia sin recargar la base; y deja lista la mezcla que pidió el usuario (por ejemplo, embeddings de Ollama con el chat de Gemini u OpenRouter). La segunda opción obliga a recargar en cada cambio y a pagar de nuevo los embeddings; la tercera es una capa que hoy no hace falta.

**Qué implica:** el `.env` del usuario se completó el mismo día con la configuración de embeddings (copiando la de Gemini, sin mostrar la clave) y con un bloque comentado para OpenRouter. `scripts/prueba_conexion.py` ahora prueba también que el modelo de chat sepa usar herramientas y que el de embeddings entregue 768 números. Cambiar el **modelo** de embeddings sigue obligando a recargar la base. Ollama, el respaldo ante caídas y por qué no se recomienda balancear entre proveedores están en `proveedores-de-modelos.md`.

**Probado el 2026-11-19** con OpenRouter en la capa gratuita (`pruebas/2026-11-19-openrouter.md`): con `nvidia/nemotron-3-ultra-550b-a55b:free` el agente se comportó igual que con Gemini, con los embeddings en Gemini y sin recargar la base. La prueba agregó `LLM_MAXIMO_TOKENS_SALIDA` (2.000 por defecto), un tope de salida en cada llamada al chat: sin él, OpenRouter reserva saldo para la salida máxima del modelo y rechaza el pedido si no alcanza.

**Actualización del 2026-11-19:** las variables `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_EMBEDDINGS_BASE_URL` y `LLM_EMBEDDINGS_API_KEY` se reemplazaron por un proveedor elegido por nombre (D14). La idea de D13 se mantiene: el chat y los embeddings tienen cada uno su proveedor.

## D14. Proveedor elegido por nombre y `.env` alineado con la plantilla

**Fecha:** 2026-11-19. **Estado:** vigente, pedido del usuario (opción 1 de dos).

**El problema:** el `.env` del usuario se había separado de `example.env`: le faltaban cuatro variables nuevas, conservaba comentarios de versiones viejas y tenía otro orden. La causa de fondo era doble: el `.env` se copia una vez de la plantilla y nada avisa cuando la plantilla cambia, y cambiar de proveedor obligaba a comentar y descomentar tres líneas, con una clave guardada en una línea comentada.

**Las opciones:** primero, un proveedor elegido por nombre, con la clave de cada proveedor en su propia variable, más un script que compare y ordene el `.env`; segundo, mantener las variables de D13 y agregar solo el script.

**La decisión:** la primera.

- **Variables:** `GEMINI_API_KEY` y `OPENROUTER_API_KEY` (cada una con su nombre; Ollama no pide clave y tiene `OLLAMA_BASE_URL`); `LLM_PROVEEDOR` (`gemini`, `openrouter` u `ollama`) y `LLM_MODEL` para el chat; `LLM_EMBEDDINGS_PROVEEDOR` y `LLM_MODELO_EMBEDDINGS` para los embeddings. Cada proveedor tiene también su dirección en el `.env` (`GEMINI_BASE_URL` y `OPENROUTER_BASE_URL`, con las direcciones públicas como valor por defecto): son las mismas para todos, pero el usuario prefirió tenerlas a la vista para poder cambiarlas sin tocar el código si fuera urgente. `config.py` las reúne en `PROVEEDORES` y `datos_del_proveedor()`, y `faltan_variables()` avisa si el proveedor está mal escrito o si falta la clave del proveedor en uso.
- **Cambiar de proveedor:** se cambian dos líneas, `LLM_PROVEEDOR` y `LLM_MODEL`; las dos claves quedan guardadas a la vez y no hay nada que comentar.
- **`scripts/revisar_env.py`:** compara los nombres del `.env` con los de `example.env` y dice qué falta o sobra; con `--ordenar`, reescribe el `.env` con el orden y los comentarios de la plantilla, conservando los valores, agregando lo que falta con su valor de ejemplo y dejando al final lo que sobra, sin borrarlo. Antes guarda una copia en `.env.respaldo`. Nunca muestra los valores.
- **`start-dev.bat`** ejecuta `revisar_env` al empezar, solo para avisar.
- **`.gitignore`** ignora también `.env.*`, para que ningún respaldo con claves se suba.

**Por qué:** la segunda opción detecta la diferencia pero deja el cambio de proveedor como una edición a mano, que es lo que la produjo. Con el proveedor por nombre, la plantilla y el `.env` tienen siempre las mismas líneas y solo cambian los valores.

**Qué implica:** el `.env` del usuario se migró el mismo día a los nombres nuevos (las dos claves pasaron a `GEMINI_API_KEY` y `OPENROUTER_API_KEY`, sin mostrarse) y se ordenó como la plantilla; la versión anterior quedó en `src/docker/.env.respaldo-antes-de-d14`, ignorada por git, que el usuario puede borrar cuando confirme que todo funciona. Si la plantilla cambia, se ejecuta `python -m scripts.revisar_env --ordenar`. Agregar un proveedor que acepte el formato de OpenAI es una línea en `PROVEEDORES` y dos variables, su dirección y su clave. Al agregar las direcciones al `.env`, `revisar_env` avisó que faltaban y `--ordenar` las agregó sin tocar las claves: el mecanismo probado con un caso real.

## D15. El prompt maestro: archivo y git, con una huella que hace cumplir la aprobación

**Fecha:** 2026-11-19. **Estado:** vigente, aprobada por el usuario; el código llega en las etapas 4 y 5.

**El problema:** el prompt maestro (`prompt_soporte_n1.md`) se lee del archivo en cada mensaje y, desplegado, viaja dentro de la imagen Docker; la base no guarda su texto. El plan dice que una versión se usa solo si pasó las pruebas y el usuario la aprobó (sección 2.6; la 2.7 dice que los criterios de aceptación son “una política organizacional, no una recomendación”), pero nada lo hacía cumplir: editar el archivo cambiaba al agente desde el mensaje siguiente, el número de versión se escribe a mano, y “Lo que no atiendes” (que llega desde `registro_agentes`) podía cambiar sin dejar rastro. El usuario creía que el prompt se guardaba en la base en cada consulta, y propuso guardarlo en un key vault (OpenBao).

**Las opciones:** analizadas con elephant-goldfish-model (`revisiones/2026-11-19-revision-prompt-maestro.md`): A, como hoy; B, una huella del prompt aprobado; C, además el texto de cada versión en la base, y leerlo desde ahí; D, una traza completa de cada llamada al modelo; E, el prompt en OpenBao; B+, la propuesta consolidada.

**La decisión:** B+.

- **El prompt sigue en el archivo, con git como historia.** No se lee desde la base ni desde un vault.
- **La huella** (SHA-256, como `hash_documento` de D8) se calcula sobre las instrucciones completas que recibe el modelo: el archivo más “Lo que no atiendes”, ya leído como texto, para que Windows y Docker den la misma. Es la identidad de cada versión.
- **El número “Versión del prompt: N” se mantiene como etiqueta** para las personas (decisión del usuario); `aprobar_prompt.py` rechaza aprobar un número ya aprobado con otra huella.
- **Etapa 4, solo registrar:** cada paso de la auditoría guarda la versión, la huella, el proveedor y el modelo, y los fragmentos con su documento, sección, huella del documento y parecido, sin su texto. Si falta el archivo del prompt, el ticket se escala por regla en vez de perder el mensaje.
- **Etapa 5, hacer cumplir:** `aprobar_prompt.py` calcula la huella antes y después de las pruebas, y si pasan y coinciden guarda en `registro_agentes` la huella aprobada, la versión, quién y la fecha, y deja una fila de intervención en `registro_auditoria` con el texto completo (una vez por aprobación, unos 4 KB). Desde ahí, cada mensaje compara la huella del prompt que va a usar con la aprobada: si no coinciden y la barrera está activa, el ticket se escala por regla con el motivo “instrucciones sin aprobar” (D11: el escalamiento se confirma y queda explicado). En desarrollo y en las evals, la barrera está apagada y la diferencia solo queda anotada.
- **Un cambio de modelo o de proveedor solo queda anotado** en la auditoría; no bloquea (decisión del usuario), para poder probar proveedores sin reaprobar. Antes de usar otro modelo en serio, se corren las evals.

**Por qué:** hace cumplir la aprobación que pide el curso con dos columnas y unas veinte líneas, sin tablas nuevas ni servicios; distingue un cambio de instrucciones de una deriva (3.3 y la segunda señal de 3.4) y da la auditoría de prompt de la sección 4.6. La traza completa (D) ocuparía de 20 a 80 KB por ticket, copiaría hasta seis veces los datos del cliente y aun así no permitiría repetir una respuesta exacta; queda postergada, como Langfuse. OpenBao (E) se descartó para el prompt: el prompt no es un secreto (viaja completo al modelo en cada llamada), el versionado de un vault no es una aprobación con evals y abriría otro camino para cambiar las instrucciones en caliente.

**Qué implica:** que cambiar el prompt de un agente desplegado exija reconstruir la imagen es una ventaja, no un problema: la imagen queda fija y la huella prueba que trae lo aprobado. Se corrigió también un pendiente de la etapa 3 que encontró la revisión: `modelo.py` acepta `temperatura` (`opciones_de_llamada()`), para que las evals y el juez usen 0, como dice `evals-del-llm.md`. Quedan postergados, con su señal, leer el prompt desde la base y OpenBao para las claves de API.
