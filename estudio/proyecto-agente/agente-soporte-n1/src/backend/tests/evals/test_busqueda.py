"""Eval de la búsqueda sola (etapa 5): ¿la búsqueda del agente encuentra el documento correcto?

Usa la misma función que la herramienta buscar_solucion (herramientas.buscar) con el texto del
cliente de cada caso de casos.jsonl, sin llamar al modelo de chat: solo cuesta un embedding por caso.
Si el fragmento correcto no llega, el modelo no puede acertar (rag.md, sección 8).

Uso, desde src/backend, con PostgreSQL levantado y la base de conocimiento cargada:
    python -m pytest tests/evals/test_busqueda.py -s
-s muestra la tabla de cada caso. Necesita la clave de los embeddings.

Curso: solo soluciones documentadas (Módulo 2, sección 2.5) y la validación funcional antes de
producción (sección 2.6). Las métricas de recuperación son técnicas: no vienen del curso.
"""
import json
from pathlib import Path

from aplicacion import herramientas

CASOS = [json.loads(linea) for linea in Path(__file__).with_name("casos.jsonl").read_text(encoding="utf-8").splitlines()]
UMBRAL_RECALL = 0.90  # recall@5 de 90% o más (evals-del-llm.md, sección 4; umbral del proyecto)


def medir(conexion, caso):
    """Busca el texto del cliente y devuelve (posición del documento esperado o None, documentos
    encontrados, parecido del primero). Técnico: no viene del curso."""
    fragmentos = herramientas.buscar(conexion, caso["entrada"])
    documentos = [documento for documento, _, _, _, _ in fragmentos]
    posicion = documentos.index(caso["documento_esperado"]) + 1 if caso["documento_esperado"] in documentos else None
    return posicion, documentos, fragmentos[0][3] if fragmentos else 0.0


def test_la_busqueda_encuentra_el_documento_esperado(conexion):
    """recall@5: en qué parte de los casos el documento esperado está entre los 5 fragmentos.
    precision@5: qué parte de los 5 fragmentos es de ese documento. MRR: el promedio de 1 dividido
    por la posición del primero correcto (1 si siempre sale primero). Con un solo documento esperado
    por caso, la tasa de acierto es igual al recall@5."""
    con_documento = [caso for caso in CASOS if caso["documento_esperado"]]
    posiciones, precisiones = [], []
    print(f"\n{'caso':<42} {'pos.':>4} {'parecido':>8}  documentos encontrados")
    for caso in con_documento:
        posicion, documentos, parecido = medir(conexion, caso)
        posiciones.append(posicion)
        precisiones.append(documentos.count(caso["documento_esperado"]) / max(len(documentos), 1))
        marca = posicion if posicion else "NO"
        print(f"{caso['id']:<42} {marca:>4} {parecido:>8.3f}  {', '.join(dict.fromkeys(documentos))}")

    recall = sum(p is not None for p in posiciones) / len(posiciones)
    precision = sum(precisiones) / len(precisiones)
    mrr = sum(1 / p for p in posiciones if p) / len(posiciones)
    print(f"\nrecall@5 {recall:.0%} | precision@5 {precision:.0%} | MRR {mrr:.2f} | {len(posiciones)} casos")

    print(f"\n{'casos sin documento':<42} {'parecido':>13}  documento más parecido")
    for caso in CASOS:
        if not caso["documento_esperado"]:
            _, documentos, parecido = medir(conexion, caso)
            print(f"{caso['id']:<42} {parecido:>13.3f}  {documentos[0] if documentos else '-'}")

    assert recall >= UMBRAL_RECALL, f"recall@5 de {recall:.0%}, bajo el umbral de {UMBRAL_RECALL:.0%}"
