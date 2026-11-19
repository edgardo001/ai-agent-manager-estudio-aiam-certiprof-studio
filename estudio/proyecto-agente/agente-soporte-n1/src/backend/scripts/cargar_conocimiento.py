"""Script de asistencia, etapa 2: carga los documentos de src/base-de-conocimiento/ en pgvector.

Uso, desde la carpeta src/backend con el entorno virtual activo y PostgreSQL levantado (start-dev.bat):
    python -m scripts.cargar_conocimiento
Se corre cada vez que cambian los documentos. Borra lo cargado antes y vuelve a
cargar todo, así la base siempre refleja exactamente lo que hay en la carpeta.

Cómo se corta cada documento (decisión D8), en tres niveles:
  1. por secciones (cada "## " del Markdown); el texto antes de la primera sección
     es la sección "Introducción";
  2. si una sección pasa de TAMANO_FRAGMENTO caracteres, por párrafos completos;
  3. si un solo párrafo pasa de ese tamaño, por caracteres, con SOLAPE.
Cada fragmento lleva antepuesto "Título - Sección", para que se entienda solo.
El formato que deben tener los documentos está en src/base-de-conocimiento/README.md.
"""
import hashlib
from pathlib import Path

from aplicacion import config
from aplicacion.base_de_datos import borrar_fragmentos, conectar, guardar_fragmento
from aplicacion.modelo import crear_embedding

# src/backend/scripts/cargar_conocimiento.py -> src/base-de-conocimiento/
CARPETA_DOCUMENTOS = Path(__file__).resolve().parents[2] / "base-de-conocimiento"

# Tamaño máximo de cada fragmento y cuánto se repite del anterior, en caracteres.
# 1.200 caracteres son unos 300 tokens, muy por debajo del máximo del modelo de embeddings.
# El solape evita que una idea quede partida justo en el corte.
TAMANO_FRAGMENTO = 1200
SOLAPE = 200


def trocear(texto):
    """Corta un texto en pedazos de TAMANO_FRAGMENTO caracteres que se solapan en SOLAPE.
    Es el último recurso, para un párrafo que solo ya es demasiado largo.
    Técnico: no viene del curso."""
    pedazos = []
    inicio = 0
    while True:
        pedazos.append(texto[inicio:inicio + TAMANO_FRAGMENTO])
        if inicio + TAMANO_FRAGMENTO >= len(texto):  # este pedazo ya llegó al final del texto
            return pedazos
        inicio += TAMANO_FRAGMENTO - SOLAPE


def cortar_por_parrafos(cuerpo):
    """Junta párrafos completos hasta TAMANO_FRAGMENTO caracteres, sin partir ninguno;
    un párrafo más largo que eso se corta con trocear().
    Técnico: no viene del curso."""
    partes, actual = [], ""
    for parrafo in [p.strip() for p in cuerpo.split("\n\n") if p.strip()]:
        if len(parrafo) > TAMANO_FRAGMENTO:
            if actual:
                partes.append(actual)
                actual = ""
            partes.extend(trocear(parrafo))
        elif actual and len(actual) + len(parrafo) + 2 > TAMANO_FRAGMENTO:
            partes.append(actual)
            actual = parrafo
        else:
            actual = f"{actual}\n\n{parrafo}" if actual else parrafo
    if actual:
        partes.append(actual)
    return partes


def fragmentar_documento(texto):
    """Corta un documento en fragmentos: devuelve una lista de (sección, texto del fragmento).
    Cada texto empieza con "Título - Sección" para que se entienda aunque se lea solo.

    Curso: cada fragmento es una solución documentada que el agente puede citar
    (Módulo 2, sección 2.5). La forma de cortar es técnica (decisión D8).
    """
    inicio, *secciones = texto.split("\n## ")
    lineas = inicio.strip().split("\n")
    titulo = lineas[0].lstrip("# ").strip()
    # Lo que va antes de la primera sección, sin el título ni el aviso de documento ficticio.
    introduccion = "\n".join(l for l in lineas[1:] if not l.startswith(">")).strip()
    bloques = [("Introducción", introduccion)] if introduccion else []
    for seccion in secciones:
        encabezado, _, cuerpo = seccion.partition("\n")
        bloques.append((encabezado.strip(), cuerpo.strip()))

    fragmentos = []
    for nombre_seccion, cuerpo in bloques:
        partes = cortar_por_parrafos(cuerpo)
        for numero, parte in enumerate(partes, start=1):
            etiqueta = f"{nombre_seccion} (parte {numero} de {len(partes)})" if len(partes) > 1 else nombre_seccion
            fragmentos.append((etiqueta, f"{titulo} - {etiqueta}\n{parte}"))
    return fragmentos


def listar_documentos():
    """Devuelve los documentos de la base de conocimiento, en orden. El README.md de la carpeta
    explica los documentos; no es conocimiento del agente. Técnico: no viene del curso."""
    return [p for p in sorted(CARPETA_DOCUMENTOS.glob("*.md")) if p.name != "README.md"]


def cargar_conocimiento():
    """Lee cada documento, lo corta en fragmentos, calcula sus vectores y los guarda.

    Curso: prepara la base de conocimiento con las soluciones documentadas del
    agente (Módulo 2, sección 2.5). Es la parte de carga del RAG del proyecto.
    """
    faltan = config.faltan_variables(con_base_de_datos=True)
    if faltan:
        print(f"Faltan en src/docker/.env: {', '.join(faltan)}.")
        return
    documentos = listar_documentos()
    try:
        conexion = conectar()
    except Exception as error:  # PostgreSQL apagado, contraseña equivocada...
        print(f"No se pudo conectar con PostgreSQL ({error}). ¿Está abierto Docker y se ejecutó start-dev.bat?")
        return
    try:
        borrar_fragmentos(conexion)
        total = 0
        for documento in documentos:
            # utf-8-sig: lee igual un archivo guardado con BOM, la marca que agregan algunos editores.
            contenido = documento.read_text(encoding="utf-8-sig")
            fragmentos = fragmentar_documento(contenido)
            if not fragmentos:
                print(f"{documento.name}: sin contenido, se omite.")
                continue
            # La huella cambia si cambia una sola letra: dice qué versión del documento está cargada.
            huella = hashlib.sha256(contenido.encode("utf-8")).hexdigest()
            vectores = crear_embedding([texto for _, texto in fragmentos])
            for orden, ((seccion, texto), vector) in enumerate(zip(fragmentos, vectores)):
                guardar_fragmento(conexion, documento.name, seccion, orden, texto, vector, huella)
            total += len(fragmentos)
            print(f"{documento.name}: {len(fragmentos)} fragmento(s), huella {huella[:12]}")
        conexion.commit()  # se guarda todo junto: si algo falla a mitad, no queda una carga a medias
        print(f"Listo: {len(documentos)} documentos, {total} fragmentos, modelo {config.LLM_MODELO_EMBEDDINGS}.")
    except Exception as error:  # sin red, clave inválida, límite de uso del modelo...
        conexion.rollback()
        print(f"La carga se detuvo y no se guardó nada; la base quedó como estaba. Motivo: {error}")
    finally:
        conexion.close()


if __name__ == "__main__":
    cargar_conocimiento()
