# Anonimización de datos sensibles, sin enviarlos fuera del equipo

Cómo se protegen los datos personales de documentos (Markdown o PDF) y de tickets antes de usarlos, guardarlos o enviarlos a un modelo remoto, a partir de las preguntas del usuario del 2026-11-18. **Estado en el proyecto: postergado** (fila “Anonimizar datos sensibles” en la tabla de lo postergado del plan), porque todos los datos del proyecto son ficticios. Este documento queda como guía para cuando haga falta.

## 1. Anonimizar y seudonimizar

- **Anonimizar:** quitar o reemplazar los datos que identifican a una persona sin posibilidad de volver atrás.
- **Seudonimizar:** reemplazarlos por etiquetas (`<PERSONA_1>`, `<RUT_1>`) y guardar aparte una tabla etiqueta → dato real, para poder reponerlos. Para la ley (por ejemplo, el GDPR europeo), un dato seudonimizado sigue siendo un dato personal.

Para el agente conviene **seudonimizar**: Gemini solo ve `<PERSONA_1>`, y el programa repone el nombre real antes de mostrar la respuesta al cliente.

## 2. Qué dice el curso

El curso no enseña la técnica; cubre la privacidad con principios de gobierno:

- **Permisos mínimos** (Módulo 2, sección 2.3): el agente solo accede a los datos que su tarea necesita.
- **Restricción explícita** (sección 2.5, en el ejemplo del agente de soporte): no compartir información de otros clientes.
- **Ethics Reviewer** (Módulo 4, sección 4.5): evalúa sesgo, privacidad, equidad y cumplimiento de políticas en los outputs del agente, y puede activar el circuit breaker.
- **Audit trail** (Módulo 1, pregunta 9): registro de lo que decidió el agente y por qué.

Todo lo que sigue no viene en el curso.

## 3. Cómo se hace en el propio equipo, en cuatro pasos

Hay que programar algo, pero no desde cero, y todo corre sin internet:

1. **Extraer el texto.** Un `.md` ya es texto. Un PDF se lee con `pypdf` (BSD), que ya se usó en este repositorio para convertir el curso; si está escaneado, hace falta OCR, por ejemplo Tesseract (Apache 2.0).
2. **Detectar los datos personales,** con dos técnicas según el tipo de dato (sección 4).
3. **Reemplazar** cada dato por una etiqueta (seudonimizar) o borrarlo (anonimizar).
4. **Medir y revisar.** Ningún detector encuentra el 100%. Se arma un conjunto de documentos de prueba con los datos marcados a mano y se mide cuántos se escapan (es la misma idea de las evals, `../evals-del-llm.md`), y se revisa una muestra a mano, como el muestreo de la sección 3.3 aplicado a la privacidad.

## 4. Cómo se encuentran nombres, RUT, direcciones y otros datos

| Tipo de dato | Técnica | Qué tan fiable es |
|---|---|---|
| RUT, correo, teléfono, tarjeta de crédito, IP | **patrones (regex) más una validación:** el dígito verificador del RUT (módulo 11) o la fórmula de Luhn de las tarjetas, para no confundir cualquier número con un dato | muy fiable |
| Nombres, direcciones, empresas | **NER** (reconocimiento de entidades nombradas): un modelo pequeño que corre en el equipo y marca “esto es una persona”, “esto es un lugar”, “esto es una organización” | bueno, pero se le escapan casos; las direcciones son lo más difícil |
| Lo que ninguno detecta | lista propia de términos (nombres de clientes conocidos, códigos internos) y revisión humana por muestreo | depende de la lista |

**Ejemplo para el RUT,** sin librerías (probado el 2026-11-18: `12.345.678-5` y `11111111-1` son válidos, `12.345.678-9` no, y `2024-11` no se confunde con un RUT). Es un ejemplo; no está en el código del proyecto:

```python
import re

# Con o sin puntos, guion y dígito verificador (número o K).
PATRON_RUT = re.compile(r"\b(\d{1,2}\.?\d{3}\.?\d{3})-([\dkK])\b")


def rut_valido(numero, digito):
    """Valida el dígito verificador con el módulo 11.
    Técnico: no viene del curso."""
    suma, factor = 0, 2
    for cifra in reversed(numero.replace(".", "")):
        suma += int(cifra) * factor
        factor = 2 if factor == 7 else factor + 1
    esperado = {10: "K", 11: "0"}.get(11 - suma % 11, str(11 - suma % 11))
    return esperado == digito.upper()


def seudonimizar_ruts(texto):
    """Reemplaza cada RUT válido por <RUT_n> y devuelve el texto y la tabla para reponerlos.
    Técnico: no viene del curso."""
    tabla = {}
    def reemplazar(encontrado):
        if not rut_valido(*encontrado.groups()):
            return encontrado.group(0)
        etiqueta = f"<RUT_{len(tabla) + 1}>"
        tabla[etiqueta] = encontrado.group(0)
        return etiqueta
    return PATRON_RUT.sub(reemplazar, texto), tabla
```

## 5. Herramientas y sus licencias (regla 13 del plan)

| Herramienta | Para qué | Licencia | ¿Cumple la regla? |
|---|---|---|---|
| Presidio | une patrones y NER; trae operadores para reemplazar, enmascarar, borrar, cifrar o hashear; se le agregan reconocedores propios (no trae el RUT chileno) | MIT | sí |
| spaCy (la librería) | NER, la usa Presidio por defecto | MIT | sí |
| Modelos de spaCy en español (`es_core_news_sm`, `md`, `lg`) | el modelo de idioma del NER | **GPL-3.0** | **no:** habría que usar otro modelo de NER con licencia permisiva, revisando cada uno |
| `pypdf` | extraer el texto de un PDF | BSD | sí |
| Tesseract | OCR de documentos escaneados | Apache 2.0 | sí |

Un modelo de lenguaje local (por ejemplo, con Ollama) también puede detectar datos personales sin salir del equipo, pero es más lento, menos predecible y la licencia depende de cada modelo.

## 6. Marcos de referencia

No hay un estándar único de cómo programarlo, pero sí marcos que se usan como guía:

- **ISO/IEC 20889:** terminología y clasificación de las técnicas de desidentificación.
- **NIST SP 800-188:** guía de desidentificación de datos del gobierno de Estados Unidos.
- **GDPR** (Unión Europea): distingue el dato seudonimizado (sigue siendo personal) del anonimizado (ya no lo es).
- **En Chile, la Ley 21.719** de protección de datos personales: si se usa, conviene revisar su vigencia y sus requisitos.

## 7. Cómo aplicaría al proyecto

- **Base de conocimiento:** lo ideal es que los documentos de procedimientos no tengan datos personales; si los tienen, se anonimizan al cargarlos, en `cargar_conocimiento.py`, antes de calcular los embeddings.
- **Tickets:** ahí sí habrá datos personales. Se seudonimiza el texto del cliente antes de enviarlo a Gemini, se repone en la respuesta y la auditoría guarda solo lo necesario, enmascarado.
- **PDF:** tapar un dato con un recuadro negro no borra el texto que está debajo; para el RAG se trabaja con el texto extraído, que es el que hay que limpiar.
- **Señal para hacerlo:** cuando el agente atienda clientes reales o se carguen documentos con datos personales.

## Fuentes consultadas el 2026-11-18

- [es-core-news-sm en PyPI](https://pypi.org/project/es-core-news-sm): licencia GPL-3.0 del modelo en español.
- [Presidio: preguntas frecuentes](https://microsoft.github.io/presidio/faq/) y [notebook de ejemplo](https://microsoft.github.io/presidio/samples/python/presidio_notebook): reconocedores propios.
- [Presidio con varios idiomas](https://python.langchain.com/docs/guides/privacy/presidio_data_anonymization/multi_language): uso en español con un modelo de spaCy.
- [Artículo sobre Presidio](https://pasqualepillitteri.it/en/news/5538/microsoft-presidio-pii-data-protection-ai): operadores y licencia MIT.
