"""Preparación común de las pruebas (etapa 3).

La fixture `conexion` abre una conexión con el PostgreSQL de desarrollo y, al terminar cada
prueba, deshace todo lo que la prueba escribió (rollback): las pruebas nunca dejan datos.
Funciona porque el código del agente no confirma los cambios; lo hace quien llama (decisión D11).
Si PostgreSQL no responde, las pruebas que lo necesitan se omiten con un aviso, en vez de fallar.
Técnico: no viene del curso.
"""
import pytest

from aplicacion.base_de_datos import conectar


@pytest.fixture
def conexion():
    """Conexión con PostgreSQL que se deshace al final de cada prueba."""
    try:
        con = conectar()
    except Exception as error:  # PostgreSQL apagado o .env sin contraseña
        pytest.skip(f"PostgreSQL no responde ({error}): ejecute start-dev.bat")
    try:
        yield con
    finally:
        con.rollback()
        con.close()
