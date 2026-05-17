# =============================================================
#  TOOL REGISTRY — Aggregates tool declarations for Gemini Live
# =============================================================
# Each tool module exports a `TOOL_DECLARATION` dict with its
# Gemini function declaration. This module collects them into GOTOCLOUD_TOOLS.
# =============================================================

from __future__ import annotations

from typing import Any

# ─────────────────────────────────────────────
# Tool declarations registry
# ─────────────────────────────────────────────
_tool_declarations: list[dict[str, Any]] = []


def register_tool(declaration: dict[str, Any]) -> None:
    """Register a tool declaration from a tool module."""
    _tool_declarations.append(declaration)


# ─────────────────────────────────────────────
# Batch 2 tool imports (T-004 → T-011)
# Each module registers its TOOL_DECLARATION on import.
# ─────────────────────────────────────────────
from .customer_registration import TOOL_DECLARATION as _t_registrar  # noqa: F401, E402
from .company_info import TOOL_DECLARATION as _t_empresa  # noqa: F401, E402
from .services_info import TOOL_DECLARATION as _t_servicios  # noqa: F401, E402
from .saas_products import TOOL_DECLARATION as _t_saas  # noqa: F401, E402
from .metrics_info import TOOL_DECLARATION as _t_metricas  # noqa: F401, E402
from .contact_info import TOOL_DECLARATION as _t_contacto  # noqa: F401, E402
from .recommendations import TOOL_DECLARATION as _t_beneficios  # noqa: F401, E402
from .call_summary import TOOL_DECLARATION as _t_resumen  # noqa: F401, E402

# Register all declarations
register_tool(_t_registrar)
register_tool(_t_empresa)
register_tool(_t_servicios)
register_tool(_t_saas)
register_tool(_t_metricas)
register_tool(_t_contacto)
register_tool(_t_beneficios)
register_tool(_t_resumen)

# Aggregate all registered declarations into the list Gemini Live expects.
GOTOCLOUD_TOOLS: list[dict[str, Any]] = _tool_declarations


# ─────────────────────────────────────────────
# Re-export tool functions for facade use
# ─────────────────────────────────────────────
from .customer_registration import execute as ejecutar_registrar_datos_cliente  # noqa: F401, E402
from .company_info import execute as ejecutar_obtener_informacion_empresa  # noqa: F401, E402
from .services_info import execute as ejecutar_obtener_servicios  # noqa: F401, E402
from .saas_products import execute as ejecutar_obtener_producto_saas  # noqa: F401, E402
from .metrics_info import execute as ejecutar_obtener_metricas  # noqa: F401, E402
from .contact_info import execute as ejecutar_obtener_contacto  # noqa: F401, E402
from .recommendations import execute as ejecutar_obtener_beneficios_para_cliente  # noqa: F401, E402
from .call_summary import execute as ejecutar_registrar_resumen_llamada  # noqa: F401, E402


__all__ = [
    "GOTOCLOUD_TOOLS",
    "register_tool",
    "ejecutar_registrar_datos_cliente",
    "ejecutar_obtener_informacion_empresa",
    "ejecutar_obtener_servicios",
    "ejecutar_obtener_producto_saas",
    "ejecutar_obtener_metricas",
    "ejecutar_obtener_contacto",
    "ejecutar_obtener_beneficios_para_cliente",
    "ejecutar_registrar_resumen_llamada",
]
