# =============================================================
#  T006 — Contact Info Tool
#  obtener_contacto()
# =============================================================

from __future__ import annotations

from typing import Any


TOOL_DECLARATION: dict[str, Any] = {
    "name": "obtener_contacto",
    "description": (
        "Retorna los datos de contacto de GoToCloud. Úsala cuando el cliente quiera "
        "hablar con un asesor, pedir una cotización o que lo llamen."
    ),
    "parameters": {"type": "object", "properties": {}, "required": []},
}


def execute(
    args: dict[str, Any],
    session: Any,
    kb: dict[str, Any],
) -> dict[str, Any]:
    """Return company contact information with a helper message."""
    contacto = kb["empresa"]["contacto"].copy()
    contacto["mensaje"] = (
        "Un asesor de GoToCloud puede orientarte y preparar una propuesta personalizada. "
        "Te pueden contactar por WhatsApp al +57 317 427 0148."
    )
    return contacto
