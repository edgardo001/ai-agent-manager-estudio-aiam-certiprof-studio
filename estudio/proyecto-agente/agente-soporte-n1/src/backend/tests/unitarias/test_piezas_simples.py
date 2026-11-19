"""Pruebas unitarias de piezas pequeñas, sin red ni base de datos: configuración, costos, vectores,
instrucciones del agente, corte de documentos y la revisión del archivo de configuración local."""
from aplicacion import config
from aplicacion.agente import armar_conversacion, armar_instrucciones, leer_version_prompt
from aplicacion.base_de_datos import vector_a_texto
from aplicacion.modelo import calcular_costo
from scripts.cargar_conocimiento import SOLAPE, TAMANO_FRAGMENTO, cortar_por_parrafos, fragmentar_documento, trocear
from scripts.revisar_env import comparar, leer_variables, ordenar


# --- Configuración y costos ---

def test_faltan_variables_nombra_la_clave_del_proveedor_en_uso(monkeypatch):
    """Falta la clave del proveedor que se usa, no la de los otros; la contraseña, solo si se pide.
    Técnico: no viene del curso (decisión D14)."""
    monkeypatch.setattr(config, "LLM_PROVEEDOR", "openrouter")
    monkeypatch.setattr(config, "LLM_EMBEDDINGS_PROVEEDOR", "gemini")
    monkeypatch.setattr(config, "OPENROUTER_API_KEY", "")
    monkeypatch.setattr(config, "GEMINI_API_KEY", "clave")
    monkeypatch.setattr(config, "LLM_MODEL", "modelo")
    monkeypatch.setattr(config, "POSTGRES_PASSWORD", "")
    assert config.faltan_variables() == ["OPENROUTER_API_KEY"]
    assert config.faltan_variables(con_base_de_datos=True) == ["OPENROUTER_API_KEY", "POSTGRES_PASSWORD"]


def test_proveedores_desconocido_ollama_y_clave_propia(monkeypatch):
    """Un proveedor mal escrito se avisa con las opciones válidas; Ollama no pide clave; cada
    proveedor usa su dirección y la clave con su nombre. Técnico: no viene del curso (D14)."""
    monkeypatch.setattr(config, "LLM_PROVEEDOR", "gemnii")
    monkeypatch.setattr(config, "LLM_EMBEDDINGS_PROVEEDOR", "ollama")
    monkeypatch.setattr(config, "LLM_MODEL", "modelo")
    monkeypatch.setattr(config, "OPENROUTER_API_KEY", "clave-openrouter")
    assert config.faltan_variables() == ["LLM_PROVEEDOR (use gemini, openrouter, ollama)"]
    assert config.datos_del_proveedor("ollama")[1] == "ollama"
    assert config.datos_del_proveedor("gemnii") == (None, None)
    assert config.datos_del_proveedor("openrouter") == (config.PROVEEDORES["openrouter"][0], "clave-openrouter")


def test_calcular_costo_con_los_precios_del_env(monkeypatch):
    """Un millón de tokens de entrada y uno de salida cuestan la suma de los dos precios.
    Curso: costo por caso (Módulo 3, sección 3.2)."""
    monkeypatch.setattr(config, "PRECIO_MILLON_TOKENS_ENTRADA", 0.25)
    monkeypatch.setattr(config, "PRECIO_MILLON_TOKENS_SALIDA", 1.5)
    assert calcular_costo(1_000_000, 1_000_000) == 1.75
    assert calcular_costo(0, 0) == 0


def test_vector_a_texto():
    """El vector viaja como texto que PostgreSQL convierte con ::vector (decisión D2)."""
    assert vector_a_texto([0.5, -1, 2.25]) == "[0.5,-1,2.25]"


# --- Instrucciones del agente ---

def test_las_instrucciones_incluyen_lo_que_no_atiende():
    """El programa agrega al prompt la lista de lo que el agente no atiende, tomada del registro.
    Curso: el alcance, con lo que queda fuera (Módulo 2, sección 2.2), guardado en el registro de agentes (2.7)."""
    instrucciones = armar_instrucciones("Versión del prompt: 3\n# Rol", {"fuera_de_alcance": "Cancelaciones y reembolsos"})
    assert instrucciones.startswith("Versión del prompt: 3")
    assert instrucciones.rstrip().endswith("Cancelaciones y reembolsos.\nSi el caso es de esta lista, escala.")


def test_la_conversacion_marca_al_cliente_como_datos():
    """Lo que escribe el cliente va marcado como datos; lo del agente va tal cual.
    Curso: dimensión adversarial (Módulo 2, sección 2.6)."""
    conversacion = armar_conversacion("instrucciones", [("cliente", "hola"), ("agente", "¿en qué ayudo?")])
    assert conversacion[0] == {"role": "system", "content": "instrucciones"}
    assert conversacion[1] == {"role": "user", "content": "<mensaje_del_cliente>\nhola\n</mensaje_del_cliente>"}
    assert conversacion[2] == {"role": "assistant", "content": "¿en qué ayudo?"}


def test_leer_version_prompt():
    """La versión sale de la primera línea del prompt. Curso: cada versión se valida y se
    aprueba (Módulo 2, sección 2.6)."""
    assert leer_version_prompt("Versión del prompt: 3\n# Rol") == "3"
    assert leer_version_prompt("# Rol sin versión") == "sin versión"
    assert leer_version_prompt("") == "sin versión"


# --- Corte de documentos (scripts/cargar_conocimiento.py, decisión D8) ---

def test_trocear_corta_con_solape_y_sin_repetir_el_final():
    """Un texto que cabe en un fragmento no se corta; uno largo se corta en partes que repiten
    SOLAPE caracteres; y 2.100 caracteres dan 2 pedazos, no 3 (corrección de la etapa 2).
    Técnico: no viene del curso."""
    assert trocear("a" * TAMANO_FRAGMENTO) == ["a" * TAMANO_FRAGMENTO]
    pedazos = trocear("".join(str(i % 10) for i in range(2000)))
    assert len(pedazos) == 2 and pedazos[0][-SOLAPE:] == pedazos[1][:SOLAPE]
    assert len(trocear("a" * 2100)) == 2


def test_cortar_por_parrafos_no_parte_un_parrafo():
    """Los párrafos se juntan enteros hasta el tamaño máximo; ninguno queda partido. Técnico: no viene del curso."""
    partes = cortar_por_parrafos("\n\n".join(["p" * 700, "q" * 700, "r" * 100]))
    assert partes == ["p" * 700, "q" * 700 + "\n\n" + "r" * 100]


def test_fragmentar_documento_por_secciones_con_titulo():
    """Cada sección es un fragmento que empieza con "Título - Sección"; la introducción no incluye
    el aviso de documento ficticio; un documento sin contenido no da fragmentos. Técnico: no viene del curso."""
    texto = "# Cuenta bloqueada\n> Documento ficticio.\nIntro breve.\n## Pasos\n1. Esperar.\n## Si no funciona\nEscalar."
    fragmentos = fragmentar_documento(texto)
    assert [seccion for seccion, _ in fragmentos] == ["Introducción", "Pasos", "Si no funciona"]
    assert fragmentos[1][1] == "Cuenta bloqueada - Pasos\n1. Esperar."
    assert "ficticio" not in fragmentos[0][1]
    assert fragmentar_documento("# Título\n> Documento ficticio.\n") == []


# --- Revisión del archivo de configuración local (scripts/revisar_env.py, decisión D14) ---

PLANTILLA = "# Claves\nGEMINI_API_KEY=\n# Modelo\nLLM_PROVEEDOR=gemini\nLLM_MODEL=gemini-3.1-flash-lite\n"
LOCAL = "LLM_MODEL=otro\n# comentario viejo\nVIEJA=1\nGEMINI_API_KEY=secreta\n"


def test_revisar_compara_y_ordena_sin_perder_valores():
    """Dice qué falta y qué sobra, y al ordenar deja el orden y los comentarios de la plantilla con
    los valores propios; lo que falta toma el valor de ejemplo y lo que sobra queda al final.
    Técnico: no viene del curso."""
    assert comparar(leer_variables(PLANTILLA), leer_variables(LOCAL)) == (["LLM_PROVEEDOR"], ["VIEJA"])
    nuevo = ordenar(PLANTILLA, leer_variables(LOCAL))
    assert nuevo.startswith("# Claves\nGEMINI_API_KEY=secreta\n# Modelo\nLLM_PROVEEDOR=gemini\nLLM_MODEL=otro\n")
    assert nuevo.rstrip().endswith("VIEJA=1")
    assert leer_variables(nuevo) == {"GEMINI_API_KEY": "secreta", "LLM_PROVEEDOR": "gemini", "LLM_MODEL": "otro", "VIEJA": "1"}
