@echo off
rem Entorno de desarrollo (dev) del Agente de Soporte N1.
rem La app corre en local, con un entorno virtual de Python; el resto de los
rem servicios (PostgreSQL, desde la etapa 2) se levanta con Docker Compose.
rem Uso: doble clic, o "start-dev.bat" desde esta carpeta. Aparece en la etapa 0.
setlocal
cd /d "%~dp0src\backend"

rem 0. El .env con las claves debe existir antes de empezar.
if not exist ..\docker\.env (
    echo Falta src\docker\.env: copie src\docker\example.env como .env y complete sus valores.
    pause
    exit /b 1
)

rem 1. Entorno virtual de Python: se crea la primera vez, en src\backend\.venv.
rem    Se revisa el propio python.exe y no solo la carpeta: si una limpieza quedo a medias,
rem    la carpeta puede existir sin el entorno, y aqui se vuelve a crear.
if not exist .venv\Scripts\python.exe (
    echo Creando el entorno virtual de Python...
    python -m venv .venv || goto :error
)
call .venv\Scripts\activate.bat
python -m pip install -q -r requirements.txt || goto :error
rem    Avisa si el .env se separo de la plantilla example.env (decision D14); no detiene nada.
python -m scripts.revisar_env

rem 2. Servicios de apoyo con Docker Compose (desde la etapa 2).
rem    Sin perfil, Compose levanta solo PostgreSQL; la app no, porque corre en local.
docker compose -f ..\docker\docker-compose.yml up -d --wait || goto :error

rem 3. La app: la consola del agente. Se mantiene en todas las etapas (regla 12 del plan);
rem    desde la etapa 6 este script tambien levantara la API con uvicorn.
python -m aplicacion.consola
goto :eof

:error
echo.
echo Algo fallo. Revise el mensaje de arriba.
echo Si el error menciona Docker, abra Docker Desktop, espere a que diga que esta corriendo y vuelva a intentar.
echo Si el error menciona .venv, otro programa (el editor o el antivirus) puede estar usando
echo el entorno virtual: cierre el editor, ejecute clear.bat y vuelva a ejecutar start-dev.bat.
pause
exit /b 1
