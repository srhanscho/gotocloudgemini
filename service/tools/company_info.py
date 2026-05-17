# =============================================================
#  T002 — Company Info Tool
#  obtener_informacion_empresa()
# =============================================================

from __future__ import annotations

from typing import Any


TOOL_DECLARATION: dict[str, Any] = {
    "name": "obtener_informacion_empresa",
    "description": (
        "Retorna información general sobre GoToCloud: qué es, dónde opera, su propuesta "
        "de valor, clientes destacados, partners y reconocimientos. Úsala cuando pregunten "
        "quién es GoToCloud, dónde están o qué premios tienen."
    ),
    "parameters": {"type": "object", "properties": {}, "required": []},
}


def execute(
    args: dict[str, Any],
    session: Any,
    kb: dict[str, Any],
) -> dict[str, Any]:
    """Return general company information from the knowledge base."""
    e = kb["empresa"]
    return {
        "nombre": e["nombre"],
        "descripcion": e["descripcion"],
        "presencia": e["presencia"],
        "propuesta_valor": e["propuesta_valor"],
        "clientes_destacados": e["clientes_destacados"],
        "partners": e["partners"],
        "reconocimientos": e["reconocimientos"],
    }
