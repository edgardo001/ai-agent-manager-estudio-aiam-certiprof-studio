# Scripts de PostgreSQL

Etapa 2: aquí irán dos archivos, que PostgreSQL ejecuta en orden alfabético la primera vez que se crea el volumen de datos:

1. `01_esquema.sql`: la extensión pgvector y las seis tablas del plan.
2. `02_datos_ficticios.sql`: el registro del agente, los clientes del CRM simulado, la línea base y un historial de tickets ficticios, marcados como tales.

El número del nombre fija el orden: el esquema debe existir antes que los datos. Mientras no haya datos reales, para cambiar el esquema se edita el SQL y se recrea todo con `docker compose down -v` (o con `clear.bat`, confirmando la parte de Docker).
