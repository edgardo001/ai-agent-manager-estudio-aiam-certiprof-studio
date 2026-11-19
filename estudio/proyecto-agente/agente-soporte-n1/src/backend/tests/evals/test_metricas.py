"""Evals de métricas (etapa 5): cada métrica de la corrida contra su umbral, una prueba por métrica.

Las métricas y los umbrales están en conftest.py (UMBRALES), con de dónde sale cada uno: las metas
de la sección 2.5 del curso (80% de resolución autónoma, 20% de escalamiento, 3 minutos) y los
umbrales del juez que fija el proyecto (evals-del-llm.md, sección 4).
Uso, desde src/backend: python -m pytest tests/evals
"""


def test_la_metrica_cumple_su_umbral(corrida, metrica):
    datos = corrida["metricas"][metrica]
    assert datos["cumple"], f"{metrica}: {datos['valor']}, umbral {datos['umbral']}"
