"""Pruebas unitarias del corte de documentos en fragmentos (scripts/cargar_conocimiento.py).
Técnico: no viene del curso; prueban la forma de cortar decidida en D8."""
from scripts.cargar_conocimiento import SOLAPE, TAMANO_FRAGMENTO, cortar_por_parrafos, fragmentar_documento, trocear


def test_trocear_un_texto_corto_queda_entero():
    """Un texto que cabe en un fragmento no se corta."""
    assert trocear("a" * TAMANO_FRAGMENTO) == ["a" * TAMANO_FRAGMENTO]


def test_trocear_un_texto_largo_se_solapa():
    """Un texto más largo que un fragmento se corta en partes que repiten SOLAPE caracteres."""
    pedazos = trocear("".join(str(i % 10) for i in range(2000)))
    assert len(pedazos) == 2
    assert pedazos[0][-SOLAPE:] == pedazos[1][:SOLAPE]


def test_trocear_no_repite_el_pedazo_final():
    """Corrección de la revisión de la etapa 2: 2.100 caracteres dan 2 pedazos, no 3."""
    assert len(trocear("a" * 2100)) == 2


def test_cortar_por_parrafos_no_parte_un_parrafo():
    """Los párrafos se juntan enteros hasta el tamaño máximo; ninguno queda partido."""
    parrafos = ["p" * 700, "q" * 700, "r" * 100]
    partes = cortar_por_parrafos("\n\n".join(parrafos))
    assert partes == ["p" * 700, "q" * 700 + "\n\n" + "r" * 100]


def test_fragmentar_documento_por_secciones_con_titulo():
    """Cada sección es un fragmento que empieza con "Título - Sección"; la introducción
    no incluye el aviso de documento ficticio (las líneas que empiezan con ">")."""
    texto = "# Cuenta bloqueada\n> Documento ficticio.\nIntro breve.\n## Pasos\n1. Esperar.\n## Si no funciona\nEscalar."
    fragmentos = fragmentar_documento(texto)
    assert [seccion for seccion, _ in fragmentos] == ["Introducción", "Pasos", "Si no funciona"]
    assert fragmentos[1][1] == "Cuenta bloqueada - Pasos\n1. Esperar."
    assert "ficticio" not in fragmentos[0][1]


def test_fragmentar_documento_vacio_no_da_fragmentos():
    """Un documento con título y aviso, pero sin contenido, no da fragmentos (la carga lo omite)."""
    assert fragmentar_documento("# Título\n> Documento ficticio.\n") == []
