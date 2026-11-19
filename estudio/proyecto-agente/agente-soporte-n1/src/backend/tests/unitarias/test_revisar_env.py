"""Pruebas unitarias de scripts/revisar_env.py: comparar y ordenar el .env sin perder valores."""
from scripts.revisar_env import comparar, leer_variables, ordenar

PLANTILLA = "# Claves\nGEMINI_API_KEY=\n# Modelo\nLLM_PROVEEDOR=gemini\nLLM_MODEL=gemini-3.1-flash-lite\n"
ENV = "LLM_MODEL=otro\n# comentario viejo\nVIEJA=1\nGEMINI_API_KEY=secreta\n"


def test_comparar_dice_que_falta_y_que_sobra():
    """Técnico: no viene del curso (decisión D14)."""
    assert comparar(leer_variables(PLANTILLA), leer_variables(ENV)) == (["LLM_PROVEEDOR"], ["VIEJA"])


def test_ordenar_conserva_los_valores_y_no_pierde_nada():
    """El .env queda con el orden y los comentarios de la plantilla, con sus propios valores;
    lo que falta toma el valor de ejemplo y lo que sobra queda al final. Técnico: no viene del curso."""
    nuevo = ordenar(PLANTILLA, leer_variables(ENV))
    assert nuevo.startswith("# Claves\nGEMINI_API_KEY=secreta\n# Modelo\nLLM_PROVEEDOR=gemini\nLLM_MODEL=otro\n")
    assert nuevo.rstrip().endswith("VIEJA=1")
    assert leer_variables(nuevo) == {"GEMINI_API_KEY": "secreta", "LLM_PROVEEDOR": "gemini", "LLM_MODEL": "otro", "VIEJA": "1"}
