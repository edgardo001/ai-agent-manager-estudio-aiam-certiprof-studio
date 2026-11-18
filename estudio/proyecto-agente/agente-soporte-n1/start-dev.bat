@echo off
rem Entorno de desarrollo (dev) del Agente de Soporte N1.
rem La app corre en local, con un entorno virtual de Python; el resto de los
rem servicios (PostgreSQL, desde la etapa 2) se levanta con Docker Compose.
rem Uso: doble clic, o "start-dev.bat" desde esta carpeta. Aparece en la etapa 0.
setlocal
cd /d "%~dp0src\backend"

rem 1. Entorno virtual de Python: se crea la primera vez, en src\backend\.venv
if not exist .venv (
    echo Creando el entorno virtual de Python...
    python -m venv .venv || goto :error
)
call .venv\Scripts\activate.bat
python -m pip install -q -r requirements.txt || goto :error

rem 2. Servicios de apoyo con Docker Compose (existe desde la etapa 2).
rem    Sin perfil, Compose levanta solo PostgreSQL; la app no, porque corre en local.
if exist ..\docker\docker-compose.yml (
    docker compose -f ..\docker\docker-compose.yml up -d || goto :error
)

rem 3. La app: la consola del agente. Se mantiene en todas las etapas (regla 12 del plan);
rem    desde la etapa 6 este script tambien levantara la API con uvicorn.
python src\consola.py
goto :eof

:error
echo.
echo Algo fallo. Revise el mensaje de arriba.
pause
exit /b 1
