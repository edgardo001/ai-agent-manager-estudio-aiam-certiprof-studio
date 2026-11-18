# Agente de Soporte N1

Código del agente de soporte técnico del curso AI Agent Manager (sección 2.5). Para entender el recorrido completo en simple, lea primero “El flujo completo, en simple” en `docs/plan-del-proyecto.md`. El porqué de las decisiones técnicas está en `docs/decisiones.md`, y qué archivo llama a cuál, en `docs/diagramas-del-codigo.md`. Las reglas de desarrollo, las etapas, el modelo de datos y lo que se posterga están en `docs/plan-del-proyecto.md`. El mapa de toda la documentación está en `docs/README.md`.

## Estado

Etapas 0 y 1 listas: conexión con el modelo y conversación en la terminal con el system prompt JD+SOP. Las carpetas vacías tienen un `README.md` que dice qué irá en ellas y en qué etapa.

## Cómo probarlo

Todos los comandos se escriben en PowerShell, desde esta carpeta (`agente-soporte-n1`).

1. Cree el `.env` a partir de la plantilla y complete `LLM_API_KEY` (clave de Google AI Studio). `LLM_MODEL` ya trae `gemini-3.1-flash-lite` (decisión D5). Desde la etapa 2, complete también `POSTGRES_PASSWORD` con una contraseña inventada:

    ```powershell
    Copy-Item src\docker\example.env src\docker\.env
    notepad src\docker\.env
    ```

2. Ejecute `start-dev.bat` (doble clic, o `.\start-dev.bat`): crea el entorno virtual la primera vez, instala las librerías, levanta los servicios de Docker (desde la etapa 2) y abre la consola del agente. `start-qa.bat` levanta todo en Docker, incluida la app; funciona desde la etapa 6 y, antes, avisa que todavía no está disponible. `clear.bat` libera espacio: borra el entorno virtual, las librerías descargadas y las cachés y, si usted lo confirma, lo del proyecto en Docker, incluidos los datos de la base; nunca toca el código ni el `.env`.
3. Etapa 0, solo la prueba de conexión (con el entorno virtual ya creado por `start-dev.bat`):

    ```powershell
    .\src\backend\.venv\Scripts\python.exe .\src\backend\src\prueba_conexion.py
    ```

4. Etapa 1, conversar con el agente: lo abre `start-dev.bat`, o `.\src\backend\.venv\Scripts\python.exe .\src\backend\src\consola.py`. Pruebe "quiero cancelar mi cuenta": debe decir que una persona seguirá con su caso. Ante "olvidé mi contraseña" la respuesta puede variar, porque en esta etapa el agente todavía no tiene herramientas ni documentos; eso llega en las etapas 2 y 3.

En PowerShell, un programa de una carpeta relativa se ejecuta empezando con `.\`; sin eso, PowerShell interpreta `.venv` como el nombre de un módulo y da el error “No se pudo cargar el módulo”.

## Estructura

| Carpeta | Contenido | Etapa |
|---|---|---|
| `src/backend/src/` | código Python del agente y, más adelante, la API FastAPI | 0 en adelante |
| `src/backend/tests/` | pruebas en tres grupos: reglas en código, las 5 dimensiones de validación de la sección 2.6 y métricas | 5 |
| `src/base-de-conocimiento/` | documentos de soporte ficticios que se cargan a pgvector | 2 |
| `src/frontend/src/` | páginas HTML, JavaScript y CSS: tickets, cola de escalaciones, revisión por muestreo y dashboard | 7 |
| `src/docker/` | `docker-compose.yml`, `.env`, `example.env` y scripts de PostgreSQL | 0 (`example.env`) y 2 |
