# Revisión de consistencia y de fidelidad al curso, 2026-11-18

Dos revisiones de solo lectura, pedidas por el usuario antes del primer commit del proyecto, porque sospechaba que algunos diagramas de `docs/` no coincidían:

1. **Consistencia interna**, con elephant-goldfish-model: cuatro revisores (detalles del código, estructura, comprensión y preparación para implementar), coordinados por su sintetizador.
2. **Fidelidad al curso**, con un verificador independiente que comprobó cada afirmación atribuida al curso contra `estudio/modulos/`.

El agente que las pidió comprobó a mano los hallazgos principales antes de aplicarlos (por ejemplo, que la sección 3.4 no menciona el kill switch y que el audit trail sale del Módulo 1, pregunta 9).

**Estado:** el usuario aprobó la propuesta y se aplicó el mismo día (ver el registro de cambios del plan).

## Resultado general

- **El código de las etapas 0 y 1 era correcto** y coincidía con el plan, el README, los diagramas del código y el registro de pruebas. Las decisiones D1 a D6, el modelo `gemini-3.1-flash-lite`, `pg8000`, los embeddings por `openai`, la API síncrona, el Nivel 3 y la numeración de las reglas eran coherentes en todos los archivos.
- **El proyecto era fiel al curso en lo esencial:** unas 55 afirmaciones se comprobaron exactas (80%, 3 minutos, 4,2 sobre 5, 20%, 8 minutos, del 5% al 10%, 90 segundos, las 5 señales, los 5 paneles, los 5 indicadores, las 5 dimensiones, los niveles de autonomía y el prompt palabra por palabra).
- **La impresión del usuario era correcta:** de los 10 diagramas de `docs/`, los 4 de `diagramas-del-codigo.md` eran de la versión 1; los 4 de `arquitectura.md` eran de la versión futura con un solo aviso general, y además contradecían decisiones (Redis, `psycopg`, clave de API, una herramienta que no existe); y los 2 de `ruta-de-construccion.md` eran del diseño anterior, uno sin ningún aviso.

## Hallazgos y qué se hizo

| Hallazgo | Qué se hizo |
|---|---|
| Tres textos mandaban a la ruta para ver las etapas | ahora mandan al plan; se creó `docs/README.md` como mapa |
| `arquitectura.md` y la ruta, con diagramas viejos o futuros sin aviso propio | pasaron a `docs/referencia/`, con un aviso al inicio y antes de cada diagrama o etapa; en `arquitectura.md` se corrigió Redis por Valkey, `psycopg` por `pg8000`, la clave de API y la herramienta |
| El README de `postgres` usaba los nombres viejos de los SQL | reescrito con `01_esquema.sql` y `02_datos_ficticios.sql` |
| El modelo de datos no decía cómo se unen las tablas ni el tipo del ID de cliente | `agente_id` en `tickets` y `registro_auditoria`, `ticket_id` vacío en intervenciones, y `codigo` de texto (`C-001`) en `clientes` |
| `POSTGRES_PASSWORD` vacía y sin aviso; faltaba el compose de la etapa 2 | aviso en `example.env` y en el README; el compose de la etapa 2 quedó definido en el plan |
| La tabla de equivalencias no cubría archivos, tablas, conexión ni parámetros de embeddings | filas nuevas; la etapa 2 nombra también los archivos que cambian y sus funciones |
| `start-qa.bat` dejaría de avisar desde la etapa 2 | ahora comprueba también el `Dockerfile` |
| El límite de 60 segundos podía triplicarse por los reintentos automáticos | `max_retries=0` en `modelo.py` |
| D6 decía que la consola necesita PostgreSQL desde la etapa 2 | corregido a la etapa 3 |
| Restos de Redis en el plan, Nivel 2 en `AGENTS.md`, “5 filtros” en varios archivos | corregidos a Valkey, Nivel 3 con nota y “5 dimensiones” o “tres grupos de pruebas” |
| La revisión anterior decía que no se había aplicado nada | se agregó su estado |
| Citas al curso: audit trail a 1.2 y 3.3; kill switch a 3.4; línea base a 5.1; registro de agentes sin 2.7; descuento a 2.2 | corregidas: Módulo 1, pregunta 9; secciones 1.2 y 4.5; secciones 3.2, 3.7, 5.2 y 5.3; 2.7; ejemplo de 2.5 |
| Señales y paneles incompletos (“5 puntos”, falta “volumen”, falta el patrón en las instrucciones, panel 4 sin prioridad ni fecha, panel 5 sin NPS) | completados con el texto del curso |
| Decisiones del proyecto presentadas como del curso (confirmación y cierre a 24 horas, agente detenido, categorías de error, fórmulas de costo y de horas, colores del semáforo) | marcadas como del proyecto |
| Coberturas del curso que faltaban | agregadas a escala pequeña: deriva de comportamiento contra los primeros 30 días, verificación obligatoria antes de cambiar una cuenta, una prueba por cada condición de escalamiento y todas las metas, campos del registro del agente (área, fuera de alcance, justificación de permisos, última auditoría), tiempo de respuesta del traspaso, traspasos por motivo, roles del equipo híbrido y los riesgos y la próxima fase del business case como texto del dashboard |

## Pendientes que quedaron fuera de esta revisión

- La lista de documentos ficticios de la base de conocimiento, que el usuario debe aprobar antes de la etapa 2.
- Las plantillas de `estudio/plantillas/` todavía describen al agente en Nivel 2.
