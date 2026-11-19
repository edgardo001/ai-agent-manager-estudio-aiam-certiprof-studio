"""Genera estudio/indice.md: el índice cruzado de todo el material de estudio.

Uso (desde la raíz del repositorio o desde estudio/):
    python -X utf8 estudio/scripts/generar-indice.py

Busca cada tema de TEMAS en los módulos del curso, los resúmenes, los apuntes,
el glosario, las preguntas frecuentes, las plantillas, los diagramas y el
proyecto de agente, y escribe dónde aparece, con enlaces a la sección exacta.
Además arma un mapa por módulo con lo que cita cada sección. No se edita
indice.md a mano: se agregan o ajustan temas aquí y se vuelve a ejecutar.
"""
import io
import pathlib
import re
import unicodedata

# Este script vive en estudio/scripts/; BASE es la carpeta estudio/.
BASE = pathlib.Path(__file__).resolve().parents[1]

# Tema: expresión regular (sin distinguir mayúsculas). Mantener en español,
# con los términos del curso y sus equivalentes en inglés.
TEMAS = {
    "Accountability (rendición de cuentas)": r"accountability",
    "Adopción y gestión del cambio": r"gesti[oó]n del cambio|niveles de adopci[oó]n|resistencia",
    "Agent sprawl": r"agent sprawl",
    "Embeddings y pgvector (búsqueda semántica)": r"embedding|pgvector|b[uú]squeda (sem[aá]ntica|vectorial)",
    "Anonimización y datos personales": r"anonimiz|seudonimiz|datos (personales|sensibles)",
    "Rol del AI Agent Manager": r"nuevo rol|rol en evoluci|futuro del ai agent manager|qu[eé] es un ai agent manager",
    "AI Productivity Paradox": r"productivity paradox",
    "Alucinaciones": r"alucinaci",
    "Arquitectura técnica del agente (Docker, Gemini, OpenRouter)": r"docker|contenedor|gemini|openrouter|orquestador",
    "Audit trail (registro de auditoría)": r"audit trail|audit_log",
    "Behavioral drift (deriva de comportamiento)": r"behavioral drift|deriva de comportamiento|scope drift",
    "Boundary testing (pruebas de límites)": r"boundary testing|validaci[oó]n de l[ií]mites",
    "Business case (caso de negocio)": r"business case",
    "C-suite (alta dirección)": r"c-suite|alta direcci[oó]n",
    "Caso Accenture": r"accenture",
    "Caso JPMorgan Chase": r"jpmorgan",
    "Caso Klarna": r"klarna",
    "Caso Salesforce Agentforce": r"salesforce|agentforce",
    "Caso UPS ORION": r"\borion\b",
    "Chatbot frente a agente": r"chatbot",
    "Competencias del AI Agent Manager": r"seis competencias|6 competencias|competencias del ai agent manager",
    "Criterios de aceptación y validación previa a producción": r"criterios de aceptaci[oó]n|dimensiones de validaci[oó]n|cinco filtros|5 filtros",
    "CSAT (satisfacción del cliente)": r"\bcsat\b",
    "Dashboard (tablero de supervisión)": r"dashboard",
    "Equipo híbrido": r"equipos? h[ií]bridos?",
    "Escalamiento a una persona": r"escalamiento|escalar a",
    "Fallos silenciosos": r"fallos? silencios|errores silenciosos|silent error",
    "Framework de intervención": r"framework de intervenci[oó]n|intervenir",
    "Governance Board Agentic (junta de gobierno)": r"governance board|junta de gobierno",
    "Identidad del agente: los seis parámetros": r"seis par[aá]metros|6 par[aá]metros|identidad del agente",
    "Instrucciones del agente: JD+SOP y system prompt": r"jd\s?\+\s?sop|job description|\bsop\b|system prompt",
    "Kill switch y circuit breaker": r"kill switch|kill-switch|circuit breaker",
    "OWASP y seguridad": r"owasp",
    "Línea base (baseline)": r"l[ií]nea base|baseline",
    "Madurez agentic organizacional": r"madurez",
    "Método AIAM de rediseño en 5 pasos": r"5 pasos|cinco pasos|redise[ñn]o de procesos?",
    "Métricas y KPI": r"\bkpis?\b|m[eé]tricas de (negocio|[eé]xito|valor)",
    "n8n (analogía de flujo)": r"\bn8n\b",
    "Niveles de autonomía": r"niveles? de autonom[ií]a",
    "Nuevos roles del equipo híbrido": r"nuevos roles|roles del equipo",
    "Onboarding agentic": r"onboarding",
    "Permisos mínimos (least-privilege)": r"permisos m[ií]nimos|least-privilege",
    "ROI (retorno de la inversión)": r"\broi\b",
    "RAG (generación aumentada por recuperación)": r"\brag\b|generaci[oó]n aumentada",
    "RPA (automatización robótica de procesos)": r"\brpa\b",
    "Registro de agentes": r"registro (centralizado )?de agentes|agent_registry",
    "Seguridad y riesgo": r"seguridad|matriz de riesgos|ataque adversarial|adversarial",
    "Supervisión del agente": r"supervisi[oó]n",
    "Taxonomía de tareas": r"taxonom[ií]a",
    "Tres horizontes de valor": r"horizontes?",
    "Vendor (proveedor)": r"\bvendors?\b",
    "Fuente: Gartner": r"gartner",
    "Fuente: Harvard Business Review (HBR)": r"\bhbr\b|harvard business review",
    "Fuente: McKinsey": r"mckinsey",
    "Fuente: MIT, MIT Sloan y BCG": r"\bmit\b|\bbcg\b",
    "Fuente: PwC": r"\bpwc\b",
}


def leer(p):
    return io.open(p, encoding="utf-8").read()


def slug(titulo):
    """Ancla de encabezado al estilo de GitHub."""
    t = titulo.strip().lower()
    t = re.sub(r"[^\w\- ]", "", t)
    return t.replace(" ", "-")


def orden(t):
    t = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def sin_html(s):
    s = re.sub(r"<style.*?</style>|<script.*?</script>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s)


# ---------- Fuentes ----------
MODULOS = sorted((BASE / "modulos").glob("modulo-*.md"))
RESUMENES = sorted((BASE / "resumenes").glob("resumen-modulo-*.md"))
PLANTILLAS = [q for q in sorted((BASE / "plantillas").glob("[0-9][0-9]-*.md")) if not q.name.startswith("00")]
APUNTES = sorted((BASE / "apuntes" / "fuente").glob("apuntes-m*.html"))


def num_modulo(p):
    return int(re.search(r"(?:modulo-|-m)(\d)", p.stem).group(1))


def secciones_modulo(p):
    """Lista de (etiqueta, titulo, ancla, texto) por cada encabezado ### del módulo."""
    m = num_modulo(p)
    out, actual, buf = [], None, []
    for linea in leer(p).split("\n"):
        if linea.startswith("### "):
            if actual:
                out.append(actual + ("\n".join(buf),))
            titulo = linea[4:]
            n = re.match(r"(\d\.\d)\s", titulo)
            if n:
                etiqueta = n.group(1)
            else:
                corto = re.sub(r"[:,].*", "", titulo)
                corto = {"AI Agent Manager": "Responsabilidades"}.get(corto, corto)
                if corto.startswith("Responsabilidades"):
                    corto = "Responsabilidades"
                etiqueta = f"M{m} {corto}"
            actual, buf = (etiqueta, titulo, slug(titulo)), []
        elif actual:
            buf.append(linea)
    if actual:
        out.append(actual + ("\n".join(buf),))
    return out


def entradas(p):
    """(titulo, ancla, texto) por cada encabezado ## de un archivo Markdown."""
    partes = re.split(r"\n(?=## )", leer(p))[1:]
    return [(x.split("\n", 1)[0][3:].strip(), slug(x.split("\n", 1)[0][3:]), x) for x in partes]


def titulo_plantilla(p):
    return leer(p).split("\n", 1)[0].lstrip("# ").strip()


def base_plantilla(p):
    m = re.search(r"Base en el curso:\*\*(.*)", leer(p))
    return m.group(1) if m else ""


def rel(p):
    return p.relative_to(BASE).as_posix()


GLOSARIO = entradas(BASE / "glosario.md")
PREGUNTAS = entradas(BASE / "preguntas-frecuentes.md")
DIAGRAMAS = entradas(BASE / "diagramas.md")
PROYECTO_ARCH = sorted((BASE / "proyecto-agente" / "agente-soporte-n1" / "docs").glob("*.md"))
PROYECTO = [(t, a, x, rel(p)) for p in PROYECTO_ARCH for t, a, x in entradas(p)]
SECCIONES = {num_modulo(p): (p, secciones_modulo(p)) for p in MODULOS}
NUM_SEC = re.compile(r"(?<![\d.,])([1-5]\.[1-9])(?![\d])")


def link(texto, archivo, ancla=None):
    return f"[{texto}]({archivo}{'#' + ancla if ancla else ''})"


# ---------- Mapa por módulo ----------
def citas(texto):
    return set(NUM_SEC.findall(texto))


def mapa_modulos():
    L = ["## Mapa por módulo", "",
         "Para cada sección del curso: qué entradas del glosario, preguntas frecuentes, plantillas, diagramas y secciones del proyecto de agente (P1, P2…, numeradas como en la lista de archivos) la citan. Cada módulo tiene además su resumen y sus apuntes impresos, que cubren todas sus secciones numeradas.", ""]
    cit_glo = {t: citas(x) for t, a, x in GLOSARIO}
    cit_faq = {t: citas(x) for t, a, x in PREGUNTAS}
    cit_dia = {t: citas(x.split("```")[0]) for t, a, x in DIAGRAMAS}
    cit_pro = {t: citas(x.split("```")[0]) for t, a, x, f in PROYECTO}
    cit_pla = {p: citas(base_plantilla(p)) for p in PLANTILLAS}
    for m, (p, secs) in sorted(SECCIONES.items()):
        titulo = leer(p).split("\n## ", 1)[-1].split("\n", 1)[0] if m == 1 else leer(p).split("\n", 1)[0][3:]
        res = [r for r in RESUMENES if num_modulo(r) == m]
        L += [f"### {titulo}", "",
              f"Módulo completo: {link(p.name, rel(p))}. Resumen: {link(res[0].name, rel(res[0])) if res else 'no hay'}. Apuntes impresos: {link(f'apuntes-modulo-{m}.pdf', f'apuntes/apuntes-modulo-{m}.pdf')}.", "",
              "| Sección | Glosario | Preguntas frecuentes | Plantillas | Diagramas | Proyecto |", "|---|---|---|---|---|---|"]
        for etq, tit, ancla, _ in secs:
            if not re.match(r"\d\.\d", etq):
                continue
            g = ", ".join(link(t, "glosario.md", a) for t, a, _ in GLOSARIO if etq in cit_glo[t])
            f = ", ".join(link(t, "preguntas-frecuentes.md", a) for t, a, _ in PREGUNTAS if etq in cit_faq[t])
            pl = ", ".join(link(q.name[:2], rel(q)) for q in PLANTILLAS if etq in cit_pla[q])
            d = ", ".join(link(str(i + 1), "diagramas.md", a) for i, (t, a, _) in enumerate(DIAGRAMAS) if etq in cit_dia[t])
            pr = ", ".join(link(f"P{i + 1}", f, a) for i, (t, a, _, f) in enumerate(PROYECTO) if etq in cit_pro[t])
            L.append(f"| {link(tit, rel(p), ancla)} | {g or '·'} | {f or '·'} | {pl or '·'} | {d or '·'} | {pr or '·'} |")
        L.append("")
    return L


# ---------- Temas de la A a la Z ----------
def temas():
    L = ["## Temas de la A a la Z", "",
         "Para cada tema: las secciones del curso donde aparece y los demás archivos que lo tratan. “Preguntas” son las preguntas de validación del módulo.", ""]
    for tema in sorted(TEMAS, key=orden):
        rx = re.compile(TEMAS[tema], re.I)
        filas = []
        curso = []
        for m, (p, secs) in sorted(SECCIONES.items()):
            for etq, tit, ancla, txt in secs:
                if rx.search(tit) or rx.search(txt):
                    etq = re.sub(r"^M\d Preguntas de validación$", f"M{m} Preguntas", etq)
                    curso.append(link(etq, rel(p), ancla))
        if curso:
            filas.append("- **Curso:** " + ", ".join(curso))
        res = [link(f"M{num_modulo(r)}", rel(r)) for r in RESUMENES if rx.search(leer(r))]
        if res:
            filas.append("- **Resúmenes:** " + ", ".join(res))
        apu = [link(f"M{num_modulo(a)}", f"apuntes/apuntes-modulo-{num_modulo(a)}.pdf") for a in APUNTES if rx.search(sin_html(leer(a)))]
        if apu:
            filas.append("- **Apuntes:** " + ", ".join(apu))
        for nombre, archivo, lista in (("Glosario", "glosario.md", GLOSARIO), ("Preguntas frecuentes", "preguntas-frecuentes.md", PREGUNTAS)):
            # Primero las entradas cuyo título nombra el tema; luego las que solo lo mencionan.
            tit = [link(t, archivo, a) for t, a, x in lista if rx.search(t)]
            men = [link(t, archivo, a) for t, a, x in lista if not rx.search(t) and rx.search(x)]
            if tit or men:
                filas.append(f"- **{nombre}:** " + ", ".join(tit + men))
        pla = [link(titulo_plantilla(q), rel(q)) for q in PLANTILLAS if rx.search(leer(q))]
        if pla:
            filas.append("- **Plantillas:** " + ", ".join(pla))
        dia = [link(t, "diagramas.md", a) for t, a, x in DIAGRAMAS if rx.search(x)]
        if dia:
            filas.append("- **Diagramas:** " + ", ".join(dia))
        pro = [link(t, f, a) for t, a, x, f in PROYECTO if rx.search(x)]
        if pro:
            filas.append("- **Proyecto de agente:** " + ", ".join(pro))
        if filas:
            L += [f"### {tema}", ""] + filas + [""]
    return L


def main():
    L = ["# Índice cruzado del material de estudio", "",
         "Este archivo conecta todo el material de `estudio/`: los módulos del curso, los resúmenes, los apuntes, el glosario, las preguntas frecuentes, las plantillas, los diagramas y el proyecto de agente. Sirve para encontrar rápido dónde se trata un tema, a mano o cuando el agente responde una pregunta.", "",
         "No se edita a mano: lo genera `estudio/scripts/generar-indice.py`, que se vuelve a ejecutar después de cada cambio en `estudio/` (`python -X utf8 estudio/scripts/generar-indice.py`). Para agregar un tema, se agrega a la lista `TEMAS` del script.", "",
         "Es un archivo de navegación, no de estudio: por eso usa listas y tablas, a diferencia del resto del material.", "",
         "## Archivos", "",
         f"- **Curso, un archivo por módulo:** " + ", ".join(link(f"Módulo {num_modulo(p)}", rel(p)) for p in MODULOS),
         f"- **Resúmenes:** " + ", ".join(link(f"Módulo {num_modulo(r)}", rel(r)) for r in RESUMENES),
         f"- **Apuntes impresos:** " + ", ".join(link(f"Módulo {num_modulo(a)}", f"apuntes/apuntes-modulo-{num_modulo(a)}.pdf") for a in APUNTES) + ", y " + link("todos juntos", "apuntes/apuntes-completos.pdf"),
         f"- **Glosario ({len(GLOSARIO)} términos):** " + ", ".join(link(t, "glosario.md", a) for t, a, _ in GLOSARIO),
         f"- **Preguntas frecuentes ({len(PREGUNTAS)}):** " + ", ".join(link(t, "preguntas-frecuentes.md", a) for t, a, _ in PREGUNTAS),
         f"- **Plantillas ({len(PLANTILLAS)}), con su " + link("guía de uso", "plantillas/00-guia.md") + "):** " + ", ".join(link(titulo_plantilla(q), rel(q)) for q in PLANTILLAS),
         f"- **Diagramas del curso ({len(DIAGRAMAS)}):** " + ", ".join(link(f"{i + 1}. {t}", "diagramas.md", a) for i, (t, a, _) in enumerate(DIAGRAMAS)),
         f"- **Proyecto de agente (" + ", ".join(link(p.name, rel(p)) for p in PROYECTO_ARCH) + "):** " + ", ".join(link(f"P{i + 1}. {t}", f, a) for i, (t, a, _, f) in enumerate(PROYECTO)),
         ""]
    L += mapa_modulos() + temas()
    io.open(BASE / "indice.md", "w", encoding="utf-8", newline="").write("\n".join(L).rstrip("\n") + "\n")
    print("indice.md:", len(L), "líneas,", len(TEMAS), "temas")


if __name__ == "__main__":
    main()
