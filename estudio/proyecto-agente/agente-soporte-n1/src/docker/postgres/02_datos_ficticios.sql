-- Etapa 2. Datos ficticios de ejemplo: el agente, sus clientes y su línea base.
-- Se ejecuta después de 01_esquema.sql, la primera vez que se crea el volumen de datos.
-- Todo es inventado (regla 10 del plan): Nubesoft y sus clientes no existen.
-- El historial de tickets para las tendencias del dashboard se agrega en la etapa 7.

-- El Agente de Soporte N1 en el registro de agentes (secciones 1.2, 2.2 y 2.7).
INSERT INTO registro_agentes (
    nombre, rol, alcance, fuera_de_alcance, nivel_autonomia, dueno, area_responsable,
    permisos, restricciones,
    meta_resolucion_autonoma, meta_escalamiento, meta_minutos_resolucion, meta_csat,
    base_casos_por_dia, base_minutos_por_caso, base_costo_por_caso
) VALUES (
    'Agente de Soporte N1',
    'Resolver tickets de soporte técnico de nivel 1 de los clientes de Nubesoft Facturación',
    'Problemas técnicos frecuentes con solución documentada en la base de conocimiento',
    'Cancelaciones, cambios de plan, correo o datos de facturación, reembolsos y descuentos, integraciones, sospechas de fraude y todo caso sin solución documentada',
    'Nivel 3, Augmentación',
    'El usuario del proyecto, como AI Agent Manager',
    'Customer Success (ficticia)',
    'buscar_cliente: leer el CRM, solo del cliente del ticket, para conocer su plan e historial. '
    'buscar_solucion: leer la base de conocimiento, porque solo puede responder con soluciones documentadas. '
    'escalar_a_humano: pasar el caso a una persona, porque hay casos que el agente no debe resolver.',
    'No cambiar la cuenta del cliente sin confirmación humana. No compartir información de otros clientes. No ofrecer descuentos no autorizados.',
    80, 20, 3, 4.2,          -- metas de la sección 2.5
    120, 12, 6.5             -- línea base ficticia: 120 casos al día, 12 minutos y 6,5 dólares por caso sin el agente
);

-- Clientes del CRM simulado (datos ficticios).
INSERT INTO clientes (codigo, nombre, empresa, plan, historial) VALUES
    ('C-001', 'Ana Torres',     'Panadería La Espiga',      'Básico',  'Cliente desde 2024. Un ticket anterior por contraseña olvidada.'),
    ('C-002', 'Bruno Díaz',     'Ferretería El Tornillo',   'Pyme',    'Cliente desde 2023. Dos tickets por sincronización.'),
    ('C-003', 'Carla Muñoz',    'Estudio Contable Muñoz',   'Empresa', 'Cliente desde 2022. Sin tickets anteriores.'),
    ('C-004', 'Diego Rojas',    'Librería Página Doce',     'Básico',  'Cliente desde 2025. Preguntó por cambio de plan en marzo.'),
    ('C-005', 'Elena Castro',   'Clínica Veterinaria Lua',  'Pyme',    'Cliente desde 2024. Un ticket por impresión de facturas.'),
    ('C-006', 'Felipe Soto',    'Transportes Soto',         'Empresa', 'Cliente desde 2021. Un cobro en disputa resuelto en 2025.');
