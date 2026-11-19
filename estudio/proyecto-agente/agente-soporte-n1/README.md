# Agente de Soporte N1

Un agente de soporte técnico de primera línea (N1) para Nubesoft, una empresa ficticia, construido a escala pequeña para entender en la práctica el curso AI Agent Manager (sección 2.5): cómo se define, se gobierna, se supervisa y se mide un agente. Empiece por el mapa de la documentación, `docs/README.md`; el estado de cada etapa está en `docs/plan-del-proyecto.md`.

## Cómo probarlo

Todos los comandos se escriben en PowerShell, desde esta carpeta (`agente-soporte-n1`), salvo los que dicen “desde `src\backend`”. Los programas de Python se ejecutan siempre desde `src\backend`, con el entorno virtual: `.\.venv\Scripts\python.exe -m <módulo>`.

1. Cree el archivo de configuración a partir de la plantilla y complete `GEMINI_API_KEY` (clave de Google AI Studio) y `POSTGRES_PASSWORD` (una contraseña inventada). `LLM_PROVEEDOR` ya trae `gemini` y `LLM_MODEL`, `gemini-3.1-flash-lite` (D5); para usar OpenRouter u Ollama, ver `docs/modelos-y-costos.md`.

    ```powershell
    Copy-Item src\docker\example.env src\docker\.env
    notepad src\docker\.env
    ```

2. Ejecute `.\start-dev.bat` (o doble clic). Ver “Los scripts de arranque y limpieza”.
3. Cargue la base de conocimiento, una sola vez y de nuevo cuando cambien los documentos o se borren los volúmenes. Necesita Docker Desktop abierto y PostgreSQL levantado por `start-dev.bat`; en otra terminal, desde `src\backend`:

    ```powershell
    .\.venv\Scripts\python.exe -m scripts.cargar_conocimiento
    .\.venv\Scripts\python.exe -m scripts.probar_busqueda
    .\.venv\Scripts\python.exe -m scripts.probar_busqueda "mi factura sale cortada"
    ```

    El primero carga los documentos; el segundo prueba una lista de consultas y dice cuántas encontraron el documento esperado; el tercero busca lo que usted escriba.

4. Converse con el agente: lo abre `start-dev.bat`, o, desde `src\backend`, `.\.venv\Scripts\python.exe -m aplicacion.consola`. Pide el código del cliente (C-001 a C-006) y crea un ticket con el primer mensaje. Pruebe “olvidé mi contraseña”: debe responder con los pasos del documento y terminar con “Fuente: restablecer-contrasena.md > Pasos”. Ante “quiero cancelar mi cuenta” debe escalar: el ticket pasa a una persona y la consola empieza un ticket nuevo. Con `--detallado` muestra cada paso del agente: herramientas, fragmentos con su parecido, tokens, costo y segundos. Desde la etapa 4, el kill switch se activa con `-m aplicacion.consola --detener "motivo"` y se desactiva con `--reactivar "motivo"`; mientras el agente está detenido, los tickets pasan a una persona.
5. Otros programas, desde `src\backend` (todos en `src/backend/scripts/README.md`): `scripts.prueba_conexion` prueba el modelo de chat y el de embeddings; `scripts.estimar_costos` estima el gasto sin llamar al modelo (`docs/modelos-y-costos.md`); `scripts.revisar_env --ordenar` pone el archivo de configuración al día con la plantilla, sin perder valores (D14).
6. Pruebas automáticas, gratis y sin llamar al modelo, desde `src\backend` y con PostgreSQL levantado: `.\.venv\Scripts\python.exe -m pytest tests/unitarias tests/integracion`. Las de integración usan la base de desarrollo y deshacen todo lo que escriben (`docs/estrategia-de-pruebas.md`).

## Los scripts de arranque y limpieza

Esta es la única descripción de los `.bat`; el plan los nombra en la regla 11.

- **`start-dev.bat`** (desarrollo): la primera vez crea el entorno virtual (`src\backend\.venv`) e instala las librerías; avisa si el archivo de configuración no existe o se separó de la plantilla; levanta PostgreSQL con Docker Compose, espera a que esté listo y abre la consola del agente. La app corre en local.
- **`start-qa.bat`** (qa): levanta todo en Docker Compose, incluida la app (el servicio del backend lleva el perfil `qa`; sin perfil, Compose levanta solo PostgreSQL). Funciona desde la etapa 6; antes, avisa que todavía no está disponible.
- **`clear.bat`** (limpieza): borra el entorno virtual con sus librerías y las cachés de Python y de `pytest`, y detiene y borra los contenedores que levantó Docker Compose. Nunca borra las imágenes descargadas, como la de PostgreSQL, para que volver a empezar sea rápido, y conserva los volúmenes (los datos de la base), salvo con `.\clear.bat --borrar-volumenes`, que además pide confirmación. Nunca toca el código, los documentos ni el archivo de configuración.

## Estructura

| Carpeta | Contenido | Etapa |
|---|---|---|
| `src/backend/aplicacion/` | el agente en sí: configuración, modelo, base de datos, prompt, herramientas, bucle del agente, consola y, más adelante, la API FastAPI; es lo que entra en la imagen Docker | 0 en adelante |
| `src/backend/scripts/` | scripts de asistencia que se ejecutan sueltos; usan la aplicación, pero la aplicación nunca los usa (D10) | 0 en adelante |
| `src/backend/tests/` | cinco tipos de pruebas, cada uno en su carpeta; las carpetas vacías tienen un `README.md` que dice qué irá en ellas | 3 en adelante |
| `src/base-de-conocimiento/` | documentos de soporte ficticios que se cargan a pgvector | 2 |
| `src/frontend/src/` | páginas HTML, JavaScript y CSS: tickets, cola de escalaciones, revisión por muestreo y dashboard | 7 |
| `src/docker/` | `docker-compose.yml`, la plantilla `example.env`, el archivo de configuración local y los scripts de PostgreSQL | 0 y 2 |
| `docs/` | la documentación; empiece por `docs/README.md` | todas |

## Si algo falla

**PowerShell dice “No se pudo cargar el módulo”:** un programa de una carpeta relativa se ejecuta empezando con `.\`; sin eso, PowerShell interpreta `.venv` como el nombre de un módulo.

**El entorno virtual no se deja borrar** (`clear.bat` avisa que algunos archivos no se pudieron borrar, o `start-dev.bat` falla al crear el entorno): a veces Windows, el editor o el antivirus dejan archivos de `src\backend\.venv` con permisos que ni el propio usuario puede leer. Solución rápida: renombrar la carpeta (`Rename-Item src\backend\.venv .venv-bloqueado`) y volver a ejecutar `start-dev.bat`, que crea un entorno nuevo. Para borrar la carpeta vieja, en una PowerShell abierta como administrador y desde esta carpeta:

```powershell
takeown /f src\backend\.venv-bloqueado /r /d s
icacls src\backend\.venv-bloqueado /grant "$($env:USERNAME):F" /t /c
Remove-Item src\backend\.venv-bloqueado -Recurse -Force
```

`takeown` toma la propiedad de los archivos, `icacls` le da permiso completo a su usuario y `Remove-Item` borra la carpeta. Git ignora cualquier carpeta `.venv*`, así que nunca se sube.

**La consola avisa que falta la base de conocimiento:** ejecute el paso 3. **Un proveedor rechaza el pedido o tarda mucho:** ver `docs/modelos-y-costos.md`.
