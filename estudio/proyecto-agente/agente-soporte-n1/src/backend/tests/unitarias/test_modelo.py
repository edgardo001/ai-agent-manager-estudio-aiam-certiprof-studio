"""Pruebas unitarias de cómo modelo.py lee la respuesta de la librería openai, sin llamar a Gemini.
Se arma una respuesta con el mismo tipo que entrega la librería (ChatCompletion)."""
from types import SimpleNamespace

from openai.types.chat import ChatCompletion

from aplicacion import modelo


def cliente_falso(respuesta):
    """Imita al cliente de openai: cliente.chat.completions.create() devuelve una respuesta fija.
    Técnico: no viene del curso."""
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **opciones: respuesta)))


def respuesta_de_openai(mensaje, fin, uso):
    """Arma una respuesta como la que entrega la librería openai. Técnico: no viene del curso."""
    datos = {"id": "x", "object": "chat.completion", "created": 0, "model": "prueba",
             "choices": [{"index": 0, "finish_reason": fin, "message": mensaje}]}
    if uso:
        datos["usage"] = uso
    return ChatCompletion.model_validate(datos)


def test_conserva_la_firma_de_gemini_y_lee_los_pedidos(monkeypatch):
    """El mensaje vuelve con la firma de pensamiento que Gemini 3 exige recibir de vuelta (D11),
    y los pedidos de herramientas y los tokens se leen bien. Técnico: no viene del curso."""
    firma = {"google": {"thought_signature": "abc"}}
    mensaje = {"role": "assistant", "content": None, "tool_calls": [{
        "id": "c1", "type": "function", "function": {"name": "buscar_cliente", "arguments": "{}"}, "extra_content": firma}]}
    uso = {"prompt_tokens": 120, "completion_tokens": 8, "total_tokens": 128}
    monkeypatch.setattr(modelo, "conectar_modelo", lambda: cliente_falso(respuesta_de_openai(mensaje, "tool_calls", uso)))
    resultado = modelo.conversar_con_herramientas([], [])
    assert resultado["mensaje"]["tool_calls"][0]["extra_content"] == firma
    assert resultado["llamadas"] == [("c1", "buscar_cliente", "{}")]
    assert (resultado["texto"], resultado["fin"], resultado["tokens_entrada"], resultado["tokens_salida"]) == ("", "tool_calls", 120, 8)


def test_sin_uso_informado_los_tokens_son_cero(monkeypatch):
    """Si el proveedor no informa los tokens, se cuentan 0 (el tope de tokens no se activaría;
    queda el máximo de llamadas). Técnico: no viene del curso (revisión de la etapa 3, m4)."""
    mensaje = {"role": "assistant", "content": "hola"}
    monkeypatch.setattr(modelo, "conectar_modelo", lambda: cliente_falso(respuesta_de_openai(mensaje, "stop", None)))
    resultado = modelo.conversar_con_herramientas([], [])
    assert (resultado["texto"], resultado["llamadas"], resultado["tokens_entrada"]) == ("hola", [], 0)


def test_la_temperatura_se_envia_solo_si_se_pide(monkeypatch):
    """Sin temperatura, el proveedor usa la suya; las evals piden 0 y esa sí se envía (también el 0).
    Técnico: no viene del curso (evals-del-llm.md; revisión del prompt maestro, M8)."""
    monkeypatch.setattr(modelo.config, "LLM_MODEL", "modelo")
    monkeypatch.setattr(modelo.config, "LLM_MAXIMO_TOKENS_SALIDA", 2000)
    assert modelo.opciones_de_llamada(None) == {"model": "modelo", "max_tokens": 2000}
    assert modelo.opciones_de_llamada(0) == {"model": "modelo", "max_tokens": 2000, "temperature": 0}


def test_chat_y_embeddings_usan_cada_uno_su_proveedor(monkeypatch):
    """El chat y los embeddings pueden ir a proveedores distintos, cada uno con su URL y su clave:
    así el chat se cambia a OpenRouter sin recargar los vectores (D13). Técnico: no viene del curso."""
    # config.py arma estas cuatro a partir de LLM_PROVEEDOR y LLM_EMBEDDINGS_PROVEEDOR (D14).
    monkeypatch.setattr(modelo.config, "LLM_BASE_URL", "https://openrouter.ai/api/v1/")
    monkeypatch.setattr(modelo.config, "LLM_API_KEY", "clave-chat")
    monkeypatch.setattr(modelo.config, "LLM_EMBEDDINGS_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    monkeypatch.setattr(modelo.config, "LLM_EMBEDDINGS_API_KEY", "clave-embeddings")
    chat, embeddings = modelo.conectar_modelo(), modelo.conectar_modelo(para_embeddings=True)
    assert (str(chat.base_url), chat.api_key) == ("https://openrouter.ai/api/v1/", "clave-chat")
    assert (str(embeddings.base_url), embeddings.api_key) == ("https://generativelanguage.googleapis.com/v1beta/openai/", "clave-embeddings")
