# Scripts de PostgreSQL

Etapa 2: aquí están dos archivos, que PostgreSQL ejecuta en orden alfabético la primera vez que se crea el volumen de datos:

1. `01_esquema.sql`: la extensión pgvector y las seis tablas del plan.
2. `02_datos_ficticios.sql`: el registro del agente, con sus metas y su línea base, y los clientes del CRM simulado, todos ficticios. Los tickets de ejemplo llegan con la etapa 7, junto con el dashboard que los usa.

El número del nombre fija el orden: el esquema debe existir antes que los datos. Mientras no haya datos reales, para cambiar el esquema se edita el SQL y se recrea todo con `docker compose down -v` (o con `clear.bat --borrar-volumenes`, que pide confirmación). La imagen de PostgreSQL descargada nunca se borra, así que volver a levantar la base es rápido.

## Cómo se entera el contenedor de que debe ejecutar estos SQL

Técnico: no viene del curso. Pregunta del usuario del 2026-11-19.

No hay que decírselo en ninguna orden: lo hace la imagen oficial de PostgreSQL, en la que se basa `pgvector/pgvector:pg17`. Este es el paso a paso, revisado el 2026-11-19 dentro del contenedor del proyecto; los fragmentos de código están resumidos (el original usa `printf` y tiene más pasos), pero las condiciones y el orden son los reales.

0. **`docker-entrypoint-initdb.d` es una carpeta, no un archivo.** El `.d` final no es una extensión: en Linux, una carpeta terminada en `.d` guarda piezas sueltas que un programa recorre todas (`/etc/init.d/`, `/etc/cron.d/`, `/etc/nginx/conf.d/`). La imagen la trae vacía; si no se montara nada en ella, el script la recorrería sin encontrar archivos y la base quedaría sin tablas.
1. **El compose muestra esta carpeta dentro del contenedor.** `./postgres:/docker-entrypoint-initdb.d:ro` es un montaje (bind mount): no copia nada; la misma carpeta de Windows se ve dentro del contenedor con otro nombre, como un acceso directo, y `ro` (solo lectura) impide que el contenedor la modifique. La otra línea, `datos-postgres:/var/lib/postgresql/data`, guarda la base en un volumen con nombre: mientras exista, la carpeta de datos no está vacía y los SQL no se vuelven a ejecutar. `docker exec agente-soporte-n1-postgres-1 ls /docker-entrypoint-initdb.d` muestra los mismos tres archivos, y un cambio hecho en Windows se ve adentro al instante.
2. **Todo contenedor ejecuta un programa al arrancar.** La imagen define cuál: `docker inspect` muestra `Entrypoint: docker-entrypoint.sh` y `Cmd: postgres`. Docker ejecuta `docker-entrypoint.sh postgres`; ese script prepara todo y al final lanza PostgreSQL.
3. **El script decide si la base es nueva** mirando si existe el archivo `PG_VERSION` en la carpeta de datos, que PostgreSQL crea cuando arma una base:

    ```bash
    if [ -s "$PGDATA/PG_VERSION" ]; then
        DATABASE_ALREADY_EXISTS='true'
    ```

4. **Si la base es nueva, ejecuta la carpeta.** Crea la base con `POSTGRES_USER`, `POSTGRES_PASSWORD` y `POSTGRES_DB`, levanta un PostgreSQL temporal y recorre los archivos en orden alfabético; ejecuta los `.sql`, `.sql.gz` y `.sh`, e ignora los demás, como este README:

    ```bash
    if [ -z "$DATABASE_ALREADY_EXISTS" ]; then
        docker_init_database_dir                          # crea la base vacía
        docker_temp_server_start "$@"                     # PostgreSQL temporal
        docker_setup_db                                   # crea POSTGRES_DB
        docker_process_init_files /docker-entrypoint-initdb.d/*
        docker_temp_server_stop
    else
        echo "...contain a database; Skipping initialization"
    fi
    ```

    ```bash
    case "$f" in
        *.sql)  echo "running $f"; docker_process_sql -f "$f" ;;   # lo pasa a psql
        *)      echo "ignoring $f" ;;
    esac
    ```

5. **Arranca PostgreSQL de verdad.** El healthcheck del compose (`pg_isready`) lo marca “Healthy” y `start-dev.bat` sigue con la consola.

Un arranque posterior, con el volumen ya creado, encuentra `PG_VERSION`, imprime “Skipping initialization” y salta directo al paso 5. Los logs del contenedor (`docker logs agente-soporte-n1-postgres-1`) muestran qué se ejecutó; así quedó la reconstrucción desde cero del 2026-11-19:

```
docker-entrypoint.sh: running /docker-entrypoint-initdb.d/01_esquema.sql
docker-entrypoint.sh: running /docker-entrypoint-initdb.d/02_datos_ficticios.sql
docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/README.md
```

Tres consecuencias prácticas:

1. **Editar un SQL no cambia una base que ya existe.** El cambio se aplica solo al recrear el volumen (`clear.bat --borrar-volumenes` y luego `start-dev.bat`). Con datos reales, en cambio, se usaría `ALTER TABLE` en vez de recrear.
2. **Si un SQL falla, el arranque se detiene** y la base queda a medias. Se ve en los logs, se corrige el SQL y se recrea el volumen.
3. **Los fragmentos de la base de conocimiento no están en estos SQL.** Sus vectores los calcula el modelo de embeddings, así que después de recrear el volumen hay que ejecutar, desde `src\backend`, `.\.venv\Scripts\python.exe -m scripts.cargar_conocimiento`.
