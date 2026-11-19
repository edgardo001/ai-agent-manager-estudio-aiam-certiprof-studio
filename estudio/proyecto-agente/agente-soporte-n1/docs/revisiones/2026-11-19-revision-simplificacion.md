# Revisión de simplificación, 2026-11-19

Pedida por el usuario porque el proyecto “sigue creciendo en archivos” y no sabía si eso ayudaba a entender el curso. Tres revisiones de solo lectura con elephant-goldfish-model, en paralelo, cada una con tres revisores: el código (simplicidad, reutilización y diseño), la documentación del proyecto (estructura, simplicidad y lector nuevo) y los archivos de gestión de la raíz (simplicidad, estructura y redacción). Criterio del usuario, que manda: ¿cada archivo ayuda a entender un concepto del curso o a operar el agente, o es registro, referencia o detalle técnico? El agente que las pidió comprobó los hallazgos principales (M1, M2 y los datos viejos 1 a 3 de la documentación).

**Estado:** pendiente de la decisión del usuario.

## Resultado general

- **El código ya es corto y se lee de corrido:** en líneas se gana poco (de 50 a 70 seguras sobre unas 2.000). Ningún revisor propone revertir una decisión.
- **Lo que pesa es la cantidad de archivos y la información repetida:** el mismo dato aparece en 3 a 6 lugares y varios ya quedaron viejos.
- **La historia crece más que las reglas:** el registro de cambios de `AGENTS.md` y la mitad de `MEMORY.md` repiten lo que ya está en el plan, en las decisiones, en las lecciones y en git.

## Dos errores reales del código (corregir antes de simplificar)

1. **M1:** si el modelo pide escalar en la sexta llamada, o en la que pasa el tope de tokens, el código revisa antes esos límites y escala “por regla”, sin el motivo ni el resumen del modelo; la persona pierde el contexto (secciones 2.5 y 4.3). Arreglo: atender el pedido de escalar antes de revisar los límites, con una prueba nueva. Lo introdujo la aplicación de la revisión de la etapa 3.
2. **M2:** `cargar_conocimiento.py` tiene un `DELETE` propio, cuando la regla dice que todo el SQL va en `base_de_datos.py`. Arreglo: una función `borrar_fragmentos()`.

## Cantidad de archivos: antes y después

| Parte | Hoy | Con lo seguro | Con lo discutible |
|---|---|---|---|
| Código, scripts, pruebas, Docker y `.bat` | 39 | 35 | 30 (27 si se reconsidera una decisión del usuario) |
| Documentación del proyecto (README, `docs/` y README de `src/`) | 35 | 35 (solo correcciones) | 29 (27 en la variante más agresiva) |
| Documentos que hay que abrir para entender el proyecto | 5 | 5 | 3: README, plan y lecciones |
| `AGENTS.md` (líneas) | 198 | unas 168 | unas 150 |
| `MEMORY.md` (líneas) | 123 | unas 113 | unas 75 |

## Simplificar ahora (seguro)

**Código:**

- unir los README de `tests/unitarias` y `tests/integracion` en `tests/README.md`;
- pasar `test_revisar_env.py` y `test_cargar_conocimiento.py` a `test_piezas_simples.py`;
- quitar del `.bat` las revisiones de la etapa 0 que ya no pueden ocurrir y el `docker compose down` repetido;
- quitar la rama de “persona” que hoy no ocurre;
- una sola fuente para el número 5 de fragmentos y para la lista de documentos;
- separar los dos modos de `probar_busqueda.py`;
- simplificar `config.py`, `modelo.py` y las pruebas casi iguales;
- reemplazar la clase `ClienteFalso` de las pruebas;
- que `prueba_conexion.py` pruebe con las herramientas reales del agente;
- corregir los comentarios viejos del esquema.

**Documentación:**

- corregir los datos viejos y las contradicciones:
  - el README de `postgres` dice que los tickets de ejemplo llegan en la etapa 3 (son de la 7);
  - `evals-del-llm.md` cita “grupos” del plan que ya no existen y una casilla con `atender_ticket()`, que es otra función;
  - D13 describe variables reemplazadas por D14;
  - el plan dice que los embeddings usan la clave del chat;
  - el árbol de `docs/` del plan está incompleto;
  - los diagramas presentan a Gemini como único proveedor;
  - nombres de pruebas y cifras de costo no coinciden;
  - el mapa `docs/README.md` está desactualizado;
- una sola fuente para cada dato:
  - el estado de las etapas, en el plan;
  - los conteos y las mediciones, en `pruebas/`;
  - las licencias, en la tabla del plan;
  - los scripts `.bat`, en el README;
  - el porqué del 768, en embeddings;
  - las cifras, en costos;
  - la aprobación del prompt, en D15;
  - los tipos de prueba, en la estrategia;
- en el plan, condensar las reglas largas con un enlace a su decisión y fusionar “Decisiones del usuario” con el registro; en `decisiones.md`, un índice al inicio;
- definir una vez JD+SOP, EGM, Nubesoft y los tres sentidos de “nivel”.

**Archivos de gestión:**

- `AGENTS.md`: el registro de cambios queda en una línea por fecha (el detalle está en `MEMORY.md` y en git); las secciones de la conversión ya terminada quedan en 3 líneas; las reglas del proyecto de agente pasan al plan y `AGENTS.md` remite a él (antes se copian al plan las dos reglas que solo están en `AGENTS.md`); se unifican las reglas repetidas; se corrigen las desactualizadas; se reordenan las secciones para que el mantenimiento vaya primero;
- `MEMORY.md`: se fusionan las decisiones que ya son reglas, se corrigen las rutas viejas, se agrega el estado del proyecto y la entrada más larga (unas 900 palabras) pasa a 4 entradas cortas con enlaces;
- `.gitignore`: sobra `.venv/`, porque `.venv*/` ya lo cubre.

## Discutible (decide el usuario)

1. **Fusionar documentos:** `embeddings-y-vectores.md` con `buenas-practicas.md` en `rag.md`; `proveedores-de-modelos.md` con `costos.md` en `modelos-y-costos.md`; `pruebas-adversariales.md` dentro de `estrategia-de-pruebas.md`; `anonimizacion-de-datos.md` a `referencia/`; eliminar `referencia/ruta-de-construccion.md` (diseño reemplazado; git lo conserva) y la tabla de equivalencias del plan. Cambia nombres que citan `AGENTS.md` y las lecciones.
2. **Condensar el registro de cambios del plan** (cerca del 35% del archivo) a una línea por entrada, dentro del mismo plan.
3. **Código:** quitar los dos `__init__.py` (bajo riesgo, por verificar con pytest); unir `prueba_conexion.py` y `revisar_env.py` en un script con dos modos (menos archivos, pero se lee peor); sacar de `config.py` los supuestos que solo usa `estimar_costos.py`; quitar `globals()` de `config.py`; quitar de `example.env` las variables de la etapa 7.
4. **`MEMORY.md` solo con lo del curso y el estado:** lo del proyecto queda en sus documentos, con 4 a 6 líneas de estado y enlaces (unas 35 líneas menos). Antes se rescatan los pendientes que solo están ahí.
5. **Las reglas de la conversión del curso:** compactarlas dentro de `AGENTS.md` (recomendado, no suma archivos) o pasarlas a un archivo aparte (AGENTS.md bajaría a unas 95 líneas, pero suma un archivo).
6. **Carpetas vacías de pruebas** (adversariales, evals, e2e): crearlas recién en su etapa. Choca con la decisión del usuario de tener los cinco tipos en carpetas desde el inicio.
7. **Pendientes vencidos de `MEMORY.md`** (la nota de la memoria interna y `estudio/fichas/`, que ya no existe): borrarlos.

## No tocar (parece complejo, pero se justifica)

- En el código: la separación de módulos, el diccionario `turno` (es el punto de la auditoría de la etapa 4), `opciones_de_llamada()` y `temperatura` (etapa 5), `PROVEEDORES` y `revisar_env` (D14), las dos revisiones del tope de tokens, el esquema y los comentarios con referencia al curso.
- En la documentación: el flujo en 14 pasos, “Qué pide el curso y dónde se cubre”, la supervisión del Módulo 3 y “Cómo funciona cada regla” del plan, que son lo que une el proyecto con el curso; D2, D7, D11, D14 y D15; el golden dataset y los umbrales de las evals; `pruebas/` y `revisiones/`, que son registros con fecha.
- En la raíz: `README.md`, `.gitattributes` y las seis reglas de mantenimiento del usuario, que solo se redactan más corto.

## Orden propuesto

1. Corregir M1 y M2 (con su prueba).
2. Aplicar lo seguro del código, la documentación y los archivos de gestión.
3. Aplicar lo discutible que elija el usuario.
4. Actualizar los enlaces, regenerar el índice y medir de nuevo archivos y líneas.
