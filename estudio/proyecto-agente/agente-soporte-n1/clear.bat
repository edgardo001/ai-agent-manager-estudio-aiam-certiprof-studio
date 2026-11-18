@echo off
rem Limpieza del Agente de Soporte N1: libera espacio en el equipo.
rem Borra lo que se descarga o se genera solo, y se vuelve a crear con start-dev.bat
rem o start-qa.bat. Nunca borra el codigo, los documentos ni src\docker\.env (sus claves).
rem Uso: doble clic, o "clear.bat" desde esta carpeta. Aparece en la etapa 0.
setlocal
cd /d "%~dp0"

rem 1. Entorno virtual de Python, con todas las librerias descargadas
if exist src\backend\.venv (
    echo Borrando el entorno virtual src\backend\.venv...
    rmdir /s /q src\backend\.venv
)

rem 2. Carpetas de cache de Python y de pytest
for /d /r src %%d in (__pycache__ .pytest_cache) do (
    if exist "%%d" rmdir /s /q "%%d"
)

rem 3. Docker: contenedores, volumenes (los datos de la base) e imagenes del proyecto. Pide confirmacion.
if exist src\docker\docker-compose.yml (
    choice /c SN /m "Borrar tambien contenedores, datos de la base e imagenes de Docker del proyecto"
    if errorlevel 2 (
        echo Docker no se toca.
    ) else (
        docker compose -f src\docker\docker-compose.yml --profile qa down -v --rmi all
    )
)

echo Limpieza terminada. Para volver a empezar, ejecute start-dev.bat o start-qa.bat.
