# Revisión: dónde vive el prompt maestro, cómo se versiona y qué se guarda, 2026-11-19

Análisis de diseño de solo lectura con elephant-goldfish-model (tres revisores: diseño, simplicidad e ideas alternativas, coordinados por su sintetizador), pedido por el usuario. Él creía que en cada consulta el prompt se guardaba en la base antes de ir al modelo, y propuso guardarlo en un key vault (OpenBao). El agente que lo pidió comprobó contra el código y el curso los hallazgos M3, M6 y M8 y las citas a las secciones 2.7 y 4.6.

**Estado:** aplicada el 2026-11-19: el usuario aprobó B+ (decisión D15), con sus decisiones al final.

## Cómo funciona hoy

En cada mensaje del cliente, el programa lee `prompt_soporte_n1.md`, le agrega “Lo que no atiendes” desde `registro_agentes` y envía todo al modelo, junto con la conversación; un caso normal hace 3 llamadas y cada una reenvía las instrucciones. La base guarda los mensajes, el estado, los tokens, el costo y el contexto de escalamiento, pero no el texto del prompt ni lo enviado en cada llamada. Desplegado, el prompt viaja dentro de la imagen Docker. El prompt no es un secreto frente al proveedor: viaja completo en cada llamada.

## Qué dice el curso

Respalda controlar las versiones del prompt: validar antes de producción (2.6); los criterios de aceptación son “una política organizacional, no una recomendación” y el registro guarda la fecha de la última validación (2.7); el audit trail pide qué decidió el agente y por qué (Módulo 1, pregunta 9); la deriva se detecta contra los primeros 30 días (3.3); se interviene si el CSAT baja “coincidiendo con un cambio en las instrucciones” (3.4, segunda señal); y la sección 4.6 menciona una auditoría de prompt. No vienen del curso las huellas, git, las trazas por llamada ni los key vaults.

## Hallazgos sobre el diseño actual

| # | Hallazgo |
|---|---|
| M1 | Nada hace cumplir “una versión se usa solo si pasó las pruebas y fue aprobada”: editar el archivo cambia al agente desde el mensaje siguiente |
| M2 | La versión escrita a mano no identifica el texto: dos textos distintos pueden decir “3” |
| M3 | “Lo que no atiendes” queda fuera de toda versión: un `UPDATE` a `fuera_de_alcance` cambia lo que recibe el modelo sin dejar rastro |
| M4 | No se registran el proveedor ni el modelo, aunque ya se alterna entre Gemini y OpenRouter, y las evals deben aprobar un cambio de prompt o de modelo |
| M5 | La aprobación guarda solo la última versión y se pierde la historia de fechas que necesita la señal 2 de 3.4 |
| M6 | Si falta el archivo del prompt, el mensaje se pierde con el `rollback`, contra D11 |
| M7 | Una verificación que bloquee siempre rompería las evals y el desarrollo, que usan versiones aún sin aprobar |
| M8 | `evals-del-llm.md` dice que las evals usan `temperature=0`, pero el código no la fija (pendiente de la etapa 3 que no se marcó) |

Menores: los fragmentos se anotan sin `hash_documento` (D8 lo promete para la etapa 4); `leer_agente()` tendrá que traer la huella aprobada; la huella aprobada debe calcularse antes y después de las pruebas; conviene dejar escrito si mandan las restricciones del prompt o las de `registro_agentes`; la huella se calcula sobre el texto ya leído, para que Windows y Docker den la misma.

## Opciones

| Opción | Qué es | Resultado |
|---|---|---|
| A | como hoy: archivo, versión a mano y git | no hace cumplir la aprobación ni distingue un cambio de instrucciones de una deriva |
| B | A más la huella del prompt aprobado y una verificación por ticket | cubre el archivo, pero no `fuera_de_alcance` (M3) |
| C | B más el texto de cada versión en la base; opcionalmente, leerlo desde la base | guardar el texto, sí; leerlo desde la base crea dos fuentes de verdad: postergado |
| D | traza completa de cada llamada en PostgreSQL (lo que el usuario imaginaba) | de 20 a 80 KB por ticket, el mensaje del cliente copiado hasta 6 veces y contra “guardar solo lo necesario”; no permite repetir una respuesta exacta. Se mantiene postergada, como Langfuse |
| E | el prompt en OpenBao | descartada: el prompt no es un secreto, el versionado del vault no es una aprobación con evals, abre otro canal de cambios en caliente y suma un servicio que el curso no exige |
| B+ | propuesta consolidada (abajo) | recomendada |

**OpenBao para las claves de API:** es su uso natural, pero hoy no reduce un riesgo real. Hay un solo equipo y una persona, el archivo de claves está fuera de git y de la imagen, y la credencial para leer el vault quedaría en el mismo lugar que las claves (el problema del “secreto cero”). Se propone en la tabla de lo postergado, con la misma señal que la autenticación: cuando el sistema salga del equipo local, haya varios servidores o personas con acceso, o haga falta rotar y auditar las claves. Antes hay que confirmar su licencia (MPL 2.0, no verificada) y pedir la excepción.

## Propuesta B+ (sin tablas nuevas)

1. **La huella cubre lo que se envía de verdad:** SHA-256 de las instrucciones completas (el archivo más “Lo que no atiendes”), calculada en `aplicacion/`. La huella es la identidad y el número de versión queda como etiqueta para personas.
2. **Cada paso de la auditoría guarda** la versión, la huella, el proveedor y el modelo, y los fragmentos con su documento, sección, huella del documento y parecido, sin el texto.
3. **La aprobación queda como evento:** `aprobar_prompt.py` guarda la huella aprobada en `registro_agentes` y una fila de intervención en `registro_auditoria` con la versión, la huella, el modelo, el resultado de las evals y el texto completo, una sola vez (unos 4 KB). Así se tiene lo útil de C sin tabla nueva.
4. **Verificación por mensaje:** si la huella no coincide y la barrera está activa, el ticket se escala por regla (“instrucciones sin aprobar”), lo que respeta D11; en desarrollo y en las evals, la barrera está apagada y solo queda anotado.
5. **Si falta el archivo del prompt,** se escala por regla (M6).

## Recomendación

- **Ahora:** registrar la decisión, agregar a lo postergado OpenBao para las claves y C con lectura desde la base, y corregir M8.
- **Etapa 4:** registrar sin bloquear (huella, versión, proveedor y modelo en cada paso; huella de los documentos; escalar si falta el archivo).
- **Etapa 5:** `aprobar_prompt.py` con la huella y la fila de intervención; activar la barrera.
- **Postergado:** C con lectura desde la base, D (como Langfuse) y OpenBao para las claves, cada uno con su señal. OpenBao para el prompt no se retoma.

**Decisiones del usuario pendientes:** si un cambio de modelo bloquea o solo queda anotado; el nombre y el valor por defecto de la variable de la barrera; si se mantiene el número de versión escrito a mano como etiqueta.

**Sin verificar:** la licencia de OpenBao; los tamaños estimados (caracteres por token, prompt armado, firmas de los proveedores, compresión de PostgreSQL); cómo invocarán al agente las evals; el contenido del futuro `Dockerfile` y `.dockerignore`.

## Decisiones del usuario

1. **Adoptar B+.** Antes hubo que aclarar que B+ no usa OpenBao: el prompt sigue en el archivo y la huella se guarda en PostgreSQL; OpenBao solo aparece, postergado, para las claves de API.
2. **Un cambio de modelo o de proveedor solo queda anotado,** sin bloquear.
3. **El número de versión escrito a mano se mantiene** como etiqueta para las personas; la huella es la identidad.

Aplicado ese día: D15 en `decisiones.md`; en el plan, las etapas 4 y 5, la regla de aprobación y tres filas nuevas de lo postergado; y M8 corregido en el código (`opciones_de_llamada()` en `modelo.py`, con su prueba). El resto se programa en las etapas 4 y 5.
