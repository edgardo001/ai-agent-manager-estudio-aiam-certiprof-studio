# Seguridad: los Top 10 de OWASP aplicados al proyecto

Pedido del usuario (2026-11-19): documentar los dos Top 10 de OWASP que tocan a este proyecto, con su fecha, para usarlos al mejorar el código, **siempre manteniendo la simpleza** (reglas 2 y 3 del plan). Nada de esto viene del curso; se relaciona con los permisos mínimos (Módulo 2, sección 2.3), las restricciones del SOP (2.5) y la validación adversarial (2.6).

OWASP (Open Worldwide Application Security Project) es una fundación sin fines de lucro que publica listas de los riesgos de seguridad más comunes. Dos aplican aquí:

- **OWASP Top 10 for LLM Applications:** los riesgos de las aplicaciones que usan un modelo de lenguaje, como el agente.
- **OWASP API Security Top 10:** los riesgos de una API, como la que llega en la etapa 6.

## Fechas: cuándo se creó este documento y cuándo revisarlo

| Dato | Valor |
|---|---|
| Creado | 2026-11-19 |
| Edición LLM usada | **2025**, publicada por OWASP el 2024-11-17 ([genai.owasp.org/llm-top-10](https://genai.owasp.org/llm-top-10/)) |
| Edición API usada | **2023** ([owasp.org/API-Security](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)); el proyecto dice “Latest Version: 2023” |
| Última revisión de las fuentes | 2026-11-19 |
| Próxima revisión | **2027-05-19** (cada seis meses), y antes de empezar las etapas 6 y 7 |

**Discrepancia por revisar:** varios sitios secundarios (por ejemplo [Picus Security](https://www.picussecurity.com/resource/blog/owasp-llm-top-10-2026-what-every-security-team-should-know) y [Aembit](https://aembit.io/blog/the-owasp-top-10-for-llm-applications-2026-what-changed-and-why-it-matters/)) hablan de una edición 2026 de la lista LLM, publicada en agosto de 2026, con otro orden (Excessive Agency en tercer lugar) y un riesgo renombrado (System Prompt Leakage pasaría a llamarse Hidden Context Exposure). El 2026-11-19, la página oficial solo mostraba la edición 2025, así que este documento usa la 2025. En la próxima revisión se confirma si la 2026 ya es oficial y se actualizan los nombres; los riesgos son los mismos.

**Cómo se usa:** antes de cerrar cada etapa se recorre la columna “Pendiente” de las dos tablas. Una mejora se hace solo si cabe en pocas líneas y se entiende de principio a fin; si exige una librería, un servicio o mucho código, se anota en la tabla de lo postergado del plan con su señal. Cada mejora hecha pasa de “Pendiente” a “Ya cubierto”.

## OWASP Top 10 for LLM Applications, edición 2025

Nombres e identificadores tal como aparecen en el sitio oficial. Las columnas “Ya cubierto” y “Pendiente” son el análisis del proyecto, no texto de OWASP.

| # | Riesgo | Qué es, en una frase | Ya cubierto en el proyecto | Pendiente |
|---|---|---|---|---|
| LLM01:2025 | Prompt Injection | un texto de entrada cambia lo que hace el modelo | mensajes y fragmentos marcados como datos (`marcar_como_datos()`), sección “Datos frente a instrucciones” del prompt, reglas en código antes y después del modelo (D16), pruebas adversariales de las reglas | casos adversariales con el modelo real en las evals (etapa 5) |
| LLM02:2025 | Sensitive Information Disclosure | el sistema deja ver datos personales, de negocio o claves | `buscar_cliente` solo lee al cliente del ticket; `revisar_respuesta()` bloquea el código, el nombre o la empresa de otro cliente; las claves fuera del alcance de los agentes (`AGENTS.md`) | un cliente que escribe su contraseña: no debe repetirse (caso de las evals); datos reales, ver `referencia/anonimizacion-de-datos.md` |
| LLM03:2025 | Supply Chain | librerías, modelos o servicios de terceros comprometidos | licencias revisadas antes de instalar (regla 13), versiones acotadas en `requirements.txt`, modelos de proveedores conocidos | fijar versiones exactas antes de exponer el sistema |
| LLM04:2025 | Data and Model Poisoning | datos de entrenamiento o de búsqueda manipulados para meter errores o sesgos | no se entrena ningún modelo; la base de conocimiento está en git, con la huella de cada documento (D8) | quién puede cambiar la base y con qué revisión, cuando haya más de una persona |
| LLM05:2025 | Improper Output Handling | la salida del modelo se usa sin validarla | `revisar_respuesta()`; respuestas cortadas o vacías se escalan; la consola muestra texto plano | el frontend (etapa 7) debe mostrar las respuestas como texto (`textContent`), nunca como HTML (`innerHTML`) |
| LLM06:2025 | Excessive Agency | el agente tiene más funciones, permisos o autonomía de los necesarios | tres herramientas, dos de solo lectura y la de escalar; ninguna cambia la cuenta; tope de llamadas por mensaje; kill switch (D16) | nada por ahora: es lo mejor cubierto |
| LLM07:2025 | System Prompt Leakage | el prompt de sistema queda a la vista, y con él lo que no debía | el prompt no guarda secretos ni claves (D15: no es un secreto) | caso de las evals que pide el prompt: medir qué responde |
| LLM08:2025 | Vector and Embedding Weaknesses | debilidades de los sistemas con RAG y vectores | una sola base, sin datos de clientes en los vectores; los fragmentos llegan marcados como datos | permisos por documento si algún día hay documentos que no todos pueden ver |
| LLM09:2025 | Misinformation | el modelo produce información falsa que parece cierta | solo soluciones documentadas, con su fuente; el prompt prohíbe inventar | el juez de fidelidad y de alucinación (etapa 5) y la revisión por muestreo (etapa 7) |
| LLM10:2025 | Unbounded Consumption | uso sin límites que causa caídas o gastos | largo máximo del mensaje, tope de tokens de salida y por ticket, tope de llamadas por mensaje, 60 segundos de espera sin reintentos | límite de pedidos por minuto en la API (D4, etapa 6) |

## OWASP API Security Top 10, edición 2023

Para la API de la etapa 6. Hoy no hay API: la consola corre solo en el equipo (D4). Las columnas “Ya cubierto” y “Pendiente” son el análisis del proyecto.

| # | Riesgo | Qué es, en una frase | Ya cubierto o decidido | Pendiente (etapa 6) |
|---|---|---|---|---|
| API1:2023 | Broken Object Level Authorization | se puede leer o cambiar un objeto ajeno cambiando su identificador | D4: cada ruta con un ticket comprueba que es del cliente que pide | escribirlo y probarlo en la API |
| API2:2023 | Broken Authentication | la autenticación falla y alguien se hace pasar por otro | D4: sin autenticación, solo en `127.0.0.1`; la identidad saldrá del token al exponerla | la capa de autenticación, cuando se exponga |
| API3:2023 | Broken Object Property Level Authorization | se ven o se cambian campos de un objeto que no corresponden | nada aún | los modelos Pydantic de respuesta exponen solo lo necesario (al cliente, ni el historial ni los costos) |
| API4:2023 | Unrestricted Resource Consumption | pedidos que agotan recursos o gastan servicios pagados | los topes del agente (ver LLM10) | límite de pedidos por minuto (D4) |
| API5:2023 | Broken Function Level Authorization | un usuario común usa funciones de administrador | D4: separar el acceso del cliente del acceso del AI Agent Manager | rutas de administración (kill switch, aprobar el prompt) separadas de las del cliente |
| API6:2023 | Unrestricted Access to Sensitive Business Flows | un flujo de negocio se abusa en masa, aunque el código esté bien | nada aún | crear tickets en masa gasta el modelo: límite de tickets por cliente |
| API7:2023 | Server Side Request Forgery | la API va a buscar una dirección que le da el usuario | no aplica: la API no recibe direcciones | revisar si alguna vez se agrega |
| API8:2023 | Security Misconfiguration | configuraciones inseguras por defecto o descuidadas | solo en `127.0.0.1`; claves fuera del repositorio | sin modo de depuración en QA; CORS solo para el propio frontend |
| API9:2023 | Improper Inventory Management | rutas o versiones viejas que nadie recuerda y siguen abiertas | el registro de agentes (2.7) es el inventario del agente | la documentación OpenAPI de FastAPI como inventario de rutas |
| API10:2023 | Unsafe Consumption of APIs | se confía de más en lo que devuelve un servicio de terceros | lo que devuelve el modelo se revisa (`revisar_respuesta()`, respuestas cortadas o vacías) | igual con cualquier servicio nuevo |

## Fuentes

- OWASP GenAI Security Project, “OWASP Top 10 for LLM Applications 2025”, 2024-11-17: https://genai.owasp.org/llm-top-10/
- OWASP API Security Project, “OWASP Top 10 API Security Risks, 2023”: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- Leídas el 2026-11-19. Las mitigaciones detalladas de cada riesgo están en la página de cada uno en esos sitios; aquí solo se resume lo que aplica al proyecto.
