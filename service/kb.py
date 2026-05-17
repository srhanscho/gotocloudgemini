# =============================================================
#  GOTOCLOUD KNOWLEDGE BASE
#  Extracted from gotocloud_voicebot_tool.py — shared read-only data
# =============================================================

from __future__ import annotations

from typing import Any

GOTOCLOUD_KB: dict[str, Any] = {
    "empresa": {
        "nombre": "GoToCloud",
        "descripcion": (
            "GoToCloud es una empresa colombiana especializada en transformación digital "
            "mediante soluciones en la nube con foco en Microsoft Azure. Ayuda a empresas "
            "a migrar, modernizar y optimizar su operación tecnológica con seguridad e IA."
        ),
        "presencia": (
            "Opera en toda Latinoamérica: Colombia, Estados Unidos, México, Ecuador, Perú "
            "y Argentina. En Colombia cubre Costa Colombiana, Antioquia, Santander, "
            "Bogotá D.C., Eje Cafetero y Sur del país."
        ),
        "propuesta_valor": [
            "Inteligente: optimización de procesos con IA",
            "Ágil: despliegue rápido con infraestructura orientada al negocio",
            "Proactivo: modernización de sistemas legados antes de que fallen",
            "Seguro: operaciones técnicas gestionadas por expertos con protección de datos",
        ],
        "clientes_destacados": ["Semana", "Ecopetrol", "Colchones El Dorado", "DIAN"],
        "partners": ["Microsoft", "Databricks", "VMware", "Veeam", "Acronis", "Fortinet"],
        "reconocimientos": [
            "Partner del año – Migración a Cloud (CloudVerse)",
            "Premio a la Excelencia en Migración hacia Azure 2023 – TD Synnex",
            "Microsoft Partner of the Year Awards 2023, 2024 y finalista 2025",
        ],
        "contacto": {
            "whatsapp": "+57 317 427 0148",
            "web": "https://www.gotocloud.ai",
            "linkedin": "https://www.linkedin.com/company/gotocloudsas",
        },
    },

    "servicios": {
        "cloud_computing": {
            "nombre": "Servicios en la Nube",
            "descripcion": (
                "Migración y gestión de infraestructura en Microsoft Azure. Arquitecturas "
                "híbridas, multicloud y listas para IA."
            ),
            "beneficios": [
                "Migración guiada a Azure con respaldo experto",
                "FinOps: visibilidad y control total del gasto en tiempo real",
                "Gobierno y seguridad integrados desde el primer despliegue",
                "Arquitecturas escalables: híbridas, multicloud o nativas en Azure",
                "Alta disponibilidad y recuperación ante fallos",
                "Automatización cloud-native para reducir errores operativos",
                "Hasta 40% de ahorro en costos operativos",
            ],
            "para_quien": {
                "pymes": [
                    "Migración rápida y sin fricciones",
                    "Escalabilidad sin perder control",
                    "Ahorro de costos con FinOps",
                    "Infraestructura lista para IA",
                ],
                "corporativos": [
                    "Gobernanza y seguridad avanzada",
                    "Arquitecturas resilientes y multi-región",
                    "Integración con sistemas heredados",
                    "Múltiples zonas geográficas",
                ],
            },
        },

        "servicios_administrados": {
            "nombre": "Servicios Administrados de TI",
            "descripcion": (
                "Gestión 24/7 de infraestructura cloud con soporte proactivo, monitoreo "
                "continuo y mejores prácticas en Azure. El equipo cliente se enfoca en el "
                "negocio mientras GoToCloud opera la tecnología."
            ),
            "pilares": ["Estabilidad", "Optimización", "Seguridad"],
            "metodologias": ["ITIL", "Scrum", "Well-Architected Framework (WAF)", "Cloud Adoption Framework (CAF)", "FinOps"],
            "alcance": [
                "Resolución de incidentes y gestión de problemas",
                "Configuración de infraestructura y automatización",
                "Estrategias de backup y recuperación ante desastres",
                "Evaluación de postura de seguridad de red",
                "Análisis de optimización de costos",
                "Mantenimiento y actualizaciones de sistemas",
            ],
            "reportes": [
                "12 informes mensuales de validación operacional con KPI/SLA",
                "4 informes trimestrales de arquitectura e innovación",
                "Seguimiento de incidentes y recomendaciones correctivas",
            ],
            "beneficios": [
                "Monitoreo 24/7 de toda la infraestructura",
                "Procesos proactivos que previenen caídas antes de que ocurran",
                "Liberación del equipo interno para actividades estratégicas",
                "Cumplimiento de los más altos estándares de seguridad",
            ],
        },

        "modernizacion_apps": {
            "nombre": "Modernización de Aplicaciones",
            "descripcion": (
                "Transformación de entornos legados en soluciones modernas, integradas "
                "y preparadas para innovar en Microsoft Azure con IA."
            ),
            "especializaciones": [
                "Migración de aplicaciones empresariales a Microsoft Azure",
                "Desarrollo y modernización de apps con IA en Azure",
                "Migración de infraestructura y bases de datos",
                "Azure VMware Solution (mover VMs VMware directamente a Azure)",
                "Infraestructura de escritorios virtuales (VDI)",
            ],
        },

        "seguridad": {
            "nombre": "Seguridad en la Nube",
            "descripcion": (
                "Protección de datos, identidades y cargas de trabajo en la nube con "
                "los más altos estándares de seguridad y cumplimiento normativo."
            ),
            "especializaciones": [
                "Protección contra amenazas en Microsoft (especialización avanzada)",
                "Gestión bajo estándares de seguridad internacionales",
                "Cumplimiento normativo desde el primer despliegue",
            ],
            "partners": ["Fortinet", "Acronis", "Microsoft Defender", "Azure Sentinel"],
        },

        "datos": {
            "nombre": "Servicios de Datos",
            "descripcion": (
                "Orquestación y gestión de datos para decisiones más inteligentes, "
                "seguras y escalables. Analítica avanzada e IA/ML en Microsoft Azure."
            ),
            "especializaciones": [
                "Analítica avanzada con Power BI y Azure",
                "IA y aprendizaje automático en Microsoft Azure (especialización avanzada)",
                "Gestión de más de 1 PB de datos para decisiones estratégicas",
            ],
            "partners": ["Databricks", "Microsoft Azure"],
        },

        "soluciones_saas": {
            "nombre": "Soluciones SaaS",
            "descripcion": "Productos de software propios de GoToCloud para necesidades empresariales específicas.",
            "productos": {
                "karman": {
                    "nombre": "Kármán Reporting Hub",
                    "descripcion": (
                        "Portal web para gestionar y visualizar dashboards de Power BI de "
                        "forma organizada, con control de acceso por usuario y departamento."
                    ),
                    "para_quien": (
                        "Organizaciones que usan Power BI y necesitan distribuir reportes "
                        "a múltiples usuarios sin que todos tengan licencia Pro individual."
                    ),
                    "funcionalidades": [
                        "Presentación organizada de tableros Power BI",
                        "Control granular de acceso por usuario y rol",
                        "Integración con Azure Active Directory",
                        "Interfaz web intuitiva, sin conocimientos técnicos avanzados",
                    ],
                    "beneficios": [
                        "Ahorro significativo en licencias Power BI Pro",
                        "Democratización de datos: más usuarios acceden a la misma información",
                        "Cada área ve solo los reportes relevantes para su función",
                        "Integración fluida con infraestructura Azure existente",
                    ],
                },
                "oasis": {
                    "nombre": "OASIS AI",
                    "descripcion": (
                        "Plataforma SaaS avanzada que automatiza procesos con IA, extrae información "
                        "de documentos no estructurados (facturas, contratos, correos, imágenes) "
                        "y genera insights para la toma de decisiones, utilizando tecnologías "
                        "de Microsoft Azure, Azure OpenAI y Azure Cognitive Services."
                    ),
                    "para_quien": (
                        "Empresas del sector financiero, retail, legal, y cualquier organización "
                        "que gestione grandes volúmenes de documentos o datos no estructurados."
                    ),
                    "funcionalidades": [
                        "Automatización de procesos: extracción de información de documentos (facturas, contratos, reportes)",
                        "Análisis avanzado de datos no estructurados con Azure Cognitive Search y Azure OpenAI",
                        "Generación de insights: resúmenes automáticos, identificación de tendencias y recomendaciones",
                        "Interfaz web intuitiva desarrollada con Django",
                    ],
                    "beneficios": [
                        "Mejora en la productividad: 40% de reducción en tiempo de gestión documental",
                        "Optimización de recursos: 25-30% de disminución en costos operativos",
                        "Eliminación de entrada manual de datos y esfuerzos duplicados",
                        "Mejor ROI con decisiones basadas en datos reales",
                        "Escalable: crece con la empresa sin fricción",
                    ],
                    "seguridad": [
                        "Autenticación multifactor (MFA) con Azure Active Directory B2C",
                        "Cifrado AES-256 en tránsito y en reposo",
                        "Monitoreo continuo con Azure Sentinel",
                        "Cumplimiento GDPR, CCPA y SOC 2",
                    ],
                },
                "dataloom": {
                    "nombre": "DataLoom",
                    "descripcion": (
                        "Solución SaaS potente para gestionar, buscar y acceder de manera eficiente "
                        "a archivos almacenados en la nube, utilizando tecnologías de Azure para "
                        "escalabilidad, seguridad y accesibilidad."
                    ),
                    "beneficios": [
                        "Gestión, búsqueda y acceso eficiente a archivos en la nube",
                        "Indexación de metadatos para búsqueda avanzada (nombre, extensión, tipo, fecha)",
                        "Integración con Azure Storage y Azure Active Directory B2C",
                        "Implementación rápida (menos de 6 horas) y personalizable",
                        "Disponibilidad del 99.95% respaldada por Azure",
                    ],
                },
            },
        },
    },

    "metricas": {
        "empresas_transformadas": "Más de 100 empresas transformadas con soluciones en la nube y datos",
        "servidores_migrados": "Más de 500 servidores migrados a Azure con 0 horas de downtime",
        "satisfaccion_cliente": "95% de satisfacción del cliente en cada proyecto",
        "ahorro_costos_cloud": "Hasta 40% de ahorro en costos operativos con FinOps",
        "ahorro_oasis": "25-30% de reducción en costos operativos con OASIS AI",
        "reduccion_tiempo_oasis": "40% de reducción en tiempo de gestión documental con OASIS AI",
        "datos_gestionados": "Más de 1 PB de datos gestionados para decisiones estratégicas",
        "cargas_modernizadas": "Más de 200 cargas de trabajo modernizadas a IaaS y PaaS en Azure",
    },
}


# ─────────────────────────────────────────────
# TYPED ACCESSORS
# ─────────────────────────────────────────────

def get_service(service_id: str) -> dict[str, Any]:
    """Return a service definition by ID, or empty dict if not found."""
    return GOTOCLOUD_KB["servicios"].get(service_id, {})


def get_product(product_id: str) -> dict[str, Any]:
    """Return a SaaS product definition by ID, or empty dict if not found."""
    return GOTOCLOUD_KB["servicios"]["soluciones_saas"]["productos"].get(product_id, {})


def get_contact() -> dict[str, str]:
    """Return company contact information."""
    return GOTOCLOUD_KB["empresa"]["contacto"].copy()


def get_metrics() -> dict[str, str]:
    """Return all company metrics."""
    return GOTOCLOUD_KB["metricas"].copy()


def get_company_info() -> dict[str, Any]:
    """Return general company information."""
    return GOTOCLOUD_KB["empresa"].copy()


__all__ = [
    "GOTOCLOUD_KB",
    "get_service",
    "get_product",
    "get_contact",
    "get_metrics",
    "get_company_info",
]
