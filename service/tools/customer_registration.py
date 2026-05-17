# =============================================================
#  T001 — Customer Registration Tool
#  registrar_datos_cliente(nombre, cedula, empresa, telefono)
# =============================================================

from __future__ import annotations

import sys
from datetime import datetime, timezone
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
    "name": "registrar_datos_cliente",
    "description": (
        "Registra los datos del cliente al inicio de la llamada: nombre completo, cédula, "
        "empresa donde trabaja y teléfono de contacto. "
        "SIEMPRE llama esta tool al comienzo de la conversación, antes de responder "
        "cualquier otra pregunta. Recoge todos los campos antes de llamarla.\n\n"
        "COMPORTAMIENTO: La cédula es única. Si el cliente YA EXISTE (llamada recurrente), "
        "la tool actualiza sus datos y retorna ya_registrado=true con el ID existente. "
        "Si es NUEVO, lo crea y retorna ya_registrado=false. "
        "En ambos casos retorna el cliente_id para usar en otras tools."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "nombre": {
                "type": "string",
                "description": "Nombre completo del cliente.",
            },
            "cedula": {
                "type": "string",
                "description": "Número de cédula o documento de identidad del cliente.",
            },
            "empresa": {
                "type": "string",
                "description": "Nombre de la empresa u organización donde trabaja el cliente.",
            },
            "telefono": {
                "type": "string",
                "description": "Número de teléfono o celular de contacto del cliente.",
            },
        },
        "required": ["nombre", "cedula"],
    },
}


def execute(
    args: dict[str, Any],
    session: Any,
    kb: dict[str, Any],
) -> dict[str, Any]:
    """Register customer data. Creates or updates client in Supabase."""
    nombre_cliente = args.get("nombre", "").strip()
    cedula = args.get("cedula", "").strip()
    empresa_cliente = args.get("empresa", "").strip()
    telefono_cliente = args.get("telefono", "").strip()

    # Update session state
    session.nombre = nombre_cliente
    session.cedula = cedula
    session.empresa = empresa_cliente
    session.telefono = telefono_cliente
    session.mark_started()

    cliente_id: int | None = None
    ya_registrado = False

    if supabase is not None:
        try:
            # 1. Buscar por cédula (es UNIQUE)
            existente = (
                supabase.table("clientes")
                .select("id")
                .eq("cedula", cedula)
                .execute()
            )
            if existente.data and len(existente.data) > 0:
                # Ya existe → UPDATE
                cliente_id = existente.data[0]["id"]
                update_row: dict[str, Any] = {}
                if nombre_cliente:
                    update_row["nombre"] = nombre_cliente
                if empresa_cliente:
                    update_row["empresa"] = empresa_cliente
                if telefono_cliente:
                    update_row["telefono"] = telefono_cliente
                update_row["updated_at"] = datetime.now(timezone.utc).isoformat()
                (
                    supabase.table("clientes")
                    .update(update_row)
                    .eq("id", cliente_id)
                    .execute()
                )
                ya_registrado = True
                session.cliente_id = cliente_id
                print(f"[Supabase] Cliente ACTUALIZADO: id={cliente_id}, cedula={cedula}")
            else:
                # No existe → INSERT
                row: dict[str, Any] = {"nombre": nombre_cliente, "cedula": cedula}
                if empresa_cliente:
                    row["empresa"] = empresa_cliente
                if telefono_cliente:
                    row["telefono"] = telefono_cliente
                resultado = supabase.table("clientes").insert(row).execute()
                if resultado.data and len(resultado.data) > 0:
                    cliente_id = resultado.data[0]["id"]
                    session.cliente_id = cliente_id
                    print(f"[Supabase] Cliente NUEVO: id={cliente_id}, cedula={cedula}")
                else:
                    print(f"[Supabase] Cliente insertado sin ID")
        except Exception as ex:
            print(f"[Supabase] Error al registrar cliente: {ex}")
    else:
        print(
            f"[BD] Cliente registrado (sin Supabase): "
            f"nombre={nombre_cliente!r}, cedula={cedula!r}"
        )

    response: dict[str, Any] = {
        "registrado": True,
        "ya_registrado": ya_registrado,
        "nombre": nombre_cliente,
        "cedula": cedula,
        "empresa": empresa_cliente,
        "telefono": telefono_cliente,
    }
    if ya_registrado:
        response["mensaje"] = (
            f"Cliente ya registrado. Datos actualizados para {nombre_cliente}."
        )
    else:
        response["mensaje"] = (
            f"Datos registrados correctamente para {nombre_cliente}."
        )
    if cliente_id is not None:
        response["cliente_id"] = cliente_id

    return response
