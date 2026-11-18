@echo off
rem Entorno de QA del Agente de Soporte N1.
rem Levanta todo con Docker Compose, incluida la app (perfil "qa"),
rem para probar el sistema tal como correria fuera del equipo de desarrollo.
rem Aparece en la etapa 0, pero funciona desde la etapa 6, cuando existen el compose y el Dockerfile.
rem Uso: doble clic, o "start-qa.bat" desde esta carpeta.
setlocal
cd /d "%~dp0src\docker"

if not exist ..\backend\Dockerfile (
    echo Todavia no existe src\backend\Dockerfile: la app dentro de Docker llega en la etapa 6.
    echo Por ahora use start-dev.bat.
    pause
    exit /b 1
)
if not exist docker-compose.yml (
    echo Todavia no existe src\docker\docker-compose.yml: llega en la etapa 2,
    echo y la app dentro de Docker, en la etapa 6. Por ahora use start-dev.bat.
    pause
    exit /b 1
)
if not exist .env (
    echo Falta src\docker\.env. Copie example.env como .env y completelo.
    pause
    exit /b 1
)

rem --profile qa suma la app a los servicios de apoyo; --build reconstruye su imagen con el codigo actual.
docker compose --profile qa up -d --build || goto :error
docker compose --profile qa ps
goto :eof

:error
echo.
echo Algo fallo. Revise el mensaje de arriba.
pause
exit /b 1
