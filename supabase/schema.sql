-- =============================================================
--  GoToCloud Voicebot — Schema de Base de Conocimientos
--  Proyecto Supabase: nzeruwamlpacikmqtcja
--  Ejecutar en: https://supabase.com/dashboard/project/nzeruwamlpacikmqtcja/sql/new
-- =============================================================

-- 1. Empresa (una fila, id=1)
CREATE TABLE IF NOT EXISTS public.empresa (
    id              SERIAL PRIMARY KEY,
    nombre          TEXT NOT NULL,
    descripcion     TEXT,
    presencia       TEXT,
    propuesta_valor         JSONB DEFAULT '[]'::jsonb,
    clientes_destacados     JSONB DEFAULT '[]'::jsonb,
    partners                JSONB DEFAULT '[]'::jsonb,
    reconocimientos         JSONB DEFAULT '[]'::jsonb,
    contacto                JSONB DEFAULT '{}'::jsonb
);

COMMENT ON TABLE public.empresa IS 'Información general de GoToCloud';
COMMENT ON COLUMN public.empresa.propuesta_valor IS 'Array de strings: propuesta de valor';
COMMENT ON COLUMN public.empresa.clientes_destacados IS 'Array de strings: nombres de clientes';
COMMENT ON COLUMN public.empresa.contacto IS 'Objeto: {whatsapp, web, linkedin}';

-- 2. Servicios (cloud_computing, seguridad, datos, etc.)
CREATE TABLE IF NOT EXISTS public.servicios (
    id              TEXT PRIMARY KEY,
    nombre          TEXT NOT NULL,
    descripcion     TEXT,
    categoria       TEXT,
    subcategoria    TEXT,
    beneficios      JSONB DEFAULT '[]'::jsonb,
    para_quien      JSONB DEFAULT '{}'::jsonb,
    pilares         JSONB DEFAULT '[]'::jsonb,
    metodologias    JSONB DEFAULT '[]'::jsonb,
    alcance         JSONB DEFAULT '[]'::jsonb,
    reportes        JSONB DEFAULT '[]'::jsonb,
    especializaciones JSONB DEFAULT '[]'::jsonb,
    partners        JSONB DEFAULT '[]'::jsonb
);

COMMENT ON TABLE public.servicios IS 'Servicios cloud de GoToCloud con metadata';

-- 3. Métricas (pares clave-valor)
CREATE TABLE IF NOT EXISTS public.metricas (
    clave   TEXT PRIMARY KEY,
    valor   TEXT NOT NULL
);

COMMENT ON TABLE public.metricas IS 'Cifras de impacto: empresas transformadas, servidores migrados, etc.';

-- 4. Productos SaaS (Kármán, OASIS AI, DataLoom)
CREATE TABLE IF NOT EXISTS public.productos_saas (
    id              TEXT PRIMARY KEY,
    nombre          TEXT NOT NULL,
    descripcion     TEXT,
    para_quien      TEXT,
    funcionalidades JSONB DEFAULT '[]'::jsonb,
    beneficios      JSONB DEFAULT '[]'::jsonb,
    seguridad       JSONB DEFAULT '[]'::jsonb
);

COMMENT ON TABLE public.productos_saas IS 'Productos SaaS propios de GoToCloud';

-- 5. Clientes (persistencia de sesión)
CREATE TABLE IF NOT EXISTS public.clientes (
    id          SERIAL PRIMARY KEY,
    nombre      TEXT NOT NULL,
    cedula      TEXT NOT NULL UNIQUE,
    empresa     TEXT,
    telefono    TEXT,
    updated_at  TIMESTAMPTZ DEFAULT now(),
    created_at  TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE public.clientes IS 'Registro de llamadas / clientes contactados';

-- 6. Llamadas (metadata de cada llamada)
CREATE TABLE IF NOT EXISTS public.llamadas (
    id                  SERIAL PRIMARY KEY,
    cliente_id          INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    started_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    ended_at            TIMESTAMPTZ,
    duracion_segundos   INTEGER,
    resumen             TEXT,
    intention           VARCHAR(10) CHECK (intention IN ('fria', 'calida', 'caliente')),
    score_lead          INTEGER CHECK (score_lead BETWEEN 0 AND 100),
    servicios_interes   TEXT[] DEFAULT '{}',
    recomendaciones     TEXT,
    created_at          TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE public.llamadas IS 'Metadata de llamadas: resumen, intención, score, servicios de interés';

-- =============================================================
--  Permisos: habilitar acceso anónimo (lectura/escritura)
--  NOTA: Ajustar según necesidad de seguridad en producción
-- =============================================================
ALTER TABLE public.empresa         ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.servicios       ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.metricas        ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.productos_saas  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.clientes        ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.llamadas         ENABLE ROW LEVEL SECURITY;

-- Limpiar políticas existentes (para rerun seguro)
DROP POLICY IF EXISTS "anon_select_empresa"         ON public.empresa;
DROP POLICY IF EXISTS "anon_select_servicios"       ON public.servicios;
DROP POLICY IF EXISTS "anon_select_metricas"        ON public.metricas;
DROP POLICY IF EXISTS "anon_select_productos_saas"  ON public.productos_saas;
DROP POLICY IF EXISTS "anon_insert_clientes"        ON public.clientes;
DROP POLICY IF EXISTS "anon_select_clientes"        ON public.clientes;
DROP POLICY IF EXISTS "anon_insert_llamadas"        ON public.llamadas;
DROP POLICY IF EXISTS "anon_select_llamadas"        ON public.llamadas;
DROP POLICY IF EXISTS "anon_insert_empresa"         ON public.empresa;
DROP POLICY IF EXISTS "anon_upsert_empresa"         ON public.empresa;
DROP POLICY IF EXISTS "anon_insert_servicios"       ON public.servicios;
DROP POLICY IF EXISTS "anon_upsert_servicios"       ON public.servicios;
DROP POLICY IF EXISTS "anon_insert_metricas"        ON public.metricas;
DROP POLICY IF EXISTS "anon_upsert_metricas"        ON public.metricas;
DROP POLICY IF EXISTS "anon_insert_productos_saas"  ON public.productos_saas;
DROP POLICY IF EXISTS "anon_upsert_productos_saas"  ON public.productos_saas;

-- Permitir lectura anónima para todas las tablas
CREATE POLICY "anon_select_empresa"         ON public.empresa         FOR SELECT USING (true);
CREATE POLICY "anon_select_servicios"       ON public.servicios       FOR SELECT USING (true);
CREATE POLICY "anon_select_metricas"        ON public.metricas        FOR SELECT USING (true);
CREATE POLICY "anon_select_productos_saas"  ON public.productos_saas  FOR SELECT USING (true);

-- Permitir insert anónimo en clientes (registro de llamadas)
CREATE POLICY "anon_insert_clientes" ON public.clientes
    FOR INSERT WITH CHECK (true);

-- Permitir select anónimo en clientes (verificar si ya existe)
CREATE POLICY "anon_select_clientes" ON public.clientes
    FOR SELECT USING (true);

-- Políticas RLS para tabla llamadas
CREATE POLICY "anon_insert_llamadas" ON public.llamadas
    FOR INSERT WITH CHECK (true);

CREATE POLICY "anon_select_llamadas" ON public.llamadas
    FOR SELECT USING (true);

-- Permitir insert/upsert anónimo para seed de datos
CREATE POLICY "anon_insert_empresa" ON public.empresa
    FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_upsert_empresa" ON public.empresa
    FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "anon_insert_servicios" ON public.servicios
    FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_upsert_servicios" ON public.servicios
    FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "anon_insert_metricas" ON public.metricas
    FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_upsert_metricas" ON public.metricas
    FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "anon_insert_productos_saas" ON public.productos_saas
    FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_upsert_productos_saas" ON public.productos_saas
    FOR UPDATE USING (true) WITH CHECK (true);

-- =============================================================
--  Seed data (INSERT con ON CONFLICT para ser idempotente)
--  Corre con permisos de owner (SQL Editor), no depende del anon key
-- =============================================================

-- 1. Empresa
INSERT INTO public.empresa (id, nombre, descripcion, presencia, propuesta_valor, clientes_destacados, partners, reconocimientos, contacto)
VALUES (
    1,
    'GoToCloud',
    'GoToCloud es una empresa colombiana especializada en transformación digital mediante soluciones en la nube con foco en Microsoft Azure. Ayuda a empresas a migrar, modernizar y optimizar su operación tecnológica con seguridad e IA.',
    'Opera en toda Latinoamérica: Colombia, Estados Unidos, México, Ecuador, Perú y Argentina. En Colombia cubre Costa Colombiana, Antioquia, Santander, Bogotá D.C., Eje Cafetero y Sur del país.',
    '["Inteligente: optimización de procesos con IA","Ágil: despliegue rápido con infraestructura orientada al negocio","Proactivo: modernización de sistemas legados antes de que fallen","Seguro: operaciones técnicas gestionadas por expertos con protección de datos"]'::jsonb,
    '["Semana","Ecopetrol","Colchones El Dorado","DIAN"]'::jsonb,
    '["Microsoft","Databricks","VMware","Veeam","Acronis","Fortinet"]'::jsonb,
    '["Partner del año – Migración a Cloud (CloudVerse)","Premio a la Excelencia en Migración hacia Azure 2023 – TD Synnex","Microsoft Partner of the Year Awards 2023, 2024 y finalista 2025"]'::jsonb,
    '{"whatsapp":"+57 317 427 0148","web":"https://www.gotocloud.ai","linkedin":"https://www.linkedin.com/company/gotocloudsas"}'::jsonb
)
ON CONFLICT (id) DO NOTHING;

-- 2. Servicios
INSERT INTO public.servicios (id, nombre, descripcion, beneficios, para_quien) VALUES
(
    'cloud_computing',
    'Servicios en la Nube',
    'Migración y gestión de infraestructura en Microsoft Azure. Arquitecturas híbridas, multicloud y listas para IA.',
    '["Migración guiada a Azure con respaldo experto","FinOps: visibilidad y control total del gasto en tiempo real","Gobierno y seguridad integrados desde el primer despliegue","Arquitecturas escalables: híbridas, multicloud o nativas en Azure","Alta disponibilidad y recuperación ante fallos","Automatización cloud-native para reducir errores operativos","Hasta 40% de ahorro en costos operativos"]'::jsonb,
    '{"pymes":["Migración rápida y sin fricciones","Escalabilidad sin perder control","Ahorro de costos con FinOps","Infraestructura lista para IA"],"corporativos":["Gobernanza y seguridad avanzada","Arquitecturas resilientes y multi-región","Integración con sistemas heredados","Múltiples zonas geográficas"]}'::jsonb
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.servicios (id, nombre, descripcion, pilares, metodologias, alcance, reportes, beneficios) VALUES
(
    'servicios_administrados',
    'Servicios Administrados de TI',
    'Gestión 24/7 de infraestructura cloud con soporte proactivo, monitoreo continuo y mejores prácticas en Azure. El equipo cliente se enfoca en el negocio mientras GoToCloud opera la tecnología.',
    '["Estabilidad","Optimización","Seguridad"]'::jsonb,
    '["ITIL","Scrum","Well-Architected Framework (WAF)","Cloud Adoption Framework (CAF)","FinOps"]'::jsonb,
    '["Resolución de incidentes y gestión de problemas","Configuración de infraestructura y automatización","Estrategias de backup y recuperación ante desastres","Evaluación de postura de seguridad de red","Análisis de optimización de costos","Mantenimiento y actualizaciones de sistemas"]'::jsonb,
    '["12 informes mensuales de validación operacional con KPI/SLA","4 informes trimestrales de arquitectura e innovación","Seguimiento de incidentes y recomendaciones correctivas"]'::jsonb,
    '["Monitoreo 24/7 de toda la infraestructura","Procesos proactivos que previenen caídas antes de que ocurran","Liberación del equipo interno para actividades estratégicas","Cumplimiento de los más altos estándares de seguridad"]'::jsonb
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.servicios (id, nombre, descripcion, especializaciones) VALUES
(
    'modernizacion_apps',
    'Modernización de Aplicaciones',
    'Transformación de entornos legados en soluciones modernas, integradas y preparadas para innovar en Microsoft Azure con IA.',
    '["Migración de aplicaciones empresariales a Microsoft Azure","Desarrollo y modernización de apps con IA en Azure","Migración de infraestructura y bases de datos","Azure VMware Solution (mover VMs VMware directamente a Azure)","Infraestructura de escritorios virtuales (VDI)"]'::jsonb
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.servicios (id, nombre, descripcion, especializaciones, partners) VALUES
(
    'seguridad',
    'Seguridad en la Nube',
    'Protección de datos, identidades y cargas de trabajo en la nube con los más altos estándares de seguridad y cumplimiento normativo.',
    '["Protección contra amenazas en Microsoft (especialización avanzada)","Gestión bajo estándares de seguridad internacionales","Cumplimiento normativo desde el primer despliegue"]'::jsonb,
    '["Fortinet","Acronis","Microsoft Defender","Azure Sentinel"]'::jsonb
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.servicios (id, nombre, descripcion, especializaciones, partners) VALUES
(
    'datos',
    'Servicios de Datos',
    'Orquestación y gestión de datos para decisiones más inteligentes, seguras y escalables. Analítica avanzada e IA/ML en Microsoft Azure.',
    '["Analítica avanzada con Power BI y Azure","IA y aprendizaje automático en Microsoft Azure (especialización avanzada)","Gestión de más de 1 PB de datos para decisiones estratégicas"]'::jsonb,
    '["Databricks","Microsoft Azure"]'::jsonb
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.servicios (id, nombre, descripcion) VALUES
(
    'soluciones_saas',
    'Soluciones SaaS',
    'Productos de software propios de GoToCloud para necesidades empresariales específicas.'
)
ON CONFLICT (id) DO NOTHING;

-- 3. Productos SaaS
INSERT INTO public.productos_saas (id, nombre, descripcion, para_quien, funcionalidades, beneficios) VALUES
(
    'karman',
    'Kármán Reporting Hub',
    'Portal web para gestionar y visualizar dashboards de Power BI de forma organizada, con control de acceso por usuario y departamento.',
    'Organizaciones que usan Power BI y necesitan distribuir reportes a múltiples usuarios sin que todos tengan licencia Pro individual.',
    '["Presentación organizada de tableros Power BI","Control granular de acceso por usuario y rol","Integración con Azure Active Directory","Interfaz web intuitiva, sin conocimientos técnicos avanzados"]'::jsonb,
    '["Ahorro significativo en licencias Power BI Pro","Democratización de datos: más usuarios acceden a la misma información","Cada área ve solo los reportes relevantes para su función","Integración fluida con infraestructura Azure existente"]'::jsonb
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.productos_saas (id, nombre, descripcion, para_quien, funcionalidades, beneficios, seguridad) VALUES
(
    'oasis',
    'OASIS AI',
    'Plataforma SaaS sobre Microsoft Azure que automatiza procesos con IA, extrae información de documentos no estructurados (facturas, contratos, correos, imágenes) y genera insights para la toma de decisiones.',
    'Empresas del sector financiero, retail, legal, y cualquier organización que gestione grandes volúmenes de documentos o datos no estructurados.',
    '["Extracción automática de datos de documentos (facturas, contratos, reportes)","Análisis de datos no estructurados con Azure Cognitive Search y Azure OpenAI","Generación de resúmenes automáticos e identificación de tendencias","Interfaz web Django intuitiva, sin conocimientos técnicos"]'::jsonb,
    '["40% de reducción en tiempo de gestión documental","25-30% de disminución en costos operativos","Eliminación de entrada manual de datos y esfuerzos duplicados","Mejor ROI con decisiones basadas en datos reales","Escalable: crece con la empresa sin fricción"]'::jsonb,
    '["Autenticación multifactor (MFA)","Cifrado AES-256","Monitoreo con Azure Sentinel","Cumplimiento GDPR, CCPA y SOC 2"]'::jsonb
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.productos_saas (id, nombre, descripcion, para_quien, beneficios) VALUES
(
    'dataloom',
    'DataLoom',
    'Herramienta para orquestar datos empresariales de múltiples fuentes, permitiendo decisiones más inteligentes, seguras y escalables.',
    'Empresas que necesitan centralizar datos de múltiples fuentes para tomar decisiones estratégicas.',
    '["Centralización de datos de múltiples fuentes","Decisiones estratégicas basadas en información consolidada","Escalabilidad con el crecimiento del negocio"]'::jsonb
)
ON CONFLICT (id) DO NOTHING;

-- 4. Métricas
INSERT INTO public.metricas (clave, valor) VALUES
    ('empresas_transformadas', 'Más de 100 empresas transformadas con soluciones en la nube y datos'),
    ('servidores_migrados', 'Más de 500 servidores migrados a Azure con 0 horas de downtime'),
    ('satisfaccion_cliente', '95% de satisfacción del cliente en cada proyecto'),
    ('ahorro_costos_cloud', 'Hasta 40% de ahorro en costos operativos con FinOps'),
    ('ahorro_oasis', '25-30% de reducción en costos operativos con OASIS AI'),
    ('reduccion_tiempo_oasis', '40% de reducción en tiempo de gestión documental con OASIS AI'),
    ('datos_gestionados', 'Más de 1 PB de datos gestionados para decisiones estratégicas'),
    ('cargas_modernizadas', 'Más de 200 cargas de trabajo modernizadas a IaaS y PaaS en Azure')
ON CONFLICT (clave) DO NOTHING;

-- =============================================================
--  Verificación
-- =============================================================
SELECT 'empresa' AS tabla, COUNT(*) AS filas FROM public.empresa
UNION ALL
SELECT 'servicios', COUNT(*) FROM public.servicios
UNION ALL
SELECT 'metricas', COUNT(*) FROM public.metricas
UNION ALL
SELECT 'productos_saas', COUNT(*) FROM public.productos_saas
UNION ALL
SELECT 'clientes', COUNT(*) FROM public.clientes
ORDER BY tabla;
