# Revisión de la etapa 4, 2026-11-19

Dos revisiones de solo lectura pedidas por el usuario antes de cerrar la etapa: elephant-goldfish-model (exactitud, diseño y simplicidad) y un verificador independiente de fidelidad al curso. A los dos se les prohibió leer o buscar en la carpeta de la configuración local. El agente que las pidió comprobó ejecutando las reglas los hallazgos 1 y 4: “Actualice su aplicación” y “Cambie su contraseña” se bloquean como cambio de cuenta; “Ya cancelé la factura” escala como cancelación; “quiero cerrar mi cuenta” y “no quiero renovar” no escalan.

**Estado:** aplicada el 2026-11-19, con las decisiones del usuario del final.

## Resultado general

- **Nada bloquea.** El orden de las revisiones en `atender_mensaje` es correcto (lo que no gasta va antes, el kill switch primero, el pedido de escalar del modelo antes de los topes) y el SQL nuevo está bien.
- **Seis hallazgos importantes,** dos de ellos sobre los patrones de `reglas.py` y uno sobre una red de seguridad que nunca encuentra nada.
- **Fidelidad:** de 38 citas, 26 fieles y 12 imprecisas; ninguna inventa un dato.

## Hallazgos importantes

| # | Hallazgo | Arreglo propuesto |
|---|---|---|
| 1 | `revisar_respuesta()` bloquea instrucciones normales: al quitar las tildes, “actualice su” (una indicación) queda igual que “actualicé su” (algo que el agente dice haber hecho). Afecta al estilo más común de una solución | buscar los verbos en primera persona con su tilde obligatoria y probar “Actualice su aplicación” como caso que pasa |
| 2 | `escalar_vencidos()`: la parte de “mensaje del cliente sin respuesta” nunca encuentra nada, porque por D11 el mensaje se confirma junto con la respuesta; si el proceso muere a mitad, el mensaje del cliente se pierde | (a) confirmar el mensaje del cliente antes de atenderlo, o (b) quitar esa parte y dejarla para la API |
| 3 | Si falla el SQL dentro de una herramienta, la transacción queda abortada y el escalamiento también falla: se pierden el mensaje, los tokens y la auditoría, contra D11 | un punto de retorno (`SAVEPOINT`) antes de cada herramienta, con su prueba |
| 4 | “cancelar” sin objeto ni intención: “ya cancelé la factura” (pagarla, en Chile y buena parte de Latinoamérica) escala; “cerrar mi cuenta”, “no quiero renovar” o “desuscribirme” no | exigir intención u objeto (“quiero cancelar”, “cancelar mi cuenta”) y sumar “cerrar mi cuenta”, “desuscribirme”, “dar de baja” en sus formas; dejar los casos escritos en las pruebas |
| 5 | La respuesta bloqueada no se guarda: no se puede saber después si fue un falso positivo | guardar el texto bloqueado en el paso de la auditoría |
| 6 | Se repite en cinco lugares que `anotar()` es el único que escribe la auditoría, y no es cierto (las intervenciones las escribe `reglas.py`); cada regla está descrita en el docstring, D16, el plan, los diagramas, `rag.md` y el README de pruebas | corregir la frase; el comportamiento de cada regla, solo en “Cómo funciona cada regla” del plan; D16 solo con el porqué |

## Hallazgos menores

- **Auditoría:** el ticket ya escalado no deja paso; los escalamientos por regla antes de leer el prompt quedan sin versión ni huella pero con proveedor y modelo; `escalar_vencidos` usa otro formato de decisión; el número de paso vuelve a 1 en cada mensaje.
- **Concurrencia:** dos consolas (o el dashboard) podrían escalar el mismo ticket dos veces; `guardar_escalamiento()` debería exigir que el ticket siga abierto.
- **Un ticket reabierto** conserva su fecha de cierre.
- **El tiempo se revisa antes de cada llamada al modelo,** no “antes de cada paso”, como dice el plan.
- **Los motivos del kill switch** son distintos al empezar y a mitad del bucle.
- **Patrones de salida:** el de descuentos atrapa “rebajar la resolución” y deja pasar “un mes gratis”, “sin cargo” o “le abonamos”; el de cambio de cuenta deja pasar “su cuenta fue actualizada” o “he procesado el reembolso”; el código de otro cliente no detecta “c-002” ni “C002”.
- **Documentación desactualizada:** el estado y algunos textos del diagrama del código, el docstring de `buscar()` (dice 4 campos y devuelve 5) y la fila de la etapa 4 del plan.
- **Pruebas que faltan:** el kill switch a mitad del bucle; `revisar_respuesta` en integración con cambio de cuenta y otro cliente; los casos negativos; un error de SQL en una herramienta; los casos que no deben escalarse en `escalar_vencidos`. La prueba del tiempo con límite 0 puede fallar al azar en Windows (conviene -1).
- **Simplicidad:** unir `detener_agente()` y `reactivar_agente()`; `reglas.py` debe quedar separado, porque es la frontera del curso entre lo que decide el modelo y lo que garantiza el código.

## Fidelidad al curso: citas imprecisas

| Dónde | Problema | Arreglo |
|---|---|---|
| `reglas.py`, la restricción de cambios de cuenta | cita textual sin “del cliente” | copiar la frase exacta de la sección 2.5 |
| `reglas.py` y `test_reglas.py`, verificación de alto impacto (3.3) | la 3.3 habla de verificar la precisión de un dato antes de actuar (tipo 3 de fallo silencioso), no de revisar una política | “inspirado en los puntos de verificación obligatoria (3.3)” |
| `reglas.py`, `base_de_datos.py`, `consola.py` y `test_agente.py`, detener y reactivar como “intervención” (3.4) | la 3.4 da criterios para decidir cuándo intervenir; no habla de detener, reactivar ni de registrar quién | detener: kill switch (1.2) y circuit breaker (4.5); cuándo intervenir: 3.4; registrarlo es del proyecto |
| `test_agente.py` | “kill switch (sección 1.2)” se lee como del Módulo 3 | “Módulo 1, sección 1.2” |
| `base_de_datos.py` y `test_agente.py`, “no inflar la resolución autónoma (3.3)” | la tasa de resolución autónoma está en la 3.2 | “inspirado en la tasa de resolución autónoma (3.2) y en los fallos silenciosos (3.3); la regla es del proyecto” |
| `agente.py`, `huella_de()` y `leer_version_prompt()` | el curso no habla de versiones de las instrucciones | “validación antes de producción (2.6) y registro con fecha de última validación (2.7); identificar la versión exacta es del proyecto” |
| D16 | “un kill switch (secciones 1.2 y 4.5)” | “un kill switch (1.2) y un circuit breaker (4.5)”; el curso no dice que sean lo mismo |

Observación del verificador: en los escalamientos por regla, el resumen para la persona va vacío; recibe el motivo, las herramientas usadas y la conversación, pero no un resumen.

## Decisiones del usuario

1. **Hallazgo 2:** el mensaje del cliente se guarda y se confirma antes de atenderlo, para que no se pierda y `escalar_vencidos()` lo rescate.
2. **Hallazgo 4:** la cancelación exige intención u objeto.
3. **Aplicar todo lo demás:** los hallazgos 1, 3, 5 y 6, los menores y las 12 citas.

Resultado en `pruebas/2026-11-19-etapa-4.md`: 89 pruebas; ningún párrafo de la base de conocimiento bloqueado por `revisar_respuesta()`.

