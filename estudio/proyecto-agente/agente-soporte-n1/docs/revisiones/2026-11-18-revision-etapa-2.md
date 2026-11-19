# Revisión de la etapa 2, 2026-11-18

Dos revisiones de solo lectura, pedidas por el usuario al cerrar la etapa 2, según la regla de revisiones de calidad de `AGENTS.md`:

1. **Elephant-goldfish-model:** tres revisores (detalles del código, estructura y simplicidad), coordinados por su sintetizador, sobre el código, el esquema, los documentos y la documentación de la etapa 2.
2. **Fidelidad al curso:** un verificador independiente revisó cada cita al curso agregada en la etapa 2.

El agente que las pidió comprobó a mano los hallazgos de código principales (el pedazo repetido de `trocear()`, la búsqueda vacía de `probar_busqueda.py` y el ejemplo SQL de D2): los tres son correctos.

**Estado:** aplicada el 2026-11-18. El usuario aceptó las recomendaciones, con un cambio propio en la pregunta 4 (ver “Decisiones del usuario”, al final).

## Resultado general

- **El código de la etapa 2 es correcto y pequeño:** el esquema coincide con el código, la conversión `::vector` y el índice de coseno son correctos, la carga es una sola transacción, los saltos de línea de Windows no afectan el corte, el diagrama entidad-relación coincide columna por columna y los 23 fragmentos cuadran con las secciones reales.
- **Fidelidad al curso:** de unas 75 citas, unas 68 coinciden exactamente; ninguna cifra está mal y ningún número de sección apunta a una sección equivocada.
- **Nada impide empezar la etapa 3,** pero conviene resolver antes tres puntos de diseño.

## Hallazgos de la revisión de elephant-goldfish-model

| # | Hallazgo | Gravedad |
|---|---|---|
| 1 | El plan subestima qué cambia en la etapa 3: también cambian `modelo.py` (que hoy no acepta herramientas ni devuelve los tokens), `base_de_datos.py` (no tiene funciones para clientes ni tickets) y `consola.py` (tendrá que pedir el código del cliente y crear el ticket); D6 dice que la consola no cambia | importante |
| 2 | Si la base está vacía o se cambió el modelo de embeddings, `probar_busqueda.py` se cae con un error ilegible; `buscar_solucion()` heredaría el problema | importante |
| 3 | Los scripts no manejan errores de conexión (PostgreSQL apagado, clave mala), no cierran la conexión si hay un error y `conectar()` no tiene límite de espera; falta una regla de “una conexión por ticket” para la etapa 3 | importante |
| 4 | La lista de lo que el agente no atiende está en un documento del RAG y en `registro_agentes`, pero no en el prompt: que el agente la vea depende de que la búsqueda la traiga | importante |
| 5 | D8 justifica no usar un umbral con las cifras anteriores al corte por secciones (0,64 y 0,66) en vez de las nuevas (0,70 y 0,69) | importante (documentación) |
| 6 | El ejemplo SQL de D2 ya no funciona contra el esquema (faltan columnas obligatorias y el filtro por modelo) | importante (documentación) |
| 7 | La función de búsqueda real vive en el script de prueba; en la etapa 3 debe pasar a `herramientas.py` | menor |
| 8 | La huella del documento se guarda pero no se lee, y D8 y `buenas-practicas.md` no coinciden en la etapa de la cita | menor |
| 9 | `trocear()` crea un pedazo final repetido cuando el anterior ya llegó al final del texto | menor |
| 10 | El formato que exige el corte (título, aviso, secciones) no está escrito, y hay casos borde silenciosos (documento sin contenido, archivo con BOM) | menor |
| 11 | El encabezado del registro de pruebas quedó desactualizado | menor |
| 12 | El README de PostgreSQL y un comentario de `example.env` están en un tiempo equivocado | menor |
| 13 | Restos de “tres grupos de pruebas” y una frase sobre quién arma la conexión; faltan dos flechas en el diagrama 1 | menor |
| 14 | `start-dev.bat` no revisa que exista el `.env` ni menciona Docker apagado; el texto de `clear.bat` no dice que borra la imagen de PostgreSQL | menor |
| 15 | La columna `dimensiones` es redundante con `vector(768)` | menor |

## Hallazgos de la verificación de fidelidad al curso

1. Un umbral de las evals atribuye al curso escalar ante descuentos, cambios de cuenta y casos adversariales; el curso los trata como restricciones y límites, y el 100% es del proyecto.
2. Una frase del prompt del proyecto aparece citada como si fuera de la sección 2.5.
3. El kill switch se cita a la sección 4.5, que habla de circuit breaker; el kill switch está en la 1.2, para el Nivel 4.
4. “Con qué datos” del audit trail es una ampliación del proyecto sobre el Módulo 1, pregunta 9.
5. En las evals, repetir la validación de la 2.6 en cada versión del prompt y la “cancelación implícita” son extensiones del proyecto sin marcar; y un ejemplo de docstring mezcla “Técnico:” con una cita al curso.

## Preguntas para el usuario

1. ¿Las funciones de clientes y tickets van en `base_de_datos.py` o se acepta SQL dentro de `herramientas.py`?
2. ¿La lista de lo que el agente no atiende pasa al prompt, con fuente única en `registro_agentes.fuera_de_alcance`?
3. ¿Se elimina la columna `dimensiones` o se conserva por lo que enseña?
4. ¿`clear.bat` sigue borrando la imagen descargada de PostgreSQL?
5. ¿La cita de la fuente va ya en la etapa 3 o solo desde la etapa 4?

## Decisiones del usuario

1. Las funciones de clientes y tickets van en `base_de_datos.py`: todo el SQL sigue en un solo archivo.
2. La lista de lo que el agente no atiende se agrega al prompt desde `registro_agentes.fuera_de_alcance`, su única fuente (etapa 3).
3. Se elimina la columna `dimensiones`: `vector(768)` ya fija el tamaño. La explicación de los 768 números quedó en D5.
4. **Cambio del usuario:** `clear.bat` nunca borra las imágenes descargadas; detiene y borra los contenedores, y borra los volúmenes solo con `clear.bat --borrar-volumenes`, que pide confirmación.
5. La fuente se cita en la respuesta desde la etapa 3 y queda en la auditoría desde la etapa 4.

Los 15 hallazgos y las 5 imprecisiones se corrigieron; los que dependen de la etapa 3 (1, 4, 7 y la regla de una conexión por ticket) quedaron escritos en la tabla de etapas del plan. Resultado de la prueba final en `pruebas/2026-11-18-etapa-2.md`.
