# 03 · Registro de agentes

> **Para qué sirve:** tener en un solo lugar el inventario de todos los agentes de IA activos del área u organización, con su nivel de autonomía, su función, su responsable y su estado de validación, para saber cuántos agentes hay, para qué sirven y quién responde por ellos. Es el primer mecanismo contra el agent sprawl (crecimiento desordenado de agentes sin dueño ni propósito).
> **Cuándo llenarla:** se abre una fila cuando se aprueba un agente nuevo (antes de su configuración técnica) y se actualiza cada vez que cambia algo del agente (permisos, métricas, validación). Se revisa completa en cada auditoría trimestral y antes de cada ciclo de revisión con la alta dirección.
> **Quién la llena y quién la aprueba:** la mantiene el AI Agent Manager (gestor de agentes de IA, el profesional que gobierna los agentes); cada Agent Owner (responsable directo de uno o más agentes, sección 4.5) actualiza los datos de sus agentes. Se presenta al C-suite (la alta dirección de la empresa) y al Governance Board (comité de gobierno de agentes, sección 3.6).
> **Con qué se llena:** las fichas de identidad (plantilla 04), las actas de aceptación (plantilla 06), el tablero de supervisión (plantilla 09) y entrevistas con cada área para descubrir agentes que nadie registró.
> **Base en el curso:** Módulo 1, responsabilidades 1 y 2 (inventario y clasificación, mapa de accountability, es decir, de quién responde por cada agente); Módulo 2, sección 2.7 (registro centralizado) y responsabilidad 5 (registro de agentes activos); pregunta 5 del Módulo 2.
> **Se conecta con:** se alimenta de 04 · Ficha de identidad del agente y 06 · Onboarding y aceptación; alimenta a 09 · Plan de supervisión, 12 · Governance Board, 13 · Auditoría trimestral del portafolio y 14 · Reporte a la dirección.

## Cómo llenarla

1. Haga el inventario: pregunte en cada área qué agentes de IA están operando, incluidos los pilotos que pasaron a producción sin proceso formal (sección 2.7 advierte que ahí nace el agent sprawl).
2. Cree una fila por agente en la Tabla A, con los campos que exige la sección 2.7. Si no conoce un dato, escriba "no sé": un "no sé" es una alerta, no un campo vacío.
3. Clasifique cada agente en uno de los 4 niveles de autonomía (sección 1.2). Si tiene dudas, use la plantilla 04.
4. Complete la Tabla B (mapa de accountability, es decir, de responsabilidad: quién responde por qué) para cada agente: quién responde por sus resultados, errores y decisiones ante el equipo, los clientes y el C-suite.
5. Revise la Tabla C de alertas. Atienda primero el agente que esté en producción sin validación pre-producción (pregunta 5 del Módulo 2: es el mayor riesgo activo).
6. Actualice la fecha de última validación y las métricas actuales después de cada auditoría (plantilla 13).
7. Presente el registro al C-suite en cada ciclo de revisión (responsabilidad 5 del Módulo 2).

## Plantilla

**Área u organización:** `[escriba aquí…]`
**AI Agent Manager a cargo del registro:** `[nombre y cargo]`
**Fecha de la última actualización:** `[AAAA-MM-DD]`

### Tabla A. Registro centralizado de agentes

| Campo | Qué escribir | Base |
|---|---|---|
| Nombre del agente | El nombre con que la organización lo conoce. | 2.2, 2.7 |
| Función | Una oración: qué problema resuelve, para quién y en qué contexto. | 2.2, 2.7 |
| Nivel de autonomía | 1 Asistencia, 2 Automatización, 3 Augmentación (ampliación de capacidades) o 4 Autonomía Total. | 1.2, 2.7 |
| Área de aplicación y área responsable | Dónde opera y qué área responde por él. | M1 resp. 1, 2.7 |
| AI Agent Manager designado | Nombre. "Ninguno" es una alerta. | 2.7 |
| Agent Owner | Nombre del responsable directo (sección 4.5: ningún agente debe operar sin Agent Owner asignado). | 4.5 |
| Permisos de acceso | Sistemas y datos a los que accede (detalle en la plantilla 04). | M2 resp. 5 |
| Estado de validación pre-producción | Validado (fecha), en validación, o "en producción sin validar". | 2.6, pregunta 5 |
| Fecha de última validación o auditoría | AAAA-MM-DD. | 2.7, M2 resp. 5 |
| Métricas de desempeño actuales | Las métricas de negocio de la ficha 04 y su valor actual. | 2.7, M2 resp. 5 |

Formato sugerido para llevar varios agentes a la vez (no viene en el curso; es solo una forma práctica de ordenar los campos anteriores):

| N.º | Nombre | Función | Nivel | Área | AI Agent Manager | Agent Owner | Permisos (resumen) | Validación | Última revisión | Métricas actuales |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `[…]` | `[…]` | `[1-4]` | `[…]` | `[…]` | `[…]` | `[…]` | `[…]` | `[AAAA-MM-DD]` | `[…]` |
| 2 | | | | | | | | | | |

### Tabla B. Mapa de accountability (responsabilidad) por agente

Para cada agente, documente explícitamente quién responde (Módulo 1, responsabilidad 2):

| Agente | Por sus resultados | Por sus errores | Por sus decisiones | Ante el equipo | Ante los clientes | Ante el C-suite |
|---|---|---|---|---|---|---|
| `[…]` | `[nombre]` | `[nombre]` | `[nombre]` | `[nombre]` | `[nombre]` | `[nombre]` |

### Tabla C. Alertas de agent sprawl

Marque las que se cumplan para algún agente (sección 2.7 y reflexión estratégica del Módulo 2):

- [ ] Hay agentes sin AI Agent Manager identificado.
- [ ] Hay agentes que no pasaron por validación pre-producción.
- [ ] Hay agentes sin métricas de negocio definidas y monitoreadas.
- [ ] Hay agentes sin propósito documentado.
- [ ] Hay agentes que hacen versiones ligeramente diferentes de lo mismo (redundancia operacional).
- [ ] Hay pilotos que pasaron a producción sin onboarding formal (incorporación estructurada del agente, plantilla 06).

**Acciones que se derivan:** `[qué se hará, quién y para cuándo; la primera, el agente sin validación]`

## Ejemplo lleno

Datos ficticios de ejemplo. El agente 1 es el agente de soporte de la sección 2.5 (su función, herramientas y metas vienen del curso; los nombres de personas, fechas y valores actuales son ficticios, y la clasificación en Nivel 2 la explica la plantilla 04). La situación de los otros agentes imita la pregunta 5 del Módulo 2.

**Área u organización:** empresa de software B2B (que vende a otras empresas), varias áreas.
**AI Agent Manager a cargo del registro:** Ana Rojas, AI Agent Manager corporativa.
**Fecha de la última actualización:** 2026-11-17.

| N.º | Nombre | Función | Nivel | Área | AI Agent Manager | Agent Owner | Permisos (resumen) | Validación | Última revisión | Métricas actuales |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Agente de Soporte N1 | Resolver tickets (solicitudes de soporte) de nivel 1 de clientes existentes en el portal de soporte | 2 | Customer Success (éxito del cliente) | Ana Rojas | Luis Pérez | CRM (sistema de gestión de clientes) en solo lectura; base de conocimiento | Validado 2026-09-30 | 2026-10-31 | Resolución autónoma 82%; CSAT (satisfacción del cliente) 4,3 sobre 5; escalamiento 18%; 2,7 minutos |
| 2 | Agente de Cobranza Preventiva | Recordar pagos próximos a vencer | 2 | Finanzas | Ninguno | Ninguno | ERP (sistema contable) y correo | En producción sin validar | No sé | No definidas |
| 3 | Asistente de Propuestas | Sugerir borradores de propuestas comerciales; el vendedor decide | 1 | Ventas | Ana Rojas | Marta Díaz | CRM en solo lectura | Validado 2026-06-15 | 2026-06-15 | No definidas |

**Mapa de accountability del agente 1:** por sus resultados responde Ana Rojas; por sus errores y decisiones del día a día responde Luis Pérez como primer punto de contacto, que escala a Ana Rojas; ante el equipo de soporte responde Luis Pérez; ante los clientes responde la jefa de Customer Success; ante el C-suite responde Ana Rojas.

**Alertas marcadas:** agente sin AI Agent Manager (2), agente sin validación (2), agentes sin métricas de negocio (2 y 3).

**Acciones:** (1) revisión urgente del agente 2, que está en producción sin validación, y designación de su AI Agent Manager esta semana; (2) definir métricas de negocio para los agentes 2 y 3 en sus fichas 04; (3) presentar el registro actualizado al C-suite en el próximo ciclo de revisión.

## Errores comunes

- **Creer que el registro es un trámite de IT (área de sistemas).** El curso dice que la gestión del portafolio es business governance (gobierno de negocio) aplicado a sistemas autónomos, no IT governance (sección 2.7).
- **Dejar agentes sin dueño.** Sin propietario claro, nadie responde cuando un agente toma una decisión incorrecta: es gobernanza sin dueño, uno de los tres costos del agent sprawl (sección 2.7).
- **Esperar a que el desorden "se resuelva solo".** Ante agentes sin manager, sin métricas o sin validación, la primera acción es completar el registro y priorizar el agente sin validar (pregunta 5 del Módulo 2).
- **No actualizar el registro.** Debe estar al día con la fecha de última validación y las métricas actuales, y presentarse en cada ciclo de revisión (sección 2.7 y responsabilidad 5 del Módulo 2).
- **Confundir la clasificación de nivel.** Tratar un agente de Nivel 4 como si tuviera el riesgo de uno de Nivel 2 es un error frecuente; la diferencia es exponencial (sección 1.2, nota crítica).
