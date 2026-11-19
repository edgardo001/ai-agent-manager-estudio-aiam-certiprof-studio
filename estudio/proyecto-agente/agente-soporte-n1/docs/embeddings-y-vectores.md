# Embeddings y vectores: cómo funcionan y por qué 768 números

Explicación técnica de los vectores que guarda el RAG del proyecto, a partir de las preguntas del usuario del 2026-11-18. **Nada de esto viene en el curso:** es la técnica con que el proyecto busca las soluciones documentadas que pide el Módulo 2, sección 2.5. Las decisiones están en `decisiones.md` (D2, D5, D8 y D9) y el código en `src/backend/aplicacion/modelo.py` (`crear_embedding()`) y `base_de_datos.py`.

## 1. Qué es un embedding

Un embedding (vector semántico) es la lista de números con que un modelo representa el **significado** de un texto. Funciona así:

1. El modelo corta el texto en tokens (trozos de palabras) y los procesa todos juntos.
2. Al final resume el texto completo en **un solo punto** de un espacio de muchas dimensiones. Cada número es una coordenada de ese punto, como (x, y) en un plano, pero con 768 ejes.
3. Los textos de significado parecido quedan cerca. La búsqueda mide esa cercanía con la distancia de coseno (`<=>` en pgvector): 1 es idéntico y, mientras más bajo, menos se parecen.

Un número suelto no significa nada por sí solo (no hay un eje “contraseñas”): lo que importa es la posición del punto completo frente a los demás.

## 2. El largo no depende del texto: prueba real

Prueba hecha el 2026-11-18 con `gemini-embedding-001` y el `.env` del usuario:

| Texto | Caracteres | Números del vector |
|---|---|---|
| “hola” | 4 | 768 |
| un párrafo sobre contraseñas | 1.275 | 768 |
| “olvidé mi clave” | 15 | 768 |
| “mi impresora corta las facturas” | 31 | 768 |

| Comparación | Parecido (coseno) |
|---|---|
| “olvidé mi clave” frente al párrafo de contraseñas | 0,86 |
| “olvidé mi clave” frente a “mi impresora corta las facturas” | 0,55 |

Para repetirla, desde `src/backend`, con el entorno virtual:

```python
from aplicacion.modelo import crear_embedding
import math

textos = ["hola", "No puedo entrar a mi cuenta, olvidé la contraseña. " * 25,
          "olvidé mi clave", "mi impresora corta las facturas"]
vectores = crear_embedding(textos)
for texto, vector in zip(textos, vectores):
    print(len(texto), "caracteres ->", len(vector), "números")

def coseno(a, b):
    return sum(x * y for x, y in zip(a, b)) / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))

print("clave frente a contraseñas:", round(coseno(vectores[2], vectores[1]), 2))
print("clave frente a impresora:", round(coseno(vectores[2], vectores[3]), 2))
```

## 3. No es relleno, cifrado ni Base64

| | Base64 | Cifrado | Huella SHA-256 | Embedding |
|---|---|---|---|---|
| ¿Guarda el texto? | sí, solo lo recodifica | sí, oculto con una clave | no | no |
| ¿Se puede volver al texto? | sí | sí, con la clave | no | no |
| ¿El largo depende del texto? | sí | sí | no: siempre 64 caracteres | no: siempre 768 números |
| ¿Usa relleno? | sí (`=`) | según el algoritmo | no | no |
| ¿Textos parecidos dan resultados parecidos? | no | no | no: cambiar una letra cambia toda la huella | **sí: es su propósito** |

Lo más parecido es la huella SHA-256 (largo fijo, no reversible), con la diferencia clave de la última fila. Un embedding es un **resumen del significado, con pérdida**.

## 4. Qué cambia el tamaño del fragmento

El tamaño del fragmento y su solape **no cambian el largo del vector, pero sí su calidad:**

- **Fragmento grande:** mezcla temas y su punto queda en un “promedio” borroso entre ellos, que no se parece mucho a ninguna consulta. Por eso el proyecto corta por secciones (D8).
- **Fragmento chico:** pierde contexto (“haga clic en Guardar”, ¿de qué pantalla?). Por eso cada fragmento lleva antepuesto “Título - Sección”.
- **Solape:** solo evita que una idea quede partida en el corte; no influye en el vector.
- **Máximo de entrada:** cada modelo acepta un máximo de tokens; más allá, corta el texto o da error. Los 1.200 caracteres del proyecto (unos 300 tokens) quedan muy por debajo.

## 5. Por qué 768

- `gemini-embedding-001` entrega **3.072 números** si no se le pide otra cosa, y acepta el parámetro `dimensions` para pedir menos.
- Está entrenado para que **los primeros números concentren lo más importante** (técnica conocida como Matryoshka Representation Learning, por las muñecas rusas): una versión corta pierde poca calidad.
- **Espacio:** pgvector guarda cada número en 4 bytes; 768 números ocupan unos 3 KB por fragmento, frente a unos 12 KB con 3.072.
- **Índice:** el índice HNSW de pgvector admite vectores de hasta 2.000 dimensiones; 3.072 no se podría indexar con el tipo `vector`.
- 768 no es un estándar: es una elección del proyecto.

## 6. Si se cambia de modelo o de proveedor

Cada modelo fija su propio tamaño. Ejemplos: 1.536 o 3.072 en los modelos de embeddings de OpenAI (que también aceptan `dimensions`), y 384, 768 o 1.024 en varios modelos abiertos, muchos de tamaño fijo. Con otro proveedor, como OpenRouter, primero hay que confirmar que ofrezca embeddings para el modelo elegido.

Qué hacer al cambiar de modelo de embeddings:

1. Revisar el tamaño que entrega el modelo nuevo y si acepta `dimensions`.
2. Si el tamaño cambia, **no hay que reconstruir la base ni las otras tablas:** solo cambia el tipo de la columna `embedding`. Como los vectores del modelo anterior no sirven con el nuevo, primero se borran, y luego se cambia el tipo; PostgreSQL rehace solo el índice HNSW:

    ```sql
    BEGIN;
    DELETE FROM fragmentos_conocimiento;            -- los vectores del modelo anterior
    ALTER TABLE fragmentos_conocimiento ALTER COLUMN embedding TYPE vector(384);  -- el tamaño nuevo
    COMMIT;
    ```

    Probado el 2026-11-18 dentro de una transacción deshecha al final (`ROLLBACK`): el tipo quedó en `vector(384)`, el índice siguió existiendo y las demás tablas no se tocaron. Además, se actualizan `DIMENSIONES_EMBEDDING` en `modelo.py` y `vector(768)` en `src/docker/postgres/01_esquema.sql`, para que una base nueva se cree con el tamaño correcto.
3. Cambiar `LLM_MODELO_EMBEDDINGS` en el `.env` y recargar con `cargar_conocimiento.py`.

Si el modelo nuevo acepta `dimensions` y permite 768 o más, basta con pedirle 768: no hay que tocar la base, solo recargar (paso 3).

**Nunca se mezclan vectores de modelos distintos, aunque tengan el mismo tamaño:** cada modelo ubica los significados en un espacio propio, y comparar puntos de dos espacios no tiene sentido. Por eso cada fragmento guarda `modelo_embedding` y la búsqueda solo compara vectores del mismo modelo que la consulta (D8).

## 7. Cuánto cuesta calcular los embeddings

Para estimarlo con sus propios números, use `estimar_costos.py`, explicado en `costos.md`, que también estima el costo de cada consulta.

**Se cobra por tokens de entrada, nada más:** un embedding no tiene tokens de salida. El precio de `gemini-embedding-001` publicado por Google es de **0,15 dólares por millón de tokens** (y la mitad en modo por lotes, según sitios que comparan precios; confirmarlo en la página de precios de Google antes de usarlo). Google AI Studio también permite usarlo gratis, con límites de uso.

**El costo depende del total de texto, no de la cantidad de documentos:** un documento de 10.000 caracteres cuesta lo mismo que diez de 1.000. Lo que suma tokens:

| Qué | Cuánto suma |
|---|---|
| El texto de los documentos | una regla práctica: un token son unos 4 caracteres en inglés, algo menos en español |
| “Título - Sección” antepuesto a cada fragmento | unos pocos tokens por fragmento |
| El solape | solo en párrafos de más de 1.200 caracteres: hasta un 20% más en esos párrafos |
| Cada recarga completa | se paga todo de nuevo: `cargar_conocimiento.py` borra y recalcula todo |
| Cada búsqueda | la consulta también se convierte en vector: unos pocos tokens por búsqueda |

**Cómo enterarse:**

1. **Estimarlo antes:** sumar los caracteres de los fragmentos, dividir por 4 para tener los tokens (por arriba, conviene dividir por 3) y multiplicar por el precio.
2. **Verlo después:** en el panel de uso y facturación de Google AI Studio. La respuesta del punto de acceso compatible con OpenAI **no informa los tokens de los embeddings** (`usage` llega vacío; comprobado el 2026-11-18), así que el programa no puede contarlos solo.

**Estimación con datos reales y ejemplos** (con 0,15 dólares por millón de tokens y 4 caracteres por token):

| Caso | Caracteres | Tokens aproximados | Costo aproximado por carga |
|---|---|---|---|
| Los 8 documentos del proyecto (23 fragmentos, medido) | 6.091 | 1.500 | 0,0002 dólares |
| 10 documentos cortos (2.000 caracteres cada uno) | 20.000 | 5.000 | 0,0008 dólares |
| 10 documentos largos (100.000 cada uno, unas 30 páginas) | 1.000.000 | 250.000 | 0,04 dólares |
| 1.000 documentos de 20.000 caracteres | 20 millones | 5 millones | 0,75 dólares |
| 10.000 documentos de 50.000 caracteres | 500 millones | 125 millones | 19 dólares |

Lo que enseña: con pocos documentos el costo es despreciable; con miles, lo que más pesa es **recargar todo cada vez**. Por eso, a esa escala, se agrega la carga incremental (solo los documentos cuya huella `hash_documento` cambió), que está en la tabla de lo postergado del plan. Calcular los embeddings cuesta mucho menos que conversar: el modelo de chat cobra 0,25 dólares por millón de tokens de entrada y 1,50 de salida (D5), y en cada ticket envía el prompt y los fragmentos encontrados.

