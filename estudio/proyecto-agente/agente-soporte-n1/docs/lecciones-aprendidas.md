# Lecciones aprendidas

Lo que el proyecto enseñó al construirlo, en un solo lugar. Cada lección es corta y remite al documento donde está el detalle, para no repetirlo. Se agrega una lección cuando una prueba, una revisión o una consulta del usuario deja algo que vale la pena recordar. Las lecciones que conectan con el curso citan su sección; el resto es técnico y **no viene en el curso**.

Última actualización: 2026-11-19 (etapas 0 a 3 y prueba con OpenRouter).

## 1. Sobre el agente, lo que el curso explica

| Lección | Curso | Detalle |
|---|---|---|
| **Un agente puede decir que hizo algo que no puede hacer.** Sin herramienta para escalar, el agente respondía “he escalado su caso”, y nadie lo recibía: un fallo silencioso. Por eso escalar es código (`escalar_a_humano`) y el aviso al cliente lo escribe el programa, no el modelo | 3.3, fallos silenciosos | `pruebas/2026-11-18-etapas-0-y-1.md` |
| **El modelo agrega pasos que el documento no dice.** Con un fragmento de una línea, respondió cuatro pasos, tres inventados. El prompt ahora pide usar solo los pasos del fragmento y citar la fuente, y las evals lo medirán | 3.3, alucinaciones; 2.5, solo soluciones documentadas | `pruebas/2026-11-19-etapa-3.md` |
| **El modelo toma decisiones razonables que nadie escribió.** Escaló un pedido de descuento con amenaza de irse, aunque el SOP solo decía “no ofrezcas descuentos”. Es razonable, pero no está escrito: por eso hay que probar los límites, no solo los casos normales | 2.4, el agente opera literalmente; 2.6, validación | `pruebas/2026-11-18-etapas-0-y-1.md` |
| **Lo que exige garantía va en código, no en el prompt.** El modelo no tiene reloj, así que no puede cumplir los 8 minutos; tampoco se puede confiar en que siempre escale una cancelación. El modelo decide lo que requiere razonamiento; el código controla los topes, las herramientas permitidas y, desde la etapa 4, las reglas graves | 2.5, protocolos de escalamiento; 1.2, kill switch | `buenas-practicas.md`; plan, “Cómo funciona cada regla” |
| **Dos modelos pueden llegar al mismo resultado por caminos distintos.** Con OpenRouter, el agente escaló la “máquina de café” sin buscar, porque las integraciones están en lo que no atiende; Gemini buscó antes. Las métricas del Módulo 3 miden resultados y caminos, así que cambiar de modelo es cambiar de agente y hay que validarlo de nuevo | 2.6, validación antes de producción; 3.3, deriva | `pruebas/2026-11-19-openrouter.md` |
| **Lo que escribe el cliente son datos, no órdenes.** Un mensaje puede traer instrucciones (“ignora tus instrucciones”). El texto del cliente y lo que devuelven las herramientas van marcados como datos, y un texto no puede “cerrar” esa marca desde adentro | 2.6, dimensión adversarial | `revisiones/2026-11-19-revision-etapa-3.md`, I3 |

## 1b. Sobre el prompt maestro

| Lección | Curso | Detalle |
|---|---|---|
| **El prompt se lee en cada mensaje, pero no se guarda en la base.** En cada mensaje del cliente, el programa lee `prompt_soporte_n1.md`, le agrega “Lo que no atiendes” desde el registro de agentes y envía todo al modelo remoto, junto con la conversación. La base guarda los mensajes, el estado, los tokens y el contexto de escalamiento, pero no el texto del prompt ni lo que se envió en cada llamada; desde la etapa 4, la auditoría guardará la versión del prompt, que hoy es un número escrito a mano | 2.5, JD+SOP; 2.6, aprobación | `agente.py`, `armar_instrucciones()` |
| **Desplegado, el prompt viaja dentro de la imagen Docker.** Cambiarlo exige reconstruir la imagen: nadie cambia las instrucciones de un agente en producción sin pasar por el proceso. El riesgo que queda es que alguien edite el texto sin cambiar el número de versión | 2.6, validación antes de producción | `decisiones.md`, D15 |
| **Un key vault es para secretos; el prompt es configuración.** El usuario pensó en guardar el prompt en OpenBao. Daría versiones y registro de lecturas, pero suma un servicio, no sabe si una versión pasó las evals y fue aprobada (lo que pide el curso), hace más difícil revisar los cambios que git, y el prompt igual viaja completo al modelo. Donde un vault sí encaja es en las claves de API, aunque el programa necesite a su vez una credencial para leerlo (más acotada y revocable) | 2.6, aprobación con nombre | `decisiones.md`, D15 |
| **Para que una regla del proceso se cumpla, el código tiene que poder comprobarla.** “Un prompt se usa solo si fue aprobado” no se cumplía con un número escrito a mano; con una huella del texto aprobado, el agente puede comprobarlo en cada mensaje. Guardar todo en cada llamada parecía más seguro, pero copia datos del cliente y no responde la pregunta que importa: qué instrucciones aprobadas atendieron el caso | 2.7, criterios de aceptación obligatorios | `decisiones.md`, D15 |

## 2. Sobre el RAG

| Lección | Detalle |
|---|---|
| **Un parecido alto no garantiza que haya una solución.** La búsqueda siempre devuelve lo menos lejano: “máquina de café”, sin documento, dio 0,70, más que algunas consultas correctas. Decidir si el fragmento resuelve el caso le toca al modelo, leyendo, y no a un umbral | `pruebas/2026-11-18-etapa-2.md`; `decisiones.md`, D8 |
| **La sección más parecida suele ser la introducción,** que describe el problema; los pasos están en otra sección. Por eso el agente recibe los 5 fragmentos más parecidos, no solo el primero | `pruebas/2026-11-18-etapa-2.md` |
| **Cortar por secciones, con el título adelante,** hace que cada fragmento se entienda solo y que la cita sea precisa (“documento > sección”) | `decisiones.md`, D8 |
| **Los vectores solo se comparan con los de su mismo modelo.** Cambiar el modelo de embeddings obliga a recargar la base; por eso el chat y los embeddings tienen cada uno su proveedor, y el chat se puede cambiar sin recargar | `embeddings-y-vectores.md`; `decisiones.md`, D8 y D13 |

## 3. Sobre los modelos y los proveedores

| Lección | Detalle |
|---|---|
| **No todos los modelos saben usar herramientas.** Sin eso, el agente no puede buscar ni escalar. Se ve en la lista del proveedor (“tools”), pero lo seguro es probarlo con `python -m scripts.prueba_conexion` | `proveedores-de-modelos.md` |
| **El mensaje del modelo se devuelve tal cual.** Gemini 3 agrega una firma de pensamiento a cada pedido de herramienta y OpenRouter puede agregar `reasoning_details`; si no vuelven intactos en la llamada siguiente, el proveedor rechaza el pedido (error 400) | `decisiones.md`, D11 |
| **Los proveedores fallan, y no es raro.** En un solo día, Gemini tuvo dos llamadas de más de 60 segundos y un error 503 por alta demanda. Por eso cada llamada tiene un límite de espera, sin reintentos automáticos, y si falla el ticket se escala por regla: el cliente nunca queda sin respuesta | `pruebas/2026-11-19-etapa-3.md`; `proveedores-de-modelos.md` |
| **La demora depende mucho del proveedor:** de 2 a 42 segundos por llamada con Gemini y de 2 a 8 con el modelo de OpenRouter, el mismo día. Pesa en la meta de 3 minutos del curso (sección 2.5) | `pruebas/2026-11-19-openrouter.md` |
| **Siempre conviene un tope de salida (`max_tokens`).** Sin él, OpenRouter reserva saldo para la salida máxima del modelo (65.536 tokens) aunque el agente escriba menos de 300, y con poco saldo rechaza el pedido | `pruebas/2026-11-19-openrouter.md` |
| **La capa gratuita sirve para probar, no para operar:** los modelos gratuitos comparten un cupo entre todos los usuarios y pueden estar saturados (error 429) | `pruebas/2026-11-19-openrouter.md` |
| **Si cambiar de proveedor es editar a mano, el `.env` se desordena.** Comentar y descomentar líneas dejó el `.env` distinto de la plantilla (variables faltantes, comentarios viejos, una clave en una línea comentada). Con el proveedor elegido por nombre, cambiar es editar dos líneas, y `start-dev.bat` avisa si el `.env` se separa de `example.env` | `decisiones.md`, D14 |
| **Que un agente no mire las claves es una conducta, no una garantía.** Cualquier agente con acceso a la terminal puede leer un `.env`, y el `.gitignore` solo protege de git. La garantía la da la herramienta: reglas de permisos y un hook que bloquea cualquier comando que mencione un `.env`, instalado en la configuración global del usuario para que valga en todos sus proyectos sin poner nada en el repositorio, y probado con 31 casos y en vivo. Vale para cualquier modelo. A nivel global hay que dejar pasar las plantillas de otros proyectos (`.env.example` y similares) | `AGENTS.md` de la raíz, “Claves fuera del alcance de los agentes” |
| **Para disponibilidad, respaldo; balancear no.** Repartir llamadas entre dos modelos mezcla dos agentes en las mismas métricas | `proveedores-de-modelos.md` |
| **El costo real coincidió con la estimación:** 0,0012 dólares por ticket resuelto, igual a lo estimado antes de programar | `costos.md` |

## 4. Sobre la base de datos y Docker

| Lección | Detalle |
|---|---|
| **El contenedor de PostgreSQL ejecuta los SQL solo la primera vez.** Su programa de arranque revisa si la base existe y, si no, ejecuta lo que haya en `/docker-entrypoint-initdb.d`, una carpeta (el `.d` no es extensión: en Linux marca carpetas con piezas que se recorren todas) donde el compose monta nuestra carpeta `postgres/`. Editar un SQL no cambia una base que ya existe | `src/docker/postgres/README.md` |
| **`localhost` en Windows puede costar 2 segundos por conexión,** porque prueba primero por IPv6 y el puerto solo está publicado en IPv4. Con `127.0.0.1`, las pruebas bajaron de 38 a 5 segundos | `decisiones.md`, D12 |
| **Que confirme quien llama permite probar con la base real.** Las funciones escriben sin confirmar; la consola confirma al terminar cada mensaje y las pruebas deshacen todo al final. Efecto curioso: los números de ticket saltan, porque PostgreSQL no retrocede sus contadores | `decisiones.md`, D11 |
| **Un `rollback` también borra lo que se creó en ese mismo intento:** la consola quedaba atrapada en un ticket que ya no existía | `revisiones/2026-11-19-revision-etapa-3.md`, I1 |

## 5. Sobre el código y las pruebas

| Lección | Detalle |
|---|---|
| **Separar el producto de los scripts de asistencia** evita olvidar para qué servía cada archivo: `aplicacion/` es el agente y `scripts/` se ejecuta suelto; la dependencia va en un solo sentido | `decisiones.md`, D10 |
| **Un modelo falso prueba gratis lo que controla el código** (topes, herramientas, escalamientos), siempre igual. El modelo real se prueba aparte, en las evals | `src/backend/tests/integracion/README.md` |
| **Una prueba puede pasar por la razón equivocada.** El modelo falso avisaba si se lo llamaba de más, pero el bucle convertía ese aviso en un escalamiento; ahora cada prueba cuenta las llamadas | `revisiones/2026-11-19-revision-etapa-3.md`, I5 |
| **Las pruebas también revisan los arreglos.** Al endurecer la marca de datos, una prueba mostró que la fuente “documento > sección” le llegaba al modelo como `&gt;`; se corrigió antes de usarlo | `pruebas/2026-11-19-etapa-3.md` |
| **Una revisión independiente encuentra lo que quien escribió no ve:** la de la etapa 3 encontró cuatro errores reales (el ticket fantasma, las fallas de herramientas sin escalar, la marca de datos que se podía saltar y tipos de paso que no cabían en la auditoría), y 11 citas al curso imprecisas | `revisiones/` |
| **La documentación repetida queda falsa.** Un conteo de pruebas escrito en siete lugares queda desactualizado en todos; cada dato va en un solo lugar y los demás lo enlazan | `revisiones/2026-11-19-revision-etapa-3.md`, I8 |

## 6. Sobre el equipo de trabajo (Windows)

| Lección | Detalle |
|---|---|
| **Otro programa puede bloquear el entorno virtual** (el editor o el antivirus): renombrar la carpeta y crear otra, y borrar la vieja como administrador | `README.md` del proyecto |
| **En PowerShell, un programa de la carpeta actual se ejecuta con `.\`** (`.\start-dev.bat`); sin eso, no lo encuentra | `README.md` del proyecto |
| **Los `.bat` necesitan saltos de línea CRLF;** `.gitattributes` lo asegura, y algunas herramientas de la terminal los convierten sin avisar | `.gitattributes` de la raíz |
