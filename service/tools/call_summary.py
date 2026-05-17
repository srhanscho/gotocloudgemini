# =============================================================
#  T008 — Call Summary Tool
#  registrar_resumen_llamada(resumen, intention, score_lead, ...)
# =============================================================

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Supabase import with fallback (same pattern as original)
try:
    from backend.supabase_client import supabase, is_connected
except ImportError:
    backend_path = Path(__file__).parent.parent.parent / "backend"
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    try:
        from supabase_client import supabase, is_connected
    except ImportError:
        supabase = None
        is_connected = lambda: False


TOOL_DECLARATION: dict[str, Any] = {
    "name": "registrar_resumen_llamada",
    "description": (
        "Guarda el resumen y metadata al final de la llamada. LLAMA CUANDO LA LLAMADA ESTÉ POR TERMINAR. "
        "Incluye toda la información obtenida durante la conversación."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "resumen": {
                "type": "string",
                "description": "Resumen breve de la conversación, qué preguntó, qué le interessó.",
            },
            "intention": {
                "type": "string",
                "enum": ["fria", "calida", "caliente"],
                "description": "'fria': solo consultas generales, 'calida': interés real pero sin urgencia, 'caliente': necesidad inmediata o presupuesto disponible",
            },
            "score_lead": {
                "type": "integer",
                "description": "Probabilidad de cierre 0-100. 0-30 baja, 31-60 media, 61-100 alta.",
            },
            "servicios_interes": {
                "type": "array",
                "items": {"type": "string"},
                "description": "IDs de servicios que le interesaron al cliente (cloud_computing, seguridad, etc.)",
            },
            "recomendaciones": {
                "type": "string",
                "description": "Recomendaciones para el vendedor que hará seguimiento",
            },
        },
        "required": ["resumen", "intention", "score_lead"],
    },
}


def execute(
    args: dict[str, Any],
    session: Any,
    kb: dict[str, Any],
) -> dict[str, Any]:
    """Register call summary in Supabase llamadas table."""
    resumen = args.get("resumen", "").strip()
    intention = args.get("intention", "calida")
    score_lead = args.get("score_lead", 50)
    servicios_interes = args.get("servicios_interes", [])
    recomendaciones = args.get("recomendaciones", "").strip()

    # Validar score_lead
    if score_lead < 0 or score_lead > 100:
        return {"error": "score_lead debe estar entre 0 y 100"}

    # Validar intention
    if intention not in ("fria", "calida", "caliente"):
        return {"error": "intention debe ser 'fria', 'calida' o 'caliente'"}

    # Obtener cliente_id de la session
    cliente_id = session.cliente_id
    cedula = session.cedula

    # Si no hay cliente_id en session, buscar por cédula en Supabase
    if not cliente_id and cedula and supabase is not None:
        try:
            result = (
                supabase.table("clientes")
                .select("id")
                .eq("cedula", cedula)
                .execute()
            )
            if result.data and len(result.data) > 0:
                cliente_id = result.data[0]["id"]
        except Exception as ex:
            print(f"[Supabase] Error al buscar cliente por cédula: {ex}")

    if not cliente_id:
        return {
            "error": "No hay cliente registrado. Llama primero a registrar_datos_cliente."
        }

    # Insertar en tabla llamadas
    started_at = session.started_at
    row: dict[str, Any] = {
        "cliente_id": cliente_id,
        "resumen": resumen,
        "intention": intention,
        "score_lead": score_lead,
        "servicios_interes": servicios_interes or [],
        "recomendaciones": recomendaciones,
        "started_at": started_at,
    }

    if supabase is not None:
        try:
            resultado = supabase.table("llamadas").insert(row).execute()
            if resultado.data and len(resultado.data) > 0:
                llamada_id = resultado.data[0]["id"]
                print(f"[Supabase] Llamada registrada: id={llamada_id}")
                return {"registrado": True, "llamada_id": llamada_id}
            else:
                print(f"[Supabase] Llamada registrada sin ID")
                return {"registrado": True}
        except Exception as ex:
            print(f"[Supabase] Error al registrar llamada: {ex}")
            return {"error": f"Error al registrar llamada: {ex}"}
    else:
        print(
            f"[BD] Llamada registrada (sin Supabase): "
            f"cliente_id={cliente_id}, resumen={resumen!r}"
        )
        return {"registrado": True}
