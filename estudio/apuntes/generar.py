"""Genera los PDF de los apuntes visuales AIAM™.

Uso:
    python estudio/apuntes/generar.py            # todos los módulos + el PDF completo
    python estudio/apuntes/generar.py --modulo 2 # solo un módulo (para probar)
    python estudio/apuntes/generar.py --modulo 2 --png carpeta  # además, una imagen por hoja

Lee fuente/apuntes-mN.html (una hoja A4 por cada <div class="pag mN">) y crea
apuntes-modulo-N.pdf. Sin --modulo, crea también apuntes-completos.pdf con los
cinco módulos seguidos. Informa las hojas cuyo contenido no cabe en la página.

Necesita Google Chrome o Microsoft Edge. Para --png necesita pypdfium2.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FUENTE = AQUI / "fuente"

NAVEGADORES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
]

REVISION = """<script>
window.addEventListener('load', () => setTimeout(() => {
  const malas = [...document.querySelectorAll('.pag')].map((p, i) =>
    (p.scrollHeight > p.clientHeight + 1 || p.scrollWidth > p.clientWidth + 1) ? i + 1 : 0).filter(Boolean);
  document.body.setAttribute('data-desborde', malas.join(','));
  document.body.setAttribute('data-revisado', '1');
}, 1500));
</script>"""


def navegador():
    """Devuelve la ruta de Chrome o Edge."""
    for ruta in NAVEGADORES:
        if os.path.exists(ruta):
            return ruta
    sys.exit("No encontré Chrome ni Edge. Instale uno de los dos.")


def cuerpo(html):
    """Extrae el contenido de <body> de un archivo de apuntes."""
    return re.search(r"<body[^>]*>(.*)</body>", html, re.S).group(1)


def documento(titulo, cuerpos):
    """Arma un HTML completo con la cabecera común y los cuerpos dados."""
    css = (FUENTE / "apuntes.css").read_text(encoding="utf-8")
    return ("<!doctype html><html lang=\"es\"><head><meta charset=\"utf-8\">"
            f"<title>{titulo}</title>"
            "<link href=\"https://fonts.googleapis.com/css2?family=Caveat:wght@500;700"
            "&family=Inter:wght@400;600;800&display=swap\" rel=\"stylesheet\">"
            f"<style>{css}</style></head><body>" + "\n".join(cuerpos) + "</body></html>")


def ejecutar(nav, html, *argumentos):
    """Abre el HTML en el navegador sin ventana y devuelve su salida."""
    with tempfile.TemporaryDirectory() as tmp:
        archivo = Path(tmp) / "apuntes.html"
        archivo.write_text(html, encoding="utf-8")
        return subprocess.run([nav, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                               "--virtual-time-budget=10000", *argumentos, archivo.as_uri()],
                              capture_output=True, text=True, encoding="utf-8", check=False)


def generar(nav, titulo, cuerpos, destino):
    """Crea el PDF y devuelve cuántas hojas se desbordan."""
    ejecutar(nav, documento(titulo, cuerpos), f"--print-to-pdf={destino}")
    salida = ejecutar(nav, documento(titulo, cuerpos) + REVISION,
                      "--window-size=794,1123", "--dump-dom").stdout
    revisado = re.search(r'data-desborde="([^"]*)"', salida)
    if not revisado or 'data-revisado="1"' not in salida:
        print(f"  No se pudo revisar el desborde de {destino.name}.")
        return 0
    malas = [x for x in revisado.group(1).split(",") if x]
    for hoja in malas:
        print(f"  DESBORDE en {destino.name}: hoja {hoja}")
    return len(malas)


def imagenes(pdf, carpeta):
    """Guarda una imagen PNG por hoja del PDF."""
    import pypdfium2  # pylint: disable=import-outside-toplevel
    carpeta.mkdir(parents=True, exist_ok=True)
    doc = pypdfium2.PdfDocument(str(pdf))
    for i in range(len(doc)):
        doc[i].render(scale=1.4).to_pil().save(carpeta / f"{pdf.stem}-hoja-{i + 1}.png")
    paginas = len(doc)
    doc.close()
    print(f"  {paginas} imágenes en {carpeta}")


def main():
    """Punto de entrada."""
    ap = argparse.ArgumentParser(description="Genera los PDF de los apuntes visuales.")
    ap.add_argument("--modulo", type=int, help="solo este módulo")
    ap.add_argument("--png", type=Path, help="carpeta donde guardar una imagen por hoja")
    args = ap.parse_args()

    nav = navegador()
    modulos = [args.modulo] if args.modulo else range(1, 6)
    errores, todos = 0, []
    for n in modulos:
        fuente = FUENTE / f"apuntes-m{n}.html"
        if not fuente.exists():
            print(f"Falta {fuente.name}; se omite.")
            continue
        c = cuerpo(fuente.read_text(encoding="utf-8"))
        todos.append(c)
        destino = AQUI / f"apuntes-modulo-{n}.pdf"
        errores += generar(nav, f"Apuntes AIAM: Módulo {n}", [c], destino)
        print(f"{destino.name} listo.")
        if args.png:
            imagenes(destino, args.png)
    if not args.modulo and len(todos) > 1:
        destino = AQUI / "apuntes-completos.pdf"
        errores += generar(nav, "Apuntes AIAM", todos, destino)
        print(f"{destino.name} listo ({len(todos)} módulos).")
    print("Sin desbordes." if not errores else f"{errores} hoja(s) con contenido que no cabe.")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
