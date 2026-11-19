# Base de conocimiento

Documentos de soporte ficticios de Nubesoft, una empresa inventada, con su producto Nubesoft Facturación. Son la fuente de las soluciones documentadas del agente (Módulo 2, sección 2.5): `cargar_conocimiento.py` los corta en fragmentos y los guarda en pgvector, y el agente solo puede responder con lo que encuentre aquí. Nunca llevan información real: el repositorio es público.

| Documento | Qué prueba |
|---|---|
| `restablecer-contrasena.md` | caso funcional frecuente (sección 2.6) |
| `cuenta-bloqueada.md` | caso parecido al anterior: la búsqueda debe distinguirlos |
| `error-de-sincronizacion.md` | caso funcional con varios pasos y un código que exige escalar |
| `exportar-reportes.md` | caso funcional simple |
| `configurar-impresora.md` | caso “ligeramente inusual” (sección 2.6) |
| `cambiar-plan.md` | exige un cambio de cuenta: siempre con confirmación humana |
| `limites-del-soporte.md` | lo que queda fuera del alcance del agente (sección 2.2) |
| `facturacion-y-cobros.md` | dinero y descuentos: el agente escala y no ofrece nada (sección 2.5) |

Hay casos sin documento a propósito (por ejemplo, “integrar con mi máquina de café”), para probar que el agente escala cuando no hay una solución documentada. Este `README.md` no se carga a la base: `cargar_conocimiento.py` lo omite.

## Formato de cada documento

`cargar_conocimiento.py` corta cada documento por sus secciones (decisión D8), así que todos siguen el mismo formato:

1. La primera línea es el título, con `# `. Se antepone a cada fragmento.
2. Las líneas que empiezan con `>`, antes de la primera sección, son avisos (por ejemplo, “documento ficticio”) y no se cargan.
3. El texto antes de la primera sección se carga como la sección “Introducción”.
4. Cada sección empieza con `## ` y su nombre, que se usa para citar (“cuenta-bloqueada.md > Pasos”).
5. Los párrafos se separan con una línea en blanco: si una sección es larga, se corta entre párrafos.
6. Se guardan en UTF-8; si un editor agrega la marca BOM, la carga la ignora. Un documento sin contenido se omite con un aviso.
