@echo off
rem Limpieza del Agente de Soporte N1: libera espacio en el equipo.
rem Borra lo que se descarga o se genera solo, y se vuelve a crear con start-dev.bat
rem o start-qa.bat. Nunca borra el codigo, los documentos ni src\docker\.env (sus claves).
rem Uso: doble clic, o "clear.bat" desde esta carpeta. Para borrar tambien los datos de la
rem base: "clear.bat --borrar-volumenes". Aparece en la etapa 0.
setlocal
cd /d "%~dp0"

rem 1. Entorno virtual de Python, con todas las librerias descargadas
if exist src\backend\.venv (
    echo Borrando el entorno virtual src\backend\.venv...
    rmdir /s /q src\backend\.venv
)
if exist src\backend\.venv (
    echo.
    echo Aviso: algunos archivos de src\backend\.venv no se pudieron borrar porque otro programa
    echo los esta usando, por ejemplo el editor de codigo o el antivirus. Cierre el editor y vuelva
    echo a ejecutar clear.bat. No afecta al proyecto: start-dev.bat recrea el entorno igual.
    echo.
)

rem 2. Carpetas de cache de Python y de pytest
for /d /r src %%d in (__pycache__ .pytest_cache) do (
    if exist "%%d" rmdir /s /q "%%d"
)

rem 3. Docker: detiene y borra los contenedores que levanto docker compose.
rem    Nunca borra las imagenes descargadas, como la de PostgreSQL (decision del usuario):
rem    asi volver a empezar es rapido. Los volumenes (los datos de la base) se conservan,
rem    salvo que se pida con "clear.bat --borrar-volumenes", que ademas pide confirmacion.
if /i "%~1"=="--borrar-volumenes" goto :volumenes
echo Deteniendo y borrando los contenedores del proyecto (los datos de la base se conservan)...
docker compose -f src\docker\docker-compose.yml --profile qa down
goto :fin

:volumenes
choice /c SN /m "Borrar tambien los volumenes: se pierden los datos de la base. Continuar"
if errorlevel 2 (
    echo Los volumenes se conservan; solo se borran los contenedores.
    docker compose -f src\docker\docker-compose.yml --profile qa down
) else (
    docker compose -f src\docker\docker-compose.yml --profile qa down -v
)

:fin
echo Limpieza terminada. Para volver a empezar, ejecute start-dev.bat o start-qa.bat.
