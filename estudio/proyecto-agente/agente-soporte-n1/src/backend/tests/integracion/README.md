# Pruebas de integración

Prueban el código junto con el PostgreSQL de desarrollo, sin llamar al modelo. Necesitan PostgreSQL levantado (`start-dev.bat`); si no responde, se omiten con un aviso. Son gratis y tardan unos segundos. Se escriben desde la etapa 3.

Desde `src/backend`: `.\.venv\Scripts\python.exe -m pytest tests/integracion`

**No dejan datos:** la fixture `conexion` de `tests/conftest.py` deshace al final de cada prueba todo lo que escribió (`rollback`). Funciona porque el código del agente no confirma los cambios; lo hace quien llama (decisión D11).

| Archivo | Qué prueba |
|---|---|
| `test_base_de_datos.py` | la búsqueda por parecido con vectores escritos a mano, el registro del agente, los clientes y los tickets con su conversación y sus tokens |
| `test_agente.py` | el bucle del agente con un **modelo falso**, que entrega respuestas escritas de antemano: resolver con una solución documentada, escalar con el contexto completo (y antes que otras herramientas), varias herramientas en un mensaje, rechazar una herramienta desconocida o argumentos inválidos, el segundo mensaje de un ticket, escalar por el tope de tokens, por el máximo de llamadas, por una falla del modelo o de una herramienta, o por una respuesta vacía o cortada, y no volver a atender un ticket escalado. Cada prueba revisa cuántas veces se llamó al modelo |

El modelo falso prueba gratis y siempre igual lo que controla el código. Cómo se comporta el modelo real se prueba en las evals (etapa 5).
