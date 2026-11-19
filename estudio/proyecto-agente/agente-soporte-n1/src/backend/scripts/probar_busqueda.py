"""Script de asistencia, etapa 2: prueba la búsqueda en la base de conocimiento, sin el agente.

Uso, desde la carpeta src/backend con el entorno virtual activo, después de cargar_conocimiento:
    python -m scripts.probar_busqueda
    python -m scripts.probar_busqueda "mi factura sale cortada"
Sin texto, prueba una lista de consultas fijas y dice si cada una encuentra el documento esperado.
Desde la etapa 3 usa la misma búsqueda que la herramienta buscar_solucion del agente
(herramientas.buscar), así lo que se prueba aquí es lo que encuentra el agente.
"""
import sys

from aplicacion import config
from aplicacion.base_de_datos import conectar, contar_fragmentos
from aplicacion.herramientas import buscar

# Consulta y documento que debería aparecer primero. La última no tiene documento a propósito:
# no se le exige una similitud baja, porque un umbral no sirve (decisión D8): el agente decide escalar.
CONSULTAS = [
    ("no puedo entrar, olvidé mi clave", "restablecer-contrasena.md"),
    ("me sale que mi cuenta está bloqueada", "cuenta-bloqueada.md"),
    ("las facturas no aparecen en la web, dice pendiente de sincronizar", "error-de-sincronizacion.md"),
    ("quiero descargar las ventas del mes en Excel", "exportar-reportes.md"),
    ("la factura impresa sale cortada", "configurar-impresora.md"),
    ("quiero pasarme al plan Empresa", "cambiar-plan.md"),
    ("me cobraron dos veces este mes", "facturacion-y-cobros.md"),
    ("¿pueden conectar Nubesoft con mi máquina de café?", None),
]


def probar_busqueda():
    """Muestra qué documentos encuentra cada consulta y si coinciden con lo esperado.
    Técnico: es una prueba manual; las pruebas automáticas están en tests/, desde la etapa 3."""
    faltan = config.faltan_variables(con_base_de_datos=True)
    if faltan:
        print(f"Faltan en src/docker/.env: {', '.join(faltan)}.")
        return
    try:
        conexion = conectar()
    except Exception as error:  # PostgreSQL apagado, contraseña equivocada...
        print(f"No se pudo conectar con PostgreSQL ({error}). ¿Está abierto Docker y se ejecutó start-dev.bat?")
        return
    try:
        if contar_fragmentos(conexion) == 0:  # base vacía, o cargada con otro modelo de embeddings
            print(f"La base no tiene fragmentos del modelo {config.LLM_MODELO_EMBEDDINGS}: ejecute python -m scripts.cargar_conocimiento.")
            return
        if len(sys.argv) > 1:  # una consulta escrita por la persona: los fragmentos más parecidos
            for documento, seccion, _, similitud, _ in buscar(conexion, " ".join(sys.argv[1:])):
                print(f"{similitud:.2f}  {documento} > {seccion}")
            return
        aciertos = 0
        for consulta, esperado in CONSULTAS:  # la lista fija: solo importa el primer resultado
            documento, seccion, _, similitud, _ = buscar(conexion, consulta)[0]
            if esperado is None:
                print(f"[sin documento] {similitud:.2f}  {consulta!r} -> {documento} > {seccion}")
                continue
            aciertos += documento == esperado
            print(f"[{'bien' if documento == esperado else 'MAL '}] {similitud:.2f}  {consulta!r} -> {documento} > {seccion}")
        print(f"\n{aciertos} de {sum(1 for _, e in CONSULTAS if e)} consultas encontraron el documento esperado.")
    except Exception as error:  # sin red, clave inválida, límite de uso del modelo...
        print(f"La búsqueda se detuvo: {error}")
    finally:
        conexion.close()


if __name__ == "__main__":
    probar_busqueda()
