# Documentación del proyecto: por dónde empezar

Este es el mapa de `docs/`. Para entender el proyecto bastan los tres primeros; el resto se consulta cuando hace falta.

## Empiece aquí

1. `plan-del-proyecto.md`: manda sobre todo lo demás. Empiece por “El flujo completo, en simple”; tiene el estado, las reglas, las etapas, el modelo de datos, lo que pide el curso y dónde se cubre, y lo que se posterga.
2. `lecciones-aprendidas.md`: lo que enseñó cada etapa, en un solo lugar, cada lección con un enlace a su detalle.
3. `diagramas-del-codigo.md`: el código real: qué archivo y qué función hace cada cosa, y quién llama a quién.

## Consulte cuando necesite...

- **saber por qué se eligió algo:** `decisiones.md` (D1 a D16, con un índice al inicio).
- **entender la búsqueda del agente:** `rag.md`: qué es un embedding, por qué 768 números, cómo cambiar de modelo y las buenas prácticas de RAG y de agentes que se adoptan.
- **cambiar de proveedor o estimar el gasto:** `modelos-y-costos.md`: cómo probar OpenRouter u Ollama, respaldo ante caídas y las cifras de costo.
- **escribir o correr pruebas:** `estrategia-de-pruebas.md` (los cinco tipos, incluidas las adversariales) y `evals-del-llm.md` (el plan de evals de la etapa 5, con sus metas y umbrales).
- **revisar la seguridad:** `seguridad-owasp.md`: los Top 10 de OWASP (aplicaciones con LLM y APIs), qué cubre ya el proyecto, qué falta y cuándo revisarlo.
- **mirar más allá de esta versión:** `referencia/`: `arquitectura.md` (hacia dónde podría crecer el sistema) y `anonimizacion-de-datos.md` (cómo proteger datos personales cuando haya datos reales).

## Historia (no hace falta leer)

- `pruebas/`: lo que se probó en cada etapa, con sus conteos y mediciones, y qué enseñó.
- `revisiones/`: las revisiones de calidad (EGM y fidelidad al curso) y qué se hizo con ellas.
