"""Pruebas unitarias de piezas pequeñas: configuración, costos, vectores e instrucciones del agente."""
from aplicacion import config
from aplicacion.agente import armar_conversacion, armar_instrucciones, leer_version_prompt
from aplicacion.base_de_datos import vector_a_texto
from aplicacion.modelo import calcular_costo


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


def test_un_proveedor_desconocido_se_avisa_y_ollama_no_pide_clave(monkeypatch):
    """Un proveedor mal escrito se avisa con las opciones válidas; Ollama no pide clave.
    Técnico: no viene del curso (decisión D14)."""
    monkeypatch.setattr(config, "LLM_PROVEEDOR", "gemnii")
    monkeypatch.setattr(config, "LLM_EMBEDDINGS_PROVEEDOR", "ollama")
    monkeypatch.setattr(config, "LLM_MODEL", "modelo")
    assert config.faltan_variables() == ["LLM_PROVEEDOR (use gemini, openrouter, ollama)"]
    assert config.datos_del_proveedor("ollama")[1] == "ollama"
    assert config.datos_del_proveedor("gemnii") == (None, None)


def test_cada_proveedor_usa_su_direccion_y_su_clave(monkeypatch):
    """Elegir el proveedor elige su dirección y la clave con su nombre. Técnico: no viene del curso (D14)."""
    monkeypatch.setattr(config, "OPENROUTER_API_KEY", "clave-openrouter")
    assert config.datos_del_proveedor("openrouter") == ("https://openrouter.ai/api/v1", "clave-openrouter")


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


def test_las_instrucciones_incluyen_lo_que_no_atiende():
    """El programa agrega al prompt la lista de lo que el agente no atiende, tomada del registro.
    Curso: el alcance, con lo que queda fuera (Módulo 2, sección 2.2), guardado en el registro de agentes (2.7)."""
    instrucciones = armar_instrucciones("Versión del prompt: 3\n# Rol", {"fuera_de_alcance": "Cancelaciones y reembolsos"})
    assert instrucciones.startswith("Versión del prompt: 3")
    assert instrucciones.rstrip().endswith("Cancelaciones y reembolsos.\nSi el caso es de esta lista, escala.")


def test_la_conversacion_marca_al_cliente_como_datos():
    """Lo que escribe el cliente va marcado como datos; lo del agente va tal cual.
    Curso: dimensión adversarial (Módulo 2, sección 2.6)."""
    conversacion = armar_conversacion("instrucciones", [("cliente", "hola"), ("agente", "¿en qué ayudo?"), ("persona", "ya lo veo")])
    assert conversacion[0] == {"role": "system", "content": "instrucciones"}
    assert conversacion[1] == {"role": "user", "content": "<mensaje_del_cliente>\nhola\n</mensaje_del_cliente>"}
    assert conversacion[2] == {"role": "assistant", "content": "¿en qué ayudo?"}
    assert conversacion[3] == {"role": "assistant", "content": "(Respondió una persona del equipo) ya lo veo"}


def test_leer_version_prompt():
    """La versión sale de la primera línea del prompt. Curso: cada versión se valida y se
    aprueba (Módulo 2, sección 2.6)."""
    assert leer_version_prompt("Versión del prompt: 3\n# Rol") == "3"
    assert leer_version_prompt("# Rol sin versión") == "sin versión"
    assert leer_version_prompt("") == "sin versión"
