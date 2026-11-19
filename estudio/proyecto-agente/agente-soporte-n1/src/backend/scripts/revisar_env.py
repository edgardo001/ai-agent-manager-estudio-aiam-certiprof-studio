"""Script de asistencia: compara src/docker/.env con la plantilla src/docker/example.env.

Uso, desde la carpeta src/backend:
    python -m scripts.revisar_env             dice qué variables faltan o sobran en el .env
    python -m scripts.revisar_env --ordenar   reescribe el .env con el orden y los comentarios de
                                              la plantilla, conservando sus valores; guarda antes
                                              una copia en src/docker/.env.respaldo
start-dev.bat lo ejecuta al empezar, solo para avisar. Nunca muestra los valores: el .env
tiene claves (decisión D14).
"""
import argparse
import re
import shutil
from pathlib import Path

# src/backend/scripts/revisar_env.py -> src/docker/
CARPETA_DOCKER = Path(__file__).resolve().parents[2] / "docker"
RUTA_ENV = CARPETA_DOCKER / ".env"
RUTA_PLANTILLA = CARPETA_DOCKER / "example.env"
RUTA_RESPALDO = CARPETA_DOCKER / ".env.respaldo"
VARIABLE = re.compile(r"^([A-Z][A-Z0-9_]*)=(.*)$")


def leer_variables(texto):
    """Devuelve las variables activas (no comentadas) de un texto, en orden: {nombre: valor}.
    Técnico: no viene del curso."""
    variables = {}
    for linea in texto.splitlines():
        coincide = VARIABLE.match(linea.strip())
        if coincide:
            variables[coincide.group(1)] = coincide.group(2)
    return variables


def comparar(plantilla, env):
    """Devuelve (las que faltan en el .env, las que sobran en el .env), por nombre.
    Técnico: no viene del curso."""
    return [n for n in plantilla if n not in env], [n for n in env if n not in plantilla]


def ordenar(texto_plantilla, env):
    """Arma el nuevo .env: las líneas de la plantilla, con los valores del .env donde existan
    y los de la plantilla donde falten; al final, las variables del .env que la plantilla no
    tiene, para no perder ninguna. Técnico: no viene del curso."""
    lineas = []
    for linea in texto_plantilla.splitlines():
        coincide = VARIABLE.match(linea.strip())
        if coincide and coincide.group(1) in env:
            linea = f"{coincide.group(1)}={env[coincide.group(1)]}"
        lineas.append(linea)
    _, sobran = comparar(leer_variables(texto_plantilla), env)
    if sobran:
        lineas += ["", "# --- Variables de este .env que la plantilla no tiene: revise si siguen sirviendo ---"]
        lineas += [f"{nombre}={env[nombre]}" for nombre in sobran]
    return "\n".join(lineas) + "\n"


def revisar_env():
    """Muestra las diferencias de nombres y, con --ordenar, reescribe el .env.
    Técnico: no viene del curso."""
    parser = argparse.ArgumentParser(description="Compara el .env con example.env.")
    parser.add_argument("--ordenar", action="store_true", help="reescribe el .env con el orden de la plantilla")
    ordenar_env = parser.parse_args().ordenar

    if not RUTA_ENV.exists():
        print("No existe src/docker/.env: copie example.env como .env y complételo.")
        return
    texto_plantilla = RUTA_PLANTILLA.read_text(encoding="utf-8-sig")
    plantilla, env = leer_variables(texto_plantilla), leer_variables(RUTA_ENV.read_text(encoding="utf-8-sig"))
    faltan, sobran = comparar(plantilla, env)
    if ordenar_env:
        shutil.copyfile(RUTA_ENV, RUTA_RESPALDO)
        RUTA_ENV.write_text(ordenar(texto_plantilla, env), encoding="utf-8", newline="\n")
        print(f"Listo: .env ordenado como la plantilla. Agregadas con su valor de ejemplo: {', '.join(faltan) or 'ninguna'}."
              f" Al final, sin borrar: {', '.join(sobran) or 'ninguna'}. Copia anterior en src/docker/.env.respaldo.")
        return
    if not faltan and not sobran:
        print(".env al día con example.env.")
        return
    if faltan:
        print(f"Aviso: al .env le faltan variables de example.env (se usan sus valores por defecto): {', '.join(faltan)}.")
    if sobran:
        print(f"Aviso: el .env tiene variables que example.env ya no tiene: {', '.join(sobran)}.")
    print("Para ordenarlo, desde src/backend: python -m scripts.revisar_env --ordenar")


if __name__ == "__main__":
    revisar_env()
