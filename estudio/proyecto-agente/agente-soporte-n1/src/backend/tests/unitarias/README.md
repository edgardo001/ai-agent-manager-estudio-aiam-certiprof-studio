# Pruebas unitarias

Prueban una función sola, con datos fijos, sin red ni base de datos. Son gratis y tardan menos de un segundo. Se escriben junto con el código de cada etapa, desde la etapa 3.

Desde `src/backend`: `.\.venv\Scripts\python.exe -m pytest tests/unitarias`

| Archivo | Qué prueba |
|---|---|
| `test_cargar_conocimiento.py` | el corte de los documentos en fragmentos: `trocear()`, `cortar_por_parrafos()` y `fragmentar_documento()` (decisión D8) |
| `test_herramientas.py` | que solo existan las tres herramientas, que se rechacen las desconocidas y los argumentos inválidos, que `buscar_cliente` no acepte otro cliente, que los datos marcados no se puedan cerrar desde adentro y que cada fragmento lleve su fuente |
| `test_piezas_simples.py` | `faltan_variables()`, `calcular_costo()`, `vector_a_texto()`, `armar_instrucciones()`, `armar_conversacion()` y `leer_version_prompt()` |
| `test_modelo.py` | cómo se lee la respuesta de la librería `openai`, sin llamar a Gemini: que el mensaje conserve la firma de pensamiento (D11), los pedidos de herramientas, el motivo de fin y los tokens |

En la etapa 4 se suman las de `reglas.py`.
