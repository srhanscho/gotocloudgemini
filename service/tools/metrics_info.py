# =============================================================
#  T005 — Metrics Info Tool
#  obtener_metricas()
# =============================================================

from __future__ import annotations

from typing import Any


TOOL_DECLARATION: dict[str, Any] = {
    "name": "obtener_metricas",
    "description": (
        "Retorna números concretos de impacto de GoToCloud: empresas atendidas, "
        "servidores migrados, ahorros, satisfacción del cliente. Úsala cuando pidan "
        "cifras, resultados o quieran saber cuánto pueden ahorrar."
    ),
    "parameters": {"type": "object", "properties": {}, "required": []},
}


def execute(
    args: dict[str, Any],
    session: Any,
    kb: dict[str, Any],
) -> dict[str, Any]:
    """Return all company metrics from the knowledge base."""
    return kb["metricas"].copy()
