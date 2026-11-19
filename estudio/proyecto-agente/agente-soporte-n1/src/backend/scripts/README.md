# Scripts de asistencia

Esta carpeta guarda los scripts que se ejecutan sueltos para preparar, probar o estimar. No son parte del Agente de Soporte N1: el agente vive en `../aplicacion/` y nunca importa nada de aquí (decisión D10 de `docs/decisiones.md`). Los scripts sí usan la aplicación (su configuración, el modelo y la base de datos), y comparten el mismo entorno virtual, `requirements.txt` y `.env`. No entran en la imagen Docker.

Todos se ejecutan desde la carpeta `src/backend`, con el entorno virtual activo (`.venv\Scripts\activate`), con `python -m scripts.<nombre>`.

## Qué hace cada uno

| Script | Etapa | Para qué sirve | Cuándo usarlo |
|---|---|---|---|
| `prueba_conexion.py` | 0 | Prueba el modelo de chat (un saludo y si sabe usar herramientas) y el de embeddings (si entrega 768 números) | Al cambiar la clave, el modelo o el proveedor en el `.env` (`docs/modelos-y-costos.md`) |
| `listar_modelos.py` | 5 | Lista los modelos de Gemini (con la clave, sin mostrarla), los gratuitos de OpenRouter que aceptan herramientas y los de Ollama en el equipo; no llama a ningún modelo | Para elegir un modelo o al actualizar la lista comentada de `example.env` (`docs/modelos-y-costos.md`, sección 2) |
| `cargar_conocimiento.py` | 2 | Borra y vuelve a cargar en pgvector los documentos de `src/base-de-conocimiento/` | Cada vez que cambia un documento, y después de `clear.bat --borrar-volumenes` |
| `probar_busqueda.py` | 2 | Prueba la búsqueda sin el agente, con la misma función que usa su herramienta `buscar_solucion`: las consultas fijas (7 de 7 esperado) o una escrita por usted | Después de cargar el conocimiento o de cambiar la forma de fragmentar |
| `revisar_env.py` | 3 | Compara los nombres del `.env` con `example.env` y dice qué falta o sobra; con `--ordenar`, deja el `.env` con el orden y los comentarios de la plantilla, conservando sus valores (copia previa en `.env.respaldo`); nunca muestra los valores | Lo ejecuta `start-dev.bat` para avisar; a mano, cuando la plantilla cambió (D14) |
| `estimar_costos.py` | 2 | Estima, sin llamar al modelo, el costo de los embeddings y de cada consulta (`docs/modelos-y-costos.md`); desde la etapa 3, si hay tickets atendidos, usa su costo real promedio | Antes de cargar muchos documentos o al cambiar precios |

Ejemplos:

```
python -m scripts.prueba_conexion
python -m scripts.listar_modelos
python -m scripts.cargar_conocimiento
python -m scripts.probar_busqueda "mi factura sale cortada"
python -m scripts.estimar_costos --documentos 1000 --caracteres 20000
```

## Reglas para un script nuevo

1. Va aquí si se ejecuta suelto y el agente no lo necesita para atender un ticket. Si la API o la consola lo necesitan, va en `aplicacion/`.
2. Puede importar de `aplicacion`; la aplicación nunca importa de `scripts`. Si un script tiene lógica que el agente pasa a necesitar, esa lógica se mueve a `aplicacion/` (así pasó en la etapa 3 con `buscar()` de `probar_busqueda.py`, que ahora vive en `aplicacion/herramientas.py` y la usa la herramienta `buscar_solucion`).
3. Su comentario inicial empieza con “Script de asistencia” y dice cómo se ejecuta.
4. Se agrega a la tabla de arriba.
