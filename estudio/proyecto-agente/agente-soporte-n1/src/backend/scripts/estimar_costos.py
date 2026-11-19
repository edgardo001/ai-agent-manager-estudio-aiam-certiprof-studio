"""Script de asistencia: estima cuánto cuestan los embeddings y las consultas, sin llamar al modelo (es gratis).

Uso, desde la carpeta src/backend con el entorno virtual activo:
    python -m scripts.estimar_costos
    python -m scripts.estimar_costos --documentos 1000 --caracteres 20000
    python -m scripts.estimar_costos --consultas 50 300 1000 --hora-pico 20
Sin argumentos, mide los documentos reales de src/base-de-conocimiento/.
Las cifras son estimaciones: los supuestos y cómo afinarlos están en docs/costos.md.
"""
import argparse

from aplicacion import config
from scripts.cargar_conocimiento import CARPETA_DOCUMENTOS, fragmentar_documento

# Supuestos de la estimación (docs/costos.md). Desde la etapa 3, los tokens reales de
# cada ticket quedan en la tabla tickets y permiten reemplazar estos supuestos.
CARACTERES_POR_TOKEN = 4         # regla práctica; en español suele haber algo más de tokens
TOKENS_HERRAMIENTAS = 300        # la descripción de las tres herramientas, que va en cada llamada
CARACTERES_PREGUNTA = 200        # largo típico del mensaje de un cliente
FRAGMENTOS_POR_BUSQUEDA = 5      # los que entrega buscar_fragmentos()
TOKENS_SALIDA_POR_CONSULTA = 300 # lo que escribe el modelo: decisiones de herramientas y la respuesta
DIAS_POR_MES = 30


def tokens(caracteres):
    """Convierte caracteres en tokens aproximados.
    Técnico: no viene del curso."""
    return caracteres / CARACTERES_POR_TOKEN


def numero(valor, decimales=0):
    """Escribe un número a la manera del español: 1.234,5 (punto de miles y coma decimal).
    Técnico: no viene del curso."""
    return f"{valor:,.{decimales}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def dolares(valor):
    """Escribe un monto en dólares, con más decimales si es muy pequeño.
    Técnico: no viene del curso."""
    return f"{numero(valor, 6 if valor < 0.01 else 2)} dólares"


def medir_base_de_conocimiento():
    """Cuenta los documentos y los caracteres de los fragmentos reales.
    Técnico: no viene del curso."""
    documentos = [p for p in sorted(CARPETA_DOCUMENTOS.glob("*.md")) if p.name != "README.md"]
    fragmentos = [texto for p in documentos for _, texto in fragmentar_documento(p.read_text(encoding="utf-8-sig"))]
    return len(documentos), len(fragmentos), sum(len(texto) for texto in fragmentos)


def estimar_embeddings(caracteres):
    """Costo de calcular los embeddings de una carga completa: solo tokens de entrada.

    Curso: parte del costo por caso y del valor que mide el dashboard
    (Módulo 3, sección 3.2, y Módulo 5). El cálculo es técnico.
    """
    return tokens(caracteres) * config.PRECIO_MILLON_TOKENS_EMBEDDINGS / 1_000_000


def estimar_consulta(caracteres_fragmento):
    """Tokens y costo de una consulta del cliente: el embedding de la pregunta más las
    llamadas al modelo de chat. Cada llamada reenvía el prompt, las herramientas y la
    pregunta; los fragmentos encontrados se envían al menos una vez.

    Curso: costo por caso (Módulo 3, sección 3.2) y ROI (Módulo 5).
    """
    base = tokens(len(config.RUTA_PROMPT.read_text(encoding="utf-8"))) + TOKENS_HERRAMIENTAS + tokens(CARACTERES_PREGUNTA)
    entrada = config.LLAMADAS_POR_CONSULTA * base + FRAGMENTOS_POR_BUSQUEDA * tokens(caracteres_fragmento)
    costo = (tokens(CARACTERES_PREGUNTA) * config.PRECIO_MILLON_TOKENS_EMBEDDINGS
             + entrada * config.PRECIO_MILLON_TOKENS_ENTRADA
             + TOKENS_SALIDA_POR_CONSULTA * config.PRECIO_MILLON_TOKENS_SALIDA) / 1_000_000
    return entrada, costo


def estimar_costos():
    """Muestra las tres estimaciones: la carga de documentos, cada consulta y los escenarios
    de uso por día y por mes, con el pico de uso frente al límite del proveedor.
    Técnico: no viene del curso."""
    parser = argparse.ArgumentParser(description="Estima costos sin llamar al modelo.")
    parser.add_argument("--documentos", type=int, help="cantidad de documentos de un caso hipotético")
    parser.add_argument("--caracteres", type=int, help="caracteres promedio por documento del caso hipotético")
    parser.add_argument("--consultas", type=int, nargs=3, default=[50, 300, 1000],
                        metavar=("BAJA", "ESPERADA", "ALTA"), help="consultas por día en tres escenarios")
    parser.add_argument("--hora-pico", type=float, default=20,
                        help="porcentaje de las consultas del día que llegan en la hora más cargada")
    argumentos = parser.parse_args()

    documentos, fragmentos, caracteres = medir_base_de_conocimiento()
    caracteres_fragmento = caracteres / fragmentos
    print(f"Precios del .env, en dólares por millón de tokens: embeddings {numero(config.PRECIO_MILLON_TOKENS_EMBEDDINGS, 2)}, "
          f"chat {numero(config.PRECIO_MILLON_TOKENS_ENTRADA, 2)} de entrada y {numero(config.PRECIO_MILLON_TOKENS_SALIDA, 2)} de salida.")

    print("\n1. Embeddings de una carga completa (se paga de nuevo en cada recarga)")
    print(f"   Base de conocimiento actual: {documentos} documentos, {fragmentos} fragmentos, {numero(caracteres)} caracteres,"
          f" unos {numero(tokens(caracteres))} tokens: {dolares(estimar_embeddings(caracteres))}.")
    if argumentos.documentos and argumentos.caracteres:
        total = argumentos.documentos * argumentos.caracteres
        print(f"   Caso hipotético: {numero(argumentos.documentos)} documentos de {numero(argumentos.caracteres)} caracteres,"
              f" unos {numero(tokens(total))} tokens: {dolares(estimar_embeddings(total))}.")

    entrada, costo = estimar_consulta(caracteres_fragmento)
    print("\n2. Una consulta del cliente")
    print(f"   {config.LLAMADAS_POR_CONSULTA} llamadas al modelo, unos {numero(entrada)} tokens de entrada y "
          f"{TOKENS_SALIDA_POR_CONSULTA} de salida: {dolares(costo)} por consulta.")

    print("\n3. Escenarios de uso")
    for nombre, por_dia in zip(("baja", "esperada", "alta"), argumentos.consultas):
        print(f"   Demanda {nombre}: {numero(por_dia)} consultas al día: {dolares(por_dia * costo)} al día,"
              f" {dolares(por_dia * costo * DIAS_POR_MES)} al mes.")

    pico = max(argumentos.consultas) * argumentos.hora_pico / 100 / 60
    llamadas = pico * config.LLAMADAS_POR_CONSULTA
    print(f"\n   Pico, con la demanda alta y el {argumentos.hora_pico:g}% en una hora: {numero(pico, 1)} consultas por minuto,"
          f" {numero(llamadas, 1)} llamadas al modelo por minuto.")
    print("   El pico no cambia el costo, que depende del total; sí puede chocar con el límite de uso del proveedor.")
    if config.LIMITE_LLAMADAS_POR_MINUTO:
        estado = "dentro del límite" if llamadas <= config.LIMITE_LLAMADAS_POR_MINUTO else "SOBRE el límite: habría esperas o errores"
        print(f"   Límite de la cuenta: {numero(config.LIMITE_LLAMADAS_POR_MINUTO)} llamadas por minuto: {estado}.")
    else:
        print("   Anote LIMITE_LLAMADAS_POR_MINUTO en el .env (sale de Google AI Studio) para compararlo.")


if __name__ == "__main__":
    estimar_costos()
