# =============================================================
#  T004 — SaaS Products Tool
#  obtener_producto_saas(producto="todos")
# =============================================================

from __future__ import annotations

from typing import Any


TOOL_DECLARATION: dict[str, Any] = {
    "name": "obtener_producto_saas",
    "description": (
        "Retorna información detallada de los productos SaaS propios de GoToCloud: "
        "Kármán Reporting Hub (portal de Power BI), OASIS AI (automatización con IA) "
        "y DataLoom (orquestación de datos). Úsala cuando pregunten por productos de "
        "software, soluciones propias o mencionen alguno de esos nombres."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "producto": {
                "type": "string",
                "description": "Producto a consultar.",
                "enum": ["karman", "oasis", "dataloom", "todos"],
            }
        },
        "required": [],
    },
}


def execute(
    args: dict[str, Any],
    session: Any,
    kb: dict[str, Any],
) -> dict[str, Any]:
    """Return SaaS product information, filtered by product ID or all products."""
    productos = kb["servicios"]["soluciones_saas"]["productos"]
    producto = args.get("producto", "todos")

    if producto == "todos":
        return {"productos": productos}

    if producto in productos:
        return productos[producto]

    return {"error": f"Producto '{producto}' no encontrado."}
