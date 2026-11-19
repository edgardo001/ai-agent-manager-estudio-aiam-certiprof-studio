# Pruebas adversariales

No llaman al modelo y son gratis. Desde la etapa 5, `test_reglas_adversariales.py` intenta saltarse las reglas de `reglas.py`: ataques escritos a mano, propiedades con Hypothesis (genera cientos de textos al azar) y los límites conocidos de un patrón de palabras, marcados como falla esperada para que queden a la vista. En la etapa 6 se suma la robustez de la API (nunca un error 500). Detalle: `docs/estrategia-de-pruebas.md`.
