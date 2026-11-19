# Agente de Soporte N1

Código del agente de soporte técnico del curso AI Agent Manager (sección 2.5). Para entender el recorrido completo en simple, lea primero “El flujo completo, en simple” en `docs/plan-del-proyecto.md`. El porqué de las decisiones técnicas está en `docs/decisiones.md`, y qué archivo llama a cuál, en `docs/diagramas-del-codigo.md`. Las reglas de desarrollo, las etapas, el modelo de datos y lo que se posterga están en `docs/plan-del-proyecto.md`. El mapa de toda la documentación está en `docs/README.md`.

## Estado

Etapas 0 y 1 listas y probadas: conexión con el modelo y conversación en la terminal con el system prompt JD+SOP. Etapa 2 lista y probada: la base de conocimiento en pgvector (el RAG), con 8 documentos cortados por secciones. Etapa 3 lista y probada: el agente usa sus tres herramientas, responde con soluciones documentadas citando la fuente o escala con el contexto completo, con topes de tokens y de llamadas; hay pruebas unitarias y de integración. Las carpetas vacías tienen un `README.md` que dice qué irá en ellas y en qué etapa.

## Cómo probarlo

Todos los comandos se escriben en PowerShell, desde esta carpeta (`agente-soporte-n1`).

1. Cree el `.env` a partir de la plantilla y complete `GEMINI_API_KEY` (clave de Google AI Studio). `LLM_PROVEEDOR` ya trae `gemini` y `LLM_MODEL`, `gemini-3.1-flash-lite` (decisión D5); para usar OpenRouter u Ollama, ver `docs/proveedores-de-modelos.md`. Si `example.env` cambia más adelante, `start-dev.bat` avisa y `python -m scripts.revisar_env --ordenar` (desde `src\backend`) pone su `.env` al día sin perder valores. Desde la etapa 2, complete también `POSTGRES_PASSWORD` con una contraseña inventada:

    ```powershell
    Copy-Item src\docker\example.env src\docker\.env
    notepad src\docker\.env
    ```

2. Ejecute `start-dev.bat` (doble clic, o `.\start-dev.bat`): crea el entorno virtual la primera vez, instala las librerías, levanta los servicios de Docker (desde la etapa 2) y abre la consola del agente. `start-qa.bat` levanta todo en Docker, incluida la app; funciona desde la etapa 6 y, antes, avisa que todavía no está disponible. `clear.bat` libera espacio: borra el entorno virtual, las librerías descargadas y las cachés y detiene y borra los contenedores de Docker. Conserva las imágenes descargadas y los datos de la base; para borrar también los datos, ejecute `.\clear.bat --borrar-volumenes`, que pide confirmación. Nunca toca el código ni el `.env`.
3. Etapa 0, solo la prueba de conexión (con el entorno virtual ya creado por `start-dev.bat`). Los scripts de asistencia se ejecutan desde `src\backend` con `python -m` (ver `src/backend/scripts/README.md`):

    ```powershell
    cd src\backend
    .\.venv\Scripts\python.exe -m scripts.prueba_conexion
    ```

4. Etapa 2, la base de conocimiento (necesaria para conversar con el agente). Necesita Docker Desktop abierto. `start-dev.bat` levanta PostgreSQL; luego, en otra terminal:

    ```powershell
    cd src\backend
    .\.venv\Scripts\python.exe -m scripts.cargar_conocimiento
    .\.venv\Scripts\python.exe -m scripts.probar_busqueda
    .\.venv\Scripts\python.exe -m scripts.probar_busqueda "mi factura sale cortada"
    ```

    El primero carga los 8 documentos; el segundo prueba una lista de consultas y dice cuántas encontraron el documento esperado; el tercero busca lo que usted escriba.

5. Conversar con el agente (etapa 3): lo abre `start-dev.bat`, o, desde `src\backend`, `.\.venv\Scripts\python.exe -m aplicacion.consola`. Necesita la base de conocimiento cargada (paso 4, una sola vez, y de nuevo cuando cambian los documentos o se borran los volúmenes); si falta, la consola avisa. Pide el código del cliente (C-001 a C-006) y crea un ticket con el primer mensaje. Pruebe "olvidé mi contraseña": debe responder con los pasos del documento y terminar con "Fuente: restablecer-contrasena.md > Pasos". Ante "quiero cancelar mi cuenta" debe escalar: el ticket pasa a una persona y la consola empieza un ticket nuevo. Con `--detallado` muestra cada paso del agente: herramientas, fragmentos con su parecido, tokens, costo y segundos.

6. Estimar costos, sin llamar al modelo (gratis), desde `src\backend`: `.\.venv\Scripts\python.exe -m scripts.estimar_costos`. Con `--documentos 1000 --caracteres 20000` estima una carga hipotética, y con `--consultas 50 300 1000` sus escenarios de consultas al día. Explicación y supuestos en `docs/costos.md`. Si ya hay tickets atendidos, usa su costo real promedio.

7. Pruebas automáticas, gratis y sin llamar al modelo, desde `src\backend` y con PostgreSQL levantado: `.\.venv\Scripts\python.exe -m pytest tests/unitarias tests/integracion`. Las de integración usan la base de desarrollo y deshacen todo lo que escriben. Detalle en `src/backend/tests/README.md`.

**Si el entorno virtual no se deja borrar** (`clear.bat` avisa que algunos archivos no se pudieron borrar, o `start-dev.bat` falla al crear el entorno): a veces Windows deja archivos de `src\backend\.venv` con permisos que ni el propio usuario puede leer. Solución rápida: renombrar la carpeta (`Rename-Item src\backend\.venv .venv-bloqueado`) y volver a ejecutar `start-dev.bat`, que crea un entorno nuevo. Para borrar la carpeta vieja, en una PowerShell abierta como administrador y desde esta carpeta:

    ```powershell
    takeown /f src\backend\.venv-bloqueado /r /d s
    icacls src\backend\.venv-bloqueado /grant "$($env:USERNAME):F" /t /c
    Remove-Item src\backend\.venv-bloqueado -Recurse -Force
    ```

    `takeown` toma la propiedad de los archivos, `icacls` le da permiso completo a su usuario y `Remove-Item` borra la carpeta. Git ignora cualquier carpeta `.venv*`, así que nunca se sube.

En PowerShell, un programa de una carpeta relativa se ejecuta empezando con `.\`; sin eso, PowerShell interpreta `.venv` como el nombre de un módulo y da el error “No se pudo cargar el módulo”.

## Estructura

| Carpeta | Contenido | Etapa |
|---|---|---|
| `src/backend/aplicacion/` | el agente en sí: configuración, modelo, base de datos, prompt, consola y, más adelante, la API FastAPI; es lo que entra en la imagen Docker | 0 en adelante |
| `src/backend/scripts/` | scripts de asistencia que se ejecutan sueltos (prueba de conexión, carga del conocimiento, prueba de búsqueda, costos); usan la aplicación, pero la aplicación nunca los usa (decisión D10) | 0 en adelante |
| `src/backend/tests/` | cinco tipos de pruebas, cada uno en su carpeta: unitarias, de integración, adversariales, evals del modelo y e2e | 3 en adelante (unitarias e integración); 5 y 6 (las demás) |
| `src/base-de-conocimiento/` | documentos de soporte ficticios que se cargan a pgvector | 2 |
| `src/frontend/src/` | páginas HTML, JavaScript y CSS: tickets, cola de escalaciones, revisión por muestreo y dashboard | 7 |
| `src/docker/` | `docker-compose.yml`, `.env`, `example.env` y scripts de PostgreSQL | 0 (`example.env`) y 2 |
