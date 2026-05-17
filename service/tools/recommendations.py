# =============================================================
#  T007 — Recommendations Tool
#  obtener_beneficios_para_cliente(tipo_empresa, necesidad)
# =============================================================

from __future__ import annotations

from typing import Any


TOOL_DECLARATION: dict[str, Any] = {
    "name": "obtener_beneficios_para_cliente",
    "description": (
        "Recomienda servicios de GoToCloud según el tipo de empresa y la necesidad "
        "detectada. Úsala cuando el cliente cuento su situación o problema y necesites "
        "recomendar la solución más adecuada."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "tipo_empresa": {
                "type": "string",
                "enum": ["pyme", "corporativo", "gobierno", "cualquiera"],
            },
            "necesidad": {
                "type": "string",
                "description": "Área de necesidad: 'reducir costos', 'seguridad', 'migración', 'datos', 'IA', 'documentos', etc.",
            },
        },
        "required": [],
    },
}


def execute(
    args: dict[str, Any],
    session: Any,
    kb: dict[str, Any],
) -> dict[str, Any]:
    """Recommend services based on company type and detected need."""
    s = kb["servicios"]
    productos = s["soluciones_saas"]["productos"]
    tipo = args.get("tipo_empresa", "cualquiera")
    necesidad = args.get("necesidad", "").lower()
    recomendaciones: list[dict[str, Any]] = []

    if any(k in necesidad for k in ["costo", "ahorro", "finops", "gasto"]):
        recomendaciones.append({
            "servicio": "Servicios en la Nube con FinOps",
            "razon": "GoToCloud ofrece hasta un 40% de ahorro en costos operativos mediante FinOps.",
            "beneficios": s["cloud_computing"].get("beneficios", []),
        })

    if any(k in necesidad for k in ["document", "factura", "contrato", "papeleo", "manual"]):
        recomendaciones.append({
            "servicio": "OASIS AI",
            "razon": "OASIS AI reduce en 40% el tiempo de gestión documental y en 25-30% los costos operativos.",
            "beneficios": productos["oasis"].get("beneficios", []),
        })

    if any(k in necesidad for k in ["reporte", "dashboard", "power bi", "analítica", "datos"]):
        recomendaciones.append({
            "servicio": "Kármán Reporting Hub + Servicios de Datos",
            "razon": "Kármán permite distribuir reportes Power BI con ahorro en licencias.",
            "beneficios": productos["karman"].get("beneficios", []),
        })

    if any(k in necesidad for k in ["seguridad", "protección", "cumplimiento", "hack"]):
        recomendaciones.append({
            "servicio": "Seguridad en la Nube",
            "razon": "GoToCloud tiene especialización avanzada en protección contra amenazas Microsoft.",
            "beneficios": s["seguridad"].get("especializaciones", []),
        })

    if any(k in necesidad for k in ["migración", "migracion", "nube", "azure", "mover"]):
        beneficios_tipo = (
            s["cloud_computing"]["para_quien"].get("pymes", [])
            if tipo == "pyme"
            else s["cloud_computing"]["para_quien"].get("corporativos", [])
        )
        recomendaciones.append({
            "servicio": "Servicios en la Nube",
            "razon": "GoToCloud ha migrado más de 500 servidores a Azure con 0 horas de downtime.",
            "beneficios": beneficios_tipo,
        })

    if any(k in necesidad for k in ["ia", "inteligencia artificial", "automatiz"]):
        recomendaciones.append({
            "servicio": "OASIS AI + Modernización de Aplicaciones con IA",
            "razon": "GoToCloud tiene especialización avanzada en IA y ML sobre Azure.",
            "beneficios": s["datos"].get("especializaciones", []),
        })

    if any(k in necesidad for k in ["soporte", "administr", "mantenimiento", "operar"]):
        recomendaciones.append({
            "servicio": "Servicios Administrados de TI",
            "razon": "GoToCloud opera la infraestructura 24/7 para que el equipo se enfoque en el negocio.",
            "beneficios": s["servicios_administrados"].get("beneficios", []),
        })

    if not recomendaciones:
        recomendaciones = [{
            "servicio": "Consultoría GoToCloud",
            "razon": "GoToCloud diseña soluciones personalizadas según tu industria y necesidades.",
            "beneficios": [
                "95% de satisfacción del cliente",
                "Más de 100 empresas transformadas en Latinoamérica",
                "Partner certificado Microsoft con múltiples especializaciones avanzadas",
            ],
        }]

    return {
        "tipo_empresa": tipo,
        "necesidad": necesidad or "general",
        "recomendaciones": recomendaciones,
    }
