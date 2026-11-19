# Scripts de asistencia

Esta carpeta guarda los scripts que se ejecutan sueltos para preparar, probar o estimar. No son parte del Agente de Soporte N1: el agente vive en `../aplicacion/` y nunca importa nada de aquí (decisión D10 de `docs/decisiones.md`). Los scripts sí usan la aplicación (su configuración, el modelo y la base de datos), y comparten el mismo entorno virtual, `requirements.txt` y `.env`. No entran en la imagen Docker.

Todos se ejecutan desde la carpeta `src/backend`, con el entorno virtual activo (`.venv\Scripts\activate`), con `python -m scripts.<nombre>`.

## Qué hace cada uno

| Script | Etapa | Para qué sirve | Cuándo usarlo |
|---|---|---|---|
| `prueba_conexion.py` | 0 | Manda un saludo al modelo y muestra la respuesta | Al cambiar la clave o el modelo en el `.env` |
| `cargar_conocimiento.py` | 2 | Borra y vuelve a cargar en pgvector los documentos de `src/base-de-conocimiento/` | Cada vez que cambia un documento, y después de `clear.bat --borrar-volumenes` |
| `probar_busqueda.py` | 2 | Prueba la búsqueda sin el agente: las consultas fijas (7 de 7 esperado) o una escrita por usted | Después de cargar el conocimiento o de cambiar la forma de fragmentar |
| `estimar_costos.py` | 2 | Estima, sin llamar al modelo, el costo de los embeddings y de cada consulta (`docs/costos.md`) | Antes de cargar muchos documentos o al cambiar precios |

Ejemplos:

```
python -m scripts.prueba_conexion
python -m scripts.cargar_conocimiento
python -m scripts.probar_busqueda "mi factura sale cortada"
python -m scripts.estimar_costos --documentos 1000 --caracteres 20000
```

## Reglas para un script nuevo

1. Va aquí si se ejecuta suelto y el agente no lo necesita para atender un ticket. Si la API o la consola lo necesitan, va en `aplicacion/`.
2. Puede importar de `aplicacion`; la aplicación nunca importa de `scripts`. Si un script tiene lógica que el agente pasa a necesitar, esa lógica se mueve a `aplicacion/` (así pasará con `buscar()` de `probar_busqueda.py`, que en la etapa 3 se convierte en la herramienta `buscar_solucion`).
3. Su comentario inicial empieza con “Script de asistencia” y dice cómo se ejecuta.
4. Se agrega a la tabla de arriba.
