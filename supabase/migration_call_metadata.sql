-- =============================================================
--  Migration: Metadata de Llamadas (call-metadata)
--  Ejecutar en: https://supabase.com/dashboard/project/nzeruwamlpacikmqtcja/sql/new
--  Idempotente: seguro de ejecutar aunque ya se haya corrido
-- =============================================================

-- 1. Extender tabla clientes
ALTER TABLE public.clientes
    ADD COLUMN IF NOT EXISTS empresa   TEXT,
    ADD COLUMN IF NOT EXISTS telefono  TEXT,
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT now();

COMMENT ON COLUMN public.clientes.empresa   IS 'Empresa u organización del cliente';
COMMENT ON COLUMN public.clientes.telefono  IS 'Teléfono de contacto del cliente';
COMMENT ON COLUMN public.clientes.updated_at IS 'Última actualización del registro';

-- 2. Crear tabla llamadas
CREATE TABLE IF NOT EXISTS public.llamadas (
    id                  SERIAL PRIMARY KEY,
    cliente_id          INTEGER NOT NULL REFERENCES public.clientes(id) ON DELETE CASCADE,
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

COMMENT ON TABLE  public.llamadas IS 'Metadata de cada llamada: resumen, intención, score, servicios de interés';
COMMENT ON COLUMN public.llamadas.intention IS 'Intención de compra: fria (consulta), calida (interés), caliente (necesidad inmediata)';
COMMENT ON COLUMN public.llamadas.score_lead IS 'Probabilidad de cierre 0-100';

-- 3. Índice para búsquedas por cliente
CREATE INDEX IF NOT EXISTS idx_llamadas_cliente_id ON public.llamadas(cliente_id);

-- 4. Políticas RLS
ALTER TABLE public.llamadas ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "anon_insert_llamadas" ON public.llamadas;
CREATE POLICY "anon_insert_llamadas" ON public.llamadas
    FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "anon_select_llamadas" ON public.llamadas;
CREATE POLICY "anon_select_llamadas" ON public.llamadas
    FOR SELECT USING (true);

-- =============================================================
--  Verificación
-- =============================================================
SELECT 'clientes' AS tabla, COUNT(*) AS filas FROM public.clientes
UNION ALL
SELECT 'llamadas', COUNT(*) FROM public.llamadas
ORDER BY tabla;
