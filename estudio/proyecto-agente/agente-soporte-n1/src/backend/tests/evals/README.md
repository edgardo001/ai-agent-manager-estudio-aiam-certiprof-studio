# Evals del modelo

Comprueban que el agente se comporta como dicen sus instrucciones: las cinco dimensiones de validación de la sección 2.6 y las metas de la sección 2.5, con el modelo real y un modelo juez. Detalle: `docs/evals-del-llm.md`.

- `casos.jsonl`: el golden dataset, 40 casos, uno por línea en JSON.
- `test_busqueda.py`: la búsqueda sola, sin el modelo de chat (solo embeddings, menos de un minuto).
- `conftest.py`: corre los 40 casos con el agente real una vez por sesión, cada uno en una transacción que se deshace, llama al juez, calcula las métricas contra los umbrales (`UMBRALES`) y guarda todo en `ultima_corrida.json` (no se sube; su resumen va a `docs/pruebas/`). Ante un límite de uso, espera y reintenta.
- `juez.py`: el modelo juez (`LLM_MODELO_JUEZ`), que califica fidelidad, alucinación, relevancia y tono, o si un escalamiento estaba justificado.
- `test_dimensiones.py`: lo que debe cumplirse en cada caso: escalamiento y adversariales al 100%, y ningún texto prohibido.
- `test_metricas.py`: cada métrica contra su umbral.

Desde `src/backend`, con PostgreSQL levantado:

```
python -m pytest tests/evals/test_busqueda.py -s     la búsqueda sola, casi gratis
python -m pytest tests/evals                         una corrida: unas 150 llamadas, de 30 a 40 minutos
python -m pytest tests/evals --repeticiones 3        la corrida para aprobar el prompt (vale la mayoría)
```
