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

# Guardar un fragmento con su vector
cursor.execute(
    "INSERT INTO fragmentos_conocimiento (documento, orden, texto, embedding) "
    "VALUES (%s, %s, %s, %s::vector)",
    (documento, orden, texto, vector_texto))

# Buscar los 5 fragmentos más parecidos a la pregunta
cursor.execute(
    "SELECT texto FROM fragmentos_conocimiento "
    "ORDER BY embedding <=> %s::vector LIMIT 5",
    (vector_pregunta_texto,))
```

El operador `<=>` mide qué tan distintos son dos vectores (la distancia de coseno): ordenar de menor a mayor trae primero los fragmentos más parecidos a la pregunta.

**Qué implica:** para leer un vector desde la base de datos llegaría como texto, pero este proyecto nunca necesita leerlos: solo los guarda y los compara dentro de PostgreSQL. Si algún día hiciera falta trabajar con los vectores en Python, se reconsideraría la opción 1.

## D3. Excepciones a la regla de licencias

**Fecha:** 2026-11-18. **Estado:** vigente.

**La regla:** toda librería, imagen o herramienta debe tener licencia MIT, BSD, Apache 2.0 o similar (ver la regla 13 del plan y la sección “Licencias”).

**Las excepciones aceptadas por el usuario:**

- **`certifi` y `tqdm` (MPL 2.0):** vienen obligatoriamente con la librería `openai`. La MPL 2.0 es un copyleft débil por archivo: solo obliga a compartir los cambios hechos a los propios archivos de esas librerías, y no se van a modificar. Evitarlas exigiría dejar `openai` y programar las llamadas HTTP a mano.
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

**Qué implica:** la consola llama directo a `agente.py`, sin pasar por la API, así que funciona aunque la API no esté corriendo. Desde la etapa 3, cuando use `agente.py`, también necesita PostgreSQL, que levanta `start-dev.bat`; en la etapa 2 la búsqueda se prueba aparte con `probar_busqueda.py`. A medida que el agente gane herramientas, reglas y auditoría, la consola las tendrá también, sin cambios propios.

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
