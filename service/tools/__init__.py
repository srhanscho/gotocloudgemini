# =============================================================
#  TOOL REGISTRY — Aggregates tool declarations for Gemini Live
# =============================================================
# Each tool module (added in Batch 2) exports a `tool` dict with its
# Gemini function declaration. This module collects them into GOTOCLOUD_TOOLS.
# =============================================================

from __future__ import annotations

from typing import Any

# Tool declarations registry — populated by tool modules as they are added.
# Batch 2 modules will import this and append their declarations.
_tool_declarations: list[dict[str, Any]] = []


def register_tool(declaration: dict[str, Any]) -> None:
    """Register a tool declaration from a tool module."""
    _tool_declarations.append(declaration)


# Aggregate all registered declarations into the list Gemini Live expects.
# Currently empty — tool modules from Batch 2 will populate this at import time.
GOTOCLOUD_TOOLS: list[dict[str, Any]] = _tool_declarations


# ─────────────────────────────────────────────
# PLACEHOLDER: Batch 2 imports (T-004 → T-011)
# Uncomment as each tool module is created:
# ─────────────────────────────────────────────
# from .customer_registration import tool as _t_registrar  # noqa: F401
# from .company_info import tool as _t_empresa             # noqa: F401
# from .services_info import tool as _t_servicios          # noqa: F401
# from .saas_products import tool as _t_saas               # noqa: F401
# from .metrics_info import tool as _t_metricas            # noqa: F401
# from .contact_info import tool as _t_contacto            # noqa: F401
# from .recommendations import tool as _t_beneficios       # noqa: F401
# from .call_summary import tool as _t_resumen             # noqa: F401


__all__ = ["GOTOCLOUD_TOOLS", "register_tool"]
