# =============================================================
#  T003 — Services Info Tool
#  obtener_servicios(servicio="todos")
# =============================================================

from __future__ import annotations

from typing import Any


TOOL_DECLARATION: dict[str, Any] = {
    "name": "obtener_servicios",
    "description": (
        "Retorna información detallada de los servicios de GoToCloud. Úsala cuando "
        "pregunten qué servicios ofrecen, qué hacen en la nube, cómo pueden ayudar, "
        "o por un servicio específico."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "servicio": {
                "type": "string",
                "description": "Servicio específico a consultar, o 'todos' para ver todos.",
                "enum": [
                    "cloud_computing",
                    "modernizacion_apps",
                    "seguridad",
                    "servicios_administrados",
                    "datos",
                    "soluciones_saas",
                    "todos",
                ],
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
    """Return service information, filtered by service ID or all services."""
    servicios = kb["servicios"]
    servicio = args.get("servicio", "todos")

    if servicio == "todos":
        return {
            "servicios": [
                {
                    "id": k,
                    "nombre": v.get("nombre"),
                    "descripcion": v.get("descripcion"),
                }
                for k, v in servicios.items()
            ]
        }

    if servicio in servicios:
        return servicios[servicio]

    return {"error": f"Servicio '{servicio}' no encontrado."}
