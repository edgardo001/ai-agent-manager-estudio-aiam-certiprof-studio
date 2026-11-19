# AGENTS.md: reglas del repositorio

Este archivo tiene las reglas que sigue cualquier agente que trabaje en este repositorio: el curso convertido para escuchar, el material de estudio y el proyecto de agente. La conversión del curso ya terminó; sus reglas, al final, sirven para corregir los módulos y para escribir cualquier texto nuevo pensado para la voz.

**Antes de empezar y al terminar cada tarea:** lea “Mantenimiento y reglas transversales”. Al cerrar cualquier cambio se actualizan `AGENTS.md`, `MEMORY.md` y `README.md`, sin esperar a que el usuario lo pida, y no se hace commit sin su autorización.

## Propósito y contexto del usuario

El repositorio convierte `certiprof-ai-agent-manager-aiam-guia-de-autoestudio-es.pdf` (programa “AI Agent Manager (AIAM™)”, 97 páginas, 5 módulos) en prosa continua, un archivo por módulo en `estudio/modulos/` (el primero incluye el título general), **sin perder ningún concepto, dato, cifra, fuente ni ejemplo**, y suma material de repaso y un proyecto de agente basado en el curso.

El usuario estudia escuchando el material con un programa text-to-speech; por eso todo lo que se escribe para el curso debe leerse bien en voz alta. Quiere buscar rápido los términos y dudas que va consultando: antes de responder una consulta sobre el contenido, se lee “Preguntas del usuario” y se sigue su formato y su largo estándar.

## Mantenimiento y reglas transversales

Las reglas de esta sección son del usuario: no se eliminan, solo se pueden reformular.

**Actualización periódica obligatoria:** `AGENTS.md`, `MEMORY.md` y `README.md` se actualizan siempre, en la misma sesión en que ocurre el cambio y sin esperar a que el usuario lo pida. Ninguna tarea se da por terminada sin este cierre:

1. **`AGENTS.md` (este archivo): las reglas.** Se actualiza cuando aparece una regla nueva del usuario, un caso nuevo de conversión o formato, o un tipo nuevo de material en `estudio/`. Cada cambio se anota en el “Registro de cambios”.
2. **`MEMORY.md`: la memoria del proyecto.** Se actualiza cuando el usuario toma una decisión, cuando cambia el estado del material, cuando hace una consulta del curso (se anota en “Consultas del usuario” con fecha y archivo de destino) y cuando se abre o se cierra un pendiente. Al empezar una sesión nueva, se lee junto con este archivo.
3. **`README.md`: la presentación del repositorio.** Se actualiza cuando se crea, se mueve o se elimina una carpeta o un tipo de material, o cambia la forma de usarlos.

**Paso a paso de cierre de cada tarea:** primero, revisar qué cambió; segundo, actualizar los tres archivos según corresponda y la documentación del proyecto de agente según la regla 7 de su plan; tercero, si cambió algo en `estudio/`, regenerar el índice con `python -X utf8 estudio/scripts/generar-indice.py` (y, si hay un tema nuevo, agregarlo a la lista `TEMAS` del script); cuarto, comprobar que ninguno de los tres archivos pase de 200 líneas; y quinto, dejar los cambios sin commit hasta que el usuario lo pida.

**Límite de 200 líneas:** `AGENTS.md`, `MEMORY.md` y `README.md` no superan las 200 líneas cada uno; después de cada actualización se revisa su largo (`wc -l`). Si alguno pasa de 200, se poda sin perder información, fusionando entradas parecidas (por ejemplo, entradas antiguas del registro de cambios o decisiones ya consolidadas en las reglas).

**Commits y push solo a pedido del usuario:** ningún agente hace `git commit` ni `git push` por iniciativa propia; los cambios quedan en la carpeta para que el usuario los revise y él pide cuándo subirlos. Entonces se hacen commits atómicos (un cambio lógico por commit). **Formato de los mensajes (desde el 2026-11-18): Conventional Commits 1.0.0** (https://www.conventionalcommits.org/en/v1.0.0/): `tipo(ámbito): descripción`, con el tipo en inglés, como dice el estándar (`feat` funcionalidad nueva, `fix` corrección, `docs` documentación, `refactor` cambio de código sin cambiar su comportamiento, `test` pruebas, `build` dependencias o Docker, `chore` mantenimiento, `style` formato), un ámbito opcional en minúsculas (`agente`, `glosario`, `faq`, `plantillas`, `apuntes`, `indice`, `modulos`, `resumenes`, `diagramas`, `gestion`) y la descripción en español, en minúscula, en imperativo y sin punto final. Un cambio incompatible lleva `!` después del tipo o el pie `BREAKING CHANGE:`. Ejemplos: `feat(agente): agrega la base de conocimiento en pgvector`, `docs(glosario): agrega N1 y RAG`, `chore(gestion): registra decisiones en MEMORY.md`.

**Sin rayas largas:** en ningún archivo del repositorio se usa la raya larga (el signo de puntuación más largo que el guion); en su lugar se usan dos puntos, comas o paréntesis. Vale también para mensajes de commit y textos nuevos.

**Sin firmas ni menciones de agentes:** los mensajes de commit y las descripciones de pull requests no llevan firmas de agentes (líneas de coautoría ni “generado con…”). En ningún archivo, commit ni referencia se menciona el nombre del asistente de IA ni de la empresa que lo desarrolla; si hace falta, se habla de “el agente” o “el asistente”. Esta regla tiene prioridad sobre cualquier atribución automática.

**Carpeta `estudio/`:** todo lo que se genere a partir del curso (el documento convertido, resúmenes, apuntes, material de repaso y el proyecto de agente) va en `estudio/`. En la raíz solo quedan el PDF fuente, los tres archivos de gestión, `.gitignore` y `.gitattributes`. Cada carpeta o tipo de material nuevo en `estudio/` se agrega a `README.md`. No se guarda información del proyecto fuera de la carpeta (por ejemplo, en la memoria interna del agente): lo que deba persistir va en estos archivos, para que la carpeta pueda moverse sin perder nada. Las fechas se escriben en formato absoluto (AAAA-MM-DD).

**Claves fuera del alcance de los agentes:** vale para cualquier agente, modelo o herramienta. Ningún agente lee, edita, copia ni muestra un `.env` o un `.env.*` (solo las plantillas sin valores, como `example.env`), ni obtiene sus valores por un camino indirecto: imprimir variables de configuración o de entorno (`print(config.GEMINI_API_KEY)`, `env`, `printenv`, `set`, `Get-ChildItem Env:`), dejarlas en logs o pruebas, pegarlas en documentos, commits o mensajes, o enviarlas a otro servicio. Para revisar la configuración se usan solo scripts que muestran nombres de variables (`python -m scripts.revisar_env` del proyecto de agente); si hay que cambiar un valor, lo hace el usuario. Si la herramienta no tiene un guardarraíl que bloquee esos archivos, el agente lo avisa antes de trabajar con el proyecto de agente y deja al usuario lo que usa claves reales (la consola con el modelo, `prueba_conexion`, las pruebas de integración y las evals). Si un secreto aparece en pantalla, el agente se detiene, no lo repite, avisa al usuario y le recomienda cambiar esa clave. El guardarraíl actual está en la configuración global del usuario, fuera del repositorio por decisión suya (reglas que niegan leer y editar `.env` y un hook que bloquea toda lectura, búsqueda o comando que lo nombre), y no se desactiva para avanzar más rápido. Hueco conocido: un programa que carga las claves y las imprime no nombra el archivo; por eso esta regla vale por sí misma, y la barrera completa es el sandbox de la herramienta, a cambio de que el usuario ejecute lo que use claves.

## Preguntas del usuario: Preguntas frecuentes y Glosario

Las reglas de esta sección son del usuario: no se eliminan, solo se pueden reformular.

Cuando el usuario pregunta sobre el contenido del curso, se responde en la conversación **y además** se agrega a uno de dos archivos independientes (no al documento del curso):

1. **`estudio/glosario.md`**: consultas por una palabra, sigla o término (p. ej. “¿qué es agent sprawl?”). Encabezado `## <Término>`, entradas **en orden alfabético**.
2. **`estudio/preguntas-frecuentes.md`**: consultas conceptuales o de comprensión (p. ej. “¿cuál es la diferencia entre un chatbot y un agente?”). Encabezado `## <Pregunta>`, en el orden en que el usuario las hace.

**Búsqueda con el índice:** para responder, primero se busca el tema en `estudio/indice.md`, que dice en qué secciones del curso, resúmenes, apuntes, glosario, preguntas frecuentes, plantillas y diagramas aparece, con enlaces.

**Sin redundancia:** antes de agregar una entrada se revisa si ya existe una pregunta o un término parecido en los dos archivos. Si existe, se complementa esa entrada (ajustando su título si hace falta para que cubra ambas), respetando el largo estándar, y se avisa al usuario qué entrada se complementó. Si un término ya está en el Glosario, se amplía su entrada.

**Largo estándar:** el Glosario lleva **entre 80 y 120 palabras, un párrafo**: qué es (sigla completa y traducción), para qué sirve en el curso con un dato o ejemplo, y dónde aparece (módulo y sección principal). Preguntas frecuentes lleva **entre 150 y 250 palabras, dos o tres párrafos**: respuesta directa en una o dos oraciones; de tres a cinco ideas clave, una oración cada una (“Primero…, segundo…”); un ejemplo o cifra del curso; y dónde profundizar. Si una consulta mezcla término y “cómo se hace”, la respuesta va en Preguntas frecuentes y el Glosario lleva una entrada corta que remite a ella.

**Lo del proyecto va en el proyecto:** el Glosario y Preguntas frecuentes son solo para lo aprendido del curso. Una consulta técnica sobre el proyecto de agente (por ejemplo, embeddings, anonimización o librerías) se responde en la conversación y se documenta en `docs/` del proyecto, preferentemente ampliando el documento del tema (o en uno nuevo agregado al mapa `docs/README.md`), con todo lo útil que se mostró (tablas, ejemplos, pruebas y fuentes). El proyecto se basa en el curso y lo cita; el curso no se llena con el proyecto.

Las respuestas siguen las reglas de formato del documento: solo encabezados y párrafos, sin tablas, viñetas ni emojis, con números y símbolos escritos para voz. Lo que no viene del PDF se indica con una frase corta (“esto no viene en el curso”).

## Reglas por tipo de material

### Apuntes visuales impresos

Hojas A4 en `estudio/apuntes/` para repasar en papel, al estilo de apuntes de clase; no son parte del documento que se escucha.

1. **Fuente y generación:** cada módulo es `estudio/apuntes/fuente/apuntes-mN.html`, con hojas `<div class="pag mN">` y estilos comunes en `apuntes.css`. `estudio/apuntes/generar.py` crea `apuntes-modulo-N.pdf` y `apuntes-completos.pdf` y avisa si una hoja se desborda; con `--modulo N --png carpeta` genera un módulo y una imagen por hoja para revisarla.
2. **Poco texto:** palabras clave, frases cortas, diagramas grandes y espacio en blanco; cada hoja entre el 60% y el 90% llena. El usuario pidió que no se vean aplastantes.
3. **Diagramas antes que texto:** cada sección numerada lleva al menos un elemento visual (escalera, ciclo, árbol de decisión, comparación, mapa de conceptos, cifra grande, nota adhesiva). Caveat (manuscrita) para títulos y notas; Inter para el resto.
4. **Contenido:** todas las secciones numeradas, las cifras clave con su fuente y el caso real de cada módulo; se omiten el checklist, las responsabilidades, la reflexión estratégica y las preguntas de validación. Todo dato sale de `estudio/modulos/`.
5. **Siglas y términos en inglés:** cada módulo termina con un recuadro “Siglas y términos en inglés” que explica en una línea cada término usado, avisando que varias explicaciones no vienen en el curso. Junto a un término difícil se puede poner una aclaración corta en gris.
6. **Técnica:** las flechas (`<marker>`) llevan color en hexadecimal e id con prefijo del módulo (`m2-fc`), porque los cinco módulos se unen en un PDF. El CSS propio de un módulo va dentro de `<body>` con selectores que empiezan por `.mN`.

### Diagramas Mermaid a pedido

Cuando el usuario pide un diagrama del curso, se agrega a `estudio/diagramas.md`, en el orden en que lo pide: encabezado `## <Tema>`, una o dos oraciones que dicen qué muestra y de qué módulo y sección sale, y el bloque Mermaid, con etiquetas cortas en español. Todo dato sale de `estudio/modulos/`; lo que no venga del curso se marca. Antes de agregarlo se valida la sintaxis (por ejemplo, comillas en etiquetas con paréntesis, dos puntos o acentos problemáticos). Los diagramas para construir el proyecto de agente van en su `docs/` (ver “Proyecto de agente”).

### Plantillas de gestión

`estudio/plantillas/` tiene 15 plantillas numeradas por fase del ciclo de vida (decidir, diseñar y activar, integrar al equipo, supervisar y gobernar, demostrar valor y escalar) y la guía `00-guia.md`. Toda plantilla mantiene la misma estructura: un bloque inicial (para qué sirve, cuándo llenarla, quién la llena y la aprueba, con qué se llena, base en el curso, se conecta con), “Cómo llenarla”, “Plantilla”, “Ejemplo lleno” y “Errores comunes”. Los campos salen del curso; lo agregado se marca “(no viene en el curso)” y los datos inventados, “datos ficticios de ejemplo”. Los ejemplos usan como hilo conductor el “Agente de Soporte N1” (soporte B2B de la sección 2.5), con personas ficticias. Cada sigla en inglés se explica la primera vez que aparece en cada plantilla. Se mantienen los términos del curso (por ejemplo, “taxonomía de tareas”) aunque suenen técnicos.

### Resúmenes por módulo

`estudio/resumenes/resumen-modulo-N.md`: un resumen por módulo para repasar en pocos minutos. Un título y solo párrafos cortos (sin subtítulos, listas ni tablas), entre 450 y 800 palabras, con números escritos para la voz y términos en inglés explicados. Todo sale del módulo; nada se inventa. Cada resumen pasa dos validaciones de agentes distintos del que lo escribió: la primera busca alucinaciones y omisiones importantes; la segunda revisa de nuevo todo el texto corregido.

### Índice cruzado

`estudio/indice.md` conecta todo el material: lista de archivos, mapa por módulo (qué entradas, plantillas y diagramas cita cada sección) y temas de la A a la Z con enlaces a la sección exacta. No se edita a mano: lo genera `estudio/scripts/generar-indice.py`, que lee rutas fijas (`modulos/`, `resumenes/`, `plantillas/`, `apuntes/fuente/`, `glosario.md`, `preguntas-frecuentes.md` y `diagramas.md`) y los `docs/*.md` del proyecto de agente; un archivo en otra carpeta nueva requiere agregarlo al script. Los scripts de mantenimiento van en `estudio/scripts/`, salvo el generador de los apuntes. Es la única excepción a la regla de no usar listas ni tablas.

## Proyecto de agente

El proyecto está en `estudio/proyecto-agente/agente-soporte-n1/`. Su plan, `docs/plan-del-proyecto.md`, manda sobre el resto de su documentación y tiene sus reglas de desarrollo, entre ellas la documentación que se actualiza con cada cambio (regla 7); el mapa de documentos es `docs/README.md`. Aquí solo quedan las reglas generales: el código (en `src/`) no sigue las reglas de formato para voz; los diagramas para construirlo van en su `docs/`, no en `estudio/diagramas.md`; y toda librería o imagen del proyecto debe tener licencia MIT, BSD, Apache 2.0 o similar, sin GPL, LGPL, AGPL ni SSPL (regla muy importante del usuario; las excepciones aceptadas están en la sección “Licencias” del plan).

## Revisiones de calidad con elephant-goldfish-model (EGM)

El usuario instaló elephant-goldfish-model (EGM) para mejorar la calidad del repositorio. Antes de cerrar un cambio importante (un plan, una etapa del proyecto, una reorganización de documentos), se pide una revisión de solo lectura con sus agentes (`egm:*`, coordinados por `egm:egm-synthesizer`) y, cuando el contenido cita el curso, un verificador independiente de fidelidad contra `estudio/modulos/`. Los hallazgos se comprueban antes de aplicarlos (un revisor puede equivocarse), el informe se guarda con fecha en `docs/revisiones/` del proyecto, y no se aplica ningún cambio sin la decisión del usuario.

## Conversión del curso (terminada)

**Mapa de páginas:** se omiten la portada (página 1) y el cierre de Certiprof (93 a 97). Módulo 1, páginas 2 a 19: “El Nuevo Rol del Manager: De Supervisar Personas a Orquestar Agentes”. Módulo 2, 20 a 40: “Diseñar y Activar Agentes: El Arte del Onboarding Agentic”. Módulo 3, 41 a 59: “Supervisión, Auditoría y Performance del Agente”. Módulo 4, 60 a 75: “Rediseño de Procesos: Equipos Híbridos Humanos + Agentes”. Módulo 5, 76 a 92: “Impacto al Negocio: Medir, Comunicar y Escalar Resultados”.

**Cómo se hizo y cómo regenerar:** un agente por módulo leyó el texto y la imagen de cada página, verificó cada cifra, fuente y concepto e informó los casos nuevos, que se volvieron reglas; después hubo una auditoría por módulo contra el PDF. Para volver al PDF página por página, se regenera en una carpeta temporal con Python: el texto con `pypdf` (`PdfReader(...).pages[i].extract_text()`) y las imágenes con `pypdfium2` (`page.render(scale=1.4).to_pil().save(...)`); la imagen aclara cards, tablas y columnas cuando el texto sale desordenado.

### Reglas de contenido

1. **No perder nada.** Todo concepto, definición, cifra, porcentaje, fuente citada (autor, institución, año), ejemplo, caso real y advertencia aparece en el resultado. Ante la duda, se incluye.
2. **Página por página, en orden.** El texto que continúa de una página a la siguiente se une en un solo párrafo.
3. **Se eliminan cabeceras y pies:** logo o “certiprof”, `www.certiprof.com`, número de página, “CERTIPROF® is a registered trademark…”, “AIAM™ VERSIÓN 052026”.
4. **Se eliminan “Duración estimada” y “Nivel”** de cada módulo; los objetivos de aprendizaje y el resto se conservan.
5. **Tablas a párrafos:** cada fila se vuelve una o varias oraciones que nombran lo que dicen las columnas (“La primera competencia es la Dirección Estratégica, que en la práctica implica…”). El título de la tabla introduce el párrafo. Nunca se omite una fila ni una celda.
6. **Cards, recuadros, cifras destacadas, citas y cajas “¿Qué dice la investigación?” a párrafos:** una cifra destacada se redacta como oración (“La demanda del skill cluster Agentic AI creció un 280% en un solo año…”); se conservan la fuente y el título de la card cuando aportan contexto (“Según Harvard Business Review, en el artículo de Srinivasan y Wei de febrero de 2026…”).
7. **Listas y viñetas a párrafos:** oraciones encadenadas (“En primer lugar…, en segundo lugar…”) o una enumeración dentro de una oración.
8. **Checklists de autoevaluación** a un párrafo que enumera todas las capacidades (“Al terminar este módulo, usted debería ser capaz de…”), sin perder ningún ítem.
9. **Casos reales, Reflexión Estratégica y Responsabilidades del AIAM™** se conservan como subsecciones en prosa.
10. **Preguntas de validación:** el enunciado completo (escenario y pregunta), “Respuesta correcta:” con el texto completo de la alternativa correcta (sin la letra) y “Por qué:” con su justificación, íntegra si no se refiere a las otras alternativas. Se eliminan las alternativas incorrectas y los comentarios sobre ellas (salvo lo que rescata la regla adicional 18).
11. **No inventar ni resumir.** Se reformula la sintaxis para pasar a prosa, pero no se agrega ni se condensa contenido. La prosa del PDF se copia fiel, corrigiendo solo cortes de extracción (“tal ento” a “talento”, guiones de corte, espacios sobrantes).
12. **Emojis y símbolos decorativos** (💡, ⏱, 🎯, ❌, ✓, ☐, 📋, flechas en cifras) se eliminan o se dicen con palabras (“2024→2025” a “de 2024 a 2025”). Las siglas y marcas (AIAM™, HBR, CSAT, NPS, ROI…) se conservan.

### Reglas de formato

1. `#` para el título general, `##` para cada módulo (“## Módulo 1. El Nuevo Rol del Manager…”), `###` para cada sección numerada (“### 1.2 Agentes de IA, Chatbots y Automatización…”) y `####` para subsecciones.
2. Mismo orden y numeración de secciones que el PDF.
3. Sin tablas Markdown, viñetas, listas numeradas, bloques de cita (`>`) ni negritas decorativas excesivas: solo encabezados y párrafos, separados por una línea en blanco, en UTF-8 con tildes correctas.
4. **Títulos exactos del PDF:** “Reflexión Estratégica” sin “Final” si así aparece; “1.6 Checklist de Competencias, Módulo 1” va numerado como `###`; “Lista de Competencias del Módulo 4” va como `###` aunque no tenga número.
5. **Jerarquía fija:** las secciones sin número que cuelgan del módulo (Objetivo de aprendizaje al inicio, Responsabilidades, Checklist o Lista de Competencias, Reflexión Estratégica, Preguntas de validación) van como `###`; “Preguntas de validación” se escribe igual en los cinco módulos. Las cards o recuadros con título propio (Regla práctica, ¿Qué dice la investigación?, Caso X, y “Lo que este programa te ha dado” antes de las secciones finales) van como `####`. Cada pregunta va como `#### Pregunta N`.

### Reglas adicionales

1. **Navegación entre módulos** (“Módulo 2 Completado. Continúe al Módulo 3…”) se elimina.
2. **“Por qué” sin letras:** se elimina toda mención a letras de alternativas (“C es correcto porque…”). La frase lleva sujeto explícito, nunca un verbo suelto: “Esta respuesta aplica…”, o “Esta conducta es…” cuando la pregunta pide lo que debe evitarse. Se conservan las frases de razonamiento que no nombran letras (“No hay que retroceder al Nivel 1 ni saltar al Nivel 3…”).
3. **Erratas evidentes del PDF** se corrigen (“el enemy número uno” a “el enemigo número uno”). Los términos técnicos en inglés usados a propósito (agent sprawl, guardrails, onboarding…) se mantienen.
4. **Formato numérico español, en todo el documento:** decimales con coma (“2,3 millones”, “4,4”) y miles con punto (“55.000 rutas”); “$40M” a “40 millones de dólares”; “$4.4T” a “4,4 billones de dólares”; “40%+” a “más del 40%”; “≥80%” a “mayor o igual al 80%”; “4.2/5” a “4,2 sobre 5”; “(a) (b) (c)” o “(1) (2) (3)” a “primero, segundo, tercero”.
5. **Rangos y fórmulas:** “12-24 meses” a “de 12 a 24 meses”; “18+ meses” a “más de 18 meses”; “(Beneficio – Inversión) / Inversión” a “el beneficio menos la inversión, dividido por la inversión”.
6. **Símbolos para voz:** “±2 semanas” a “más o menos 2 semanas”; “3+ días” a “3 o más días”; “5-10%” a “entre el 5% y el 10%”; “tokens/min” a “tokens por minuto”; “verde/amarillo/rojo” a “verde, amarillo o rojo”; “1-a-1” y “1:1” a “1 a 1”; “vs.” a “frente a”; “+” entre instituciones o conceptos (“MIT SMR + BCG”) a “y” o “más”; “24/7” a “las 24 horas, los 7 días de la semana”; las rayas que separan incisos, o con que empieza una respuesta, a comas o dos puntos.
7. **Tablas comparativas de dos columnas** (antes y después, humano y agente): un párrafo por fila contrastando ambas columnas, o dos bloques paralelos con todos los ítems en orden. Si no tienen título, el `####` se construye con los encabezados (“Organización sin… frente a organización con…”).
8. **Celdas “N/A”** se explican en prosa (“aquí no aplica dejar correr, porque…”); la fila no se omite.
9. **Checklists en tercera persona formal:** cada ítem en primera persona (“Puedo…”, “Entiendo…”) pasa a infinitivo dentro de “usted debería ser capaz de…”, y “mi” pasa a “su”.
10. **Cards de caso:** “Industria” y “Resultado medible” van a un párrafo introductorio; “Lección para el AI Agent Manager” a “La lección para el AI Agent Manager es la siguiente: …”.
11. **Cards de pares de ejemplo** (lenguaje técnico frente a directivo): un `####` con un párrafo por par (“En lenguaje técnico: … Traducido al lenguaje directivo: …”).
12. **Referencias académicas destacadas:** `#### Referencia académica N`, con la fuente en prosa (autor, año, título, editorial) y la cita textual entre comillas.
13. **Cards de tipos** (por ejemplo, tipos de error): un `####` por tipo, con párrafos que empiezan por “Qué son:”, “Ejemplo:” y “Señal de detección:”.
14. **Responsabilidades numeradas (01, 02…)** a “La primera responsabilidad es…”, un párrafo por responsabilidad.
15. **Encabezado de las preguntas de validación:** se conserva la descripción (“Diez preguntas de práctica basadas en rol”) y se elimina “Seleccione la opción que mejor aplique”.
16. Una cifra que solo aparece en una alternativa incorrecta se pierde legítimamente con ella.
17. **Enunciados que terminan en “…es:”** se reformulan como pregunta directa.
18. **Conceptos en comentarios sobre alternativas incorrectas (prioridad sobre la regla adicional 2):** si el comentario enseña un concepto, criterio o dato (“el problema real es el criterio de evaluación, no el volumen de datos”; “todos los niveles requieren gestión”) o descalifica por un motivo con contenido (“es un argumento operativo, no estratégico”, “confunde la eficiencia con la transformación”), se conserva en el “Por qué” como afirmación general, sin nombrar la letra ni describir la alternativa. Solo se elimina la etiqueta sin criterio (“es irrelevante”, “es negligencia”).
19. **Fidelidad de cifras:** si el PDF da cifras distintas para el mismo dato en lugares distintos (McKinsey 4,4 billones en una card y “2,6 a 4,4 billones” en una pregunta), se conservan ambas donde aparecen.
20. **No se agregan glosas** que no están en el PDF (“4.4 trillion, en la notación anglosajona”).
21. **Oraciones completas en inglés** dentro de la prosa en español se traducen fielmente; los términos técnicos en inglés se mantienen.

## Registro de cambios

El detalle de cada cambio está en git y en `MEMORY.md`.

- 2026-11-17: Conversión completa del curso con sus reglas (a partir de los informes de los agentes y de una auditoría por módulo contra el PDF), separada después en cinco archivos por módulo; PDF renombrado y carpeta `estudio/`; archivos de gestión con su mantenimiento y el límite de 200 líneas; Glosario y Preguntas frecuentes con largo estándar y sin redundancia; reglas de git (sin firmas ni menciones, commits a pedido); apuntes, diagramas Mermaid, plantillas y resúmenes.
- 2026-11-18: Índice cruzado generado por script; proyecto de agente con su plan, sus reglas y su documentación actualizada con cada cambio; revisiones con EGM; Conventional Commits; sin rayas largas; lo del proyecto se documenta en el proyecto.
- 2026-11-19: Agente y scripts de asistencia separados (D10); lecciones aprendidas del proyecto; regla “Claves fuera del alcance de los agentes”, con guardarraíl en la configuración global de la herramienta; simplificación aprobada por el usuario: este archivo se reordena, las reglas del proyecto pasan a su plan y las de la conversión se compactan (informe en `docs/revisiones/` del proyecto).
