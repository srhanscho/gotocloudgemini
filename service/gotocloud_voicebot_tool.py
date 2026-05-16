# =============================================================
#  GOTOCLOUD VOICEBOT TOOL — Compatible con Gemini Live
#  Agente: Camila | Empresa: GoToCloud
# =============================================================

from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import Any

# Import compatibility: funciona con sys.path (voice_to_voice.py) y package-relative (main.py)
try:
    from backend.supabase_client import supabase, is_connected
except ImportError:
    # Fallback: agregar backend al path si no está
    backend_path = Path(__file__).parent.parent / "backend"
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    try:
        from supabase_client import supabase, is_connected
    except ImportError:
        supabase = None
        is_connected = lambda: False

# ─────────────────────────────────────────────
# BASE DE CONOCIMIENTO
# ─────────────────────────────────────────────
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
                        "Plataforma SaaS sobre Microsoft Azure que automatiza procesos con IA, "
                        "extrae información de documentos no estructurados (facturas, contratos, "
                        "correos, imágenes) y genera insights para la toma de decisiones."
                    ),
                    "para_quien": (
                        "Empresas del sector financiero, retail, legal, y cualquier organización "
                        "que gestione grandes volúmenes de documentos o datos no estructurados."
                    ),
                    "funcionalidades": [
                        "Extracción automática de datos de documentos (facturas, contratos, reportes)",
                        "Análisis de datos no estructurados con Azure Cognitive Search y Azure OpenAI",
                        "Generación de resúmenes automáticos e identificación de tendencias",
                        "Interfaz web Django intuitiva, sin conocimientos técnicos",
                    ],
                    "beneficios": [
                        "40% de reducción en tiempo de gestión documental",
                        "25-30% de disminución en costos operativos",
                        "Eliminación de entrada manual de datos y esfuerzos duplicados",
                        "Mejor ROI con decisiones basadas en datos reales",
                        "Escalable: crece con la empresa sin fricción",
                    ],
                    "seguridad": [
                        "Autenticación multifactor (MFA)",
                        "Cifrado AES-256",
                        "Monitoreo con Azure Sentinel",
                        "Cumplimiento GDPR, CCPA y SOC 2",
                    ],
                },
                "dataloom": {
                    "nombre": "DataLoom",
                    "descripcion": (
                        "Herramienta para orquestar datos empresariales de múltiples fuentes, "
                        "permitiendo decisiones más inteligentes, seguras y escalables."
                    ),
                    "beneficios": [
                        "Centralización de datos de múltiples fuentes",
                        "Decisiones estratégicas basadas en información consolidada",
                        "Escalabilidad con el crecimiento del negocio",
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
# TOOLS PARA GEMINI LIVE
# ─────────────────────────────────────────────
GOTOCLOUD_TOOLS: list[dict[str, Any]] = [
    {
        "name": "registrar_datos_cliente",
        "description": (
            "Registra el nombre y número de cédula del cliente al inicio de la llamada. "
            "SIEMPRE llama esta tool al comienzo de la conversación, antes de responder "
            "cualquier otra pregunta. Necesitas preguntar el nombre completo y la cédula."
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
            },
            "required": ["nombre", "cedula"],
        },
    },
    {
        "name": "obtener_informacion_empresa",
        "description": (
            "Retorna información general sobre GoToCloud: qué es, dónde opera, su propuesta "
            "de valor, clientes destacados, partners y reconocimientos. Úsala cuando pregunten "
            "quién es GoToCloud, dónde están o qué premios tienen."
        ),
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
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
    },
    {
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
    },
    {
        "name": "obtener_metricas",
        "description": (
            "Retorna números concretos de impacto de GoToCloud: empresas atendidas, "
            "servidores migrados, ahorros, satisfacción del cliente. Úsala cuando pidan "
            "cifras, resultados o quieran saber cuánto pueden ahorrar."
        ),
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "obtener_contacto",
        "description": (
            "Retorna los datos de contacto de GoToCloud. Úsala cuando el cliente quiera "
            "hablar con un asesor, pedir una cotización o que lo llamen."
        ),
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "obtener_beneficios_para_cliente",
        "description": (
            "Recomienda servicios de GoToCloud según el tipo de empresa y la necesidad "
            "detectada. Úsala cuando el cliente cuente su situación o problema y necesites "
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
    },
]


# ─────────────────────────────────────────────
# HANDLERS
# ─────────────────────────────────────────────

# Almacén temporal de datos del cliente (el compañero conectará la BD)
_cliente_actual: dict[str, str] = {}


def _fallback(que: str) -> dict:
    """Fallback genérico para errores de base de datos."""
    return {"error": f"Base de datos no disponible. Intenta más tarde."}


def ejecutar_tool(nombre: str, args: dict[str, Any] | None = None) -> dict[str, Any]:
    args = args or {}

    if nombre == "registrar_datos_cliente":
        nombre_cliente = args.get("nombre", "").strip()
        cedula = args.get("cedula", "").strip()
        _cliente_actual["nombre"] = nombre_cliente
        _cliente_actual["cedula"] = cedula
        print(f"\n[BD] Cliente registrado: nombre={nombre_cliente!r}, cedula={cedula!r}")
        return {
            "registrado": True,
            "nombre": nombre_cliente,
            "cedula": cedula,
            "mensaje": f"Datos registrados correctamente para {nombre_cliente}.",
        }

    elif nombre == "obtener_informacion_empresa":
        try:
            if supabase is None:
                raise Exception("Cliente Supabase no inicializado")
            result = supabase.table("empresa").select("*").eq("id", 1).execute()
            if not result.data:
                return _fallback("información de la empresa")
            e = result.data[0]
            return {
                "nombre": e.get("nombre"),
                "descripcion": e.get("descripcion"),
                "presencia": e.get("presencia"),
                "propuesta_valor": e.get("propuesta_valor"),
                "clientes_destacados": e.get("clientes_destacados"),
                "partners": e.get("partners"),
                "reconocimientos": e.get("reconocimientos"),
            }
        except Exception as ex:
            print(f"[KB DB error] obtener_informacion_empresa: {ex}")
            return _fallback("información de la empresa")

    elif nombre == "obtener_servicios":
        try:
            if supabase is None:
                raise Exception("Cliente Supabase no inicializado")
            result = supabase.table("servicios").select("*").execute()
            if not result.data:
                return _fallback("servicios")
            servicios_dict = {row["id"]: row for row in result.data}
            servicio = args.get("servicio", "todos")
            if servicio == "todos":
                return {
                    "servicios": [
                        {"id": k, "nombre": v.get("nombre"), "descripcion": v.get("descripcion")}
                        for k, v in servicios_dict.items()
                    ]
                }
            if servicio in servicios_dict:
                return servicios_dict[servicio]
            return {"error": f"Servicio '{servicio}' no encontrado."}
        except Exception as ex:
            print(f"[KB DB error] obtener_servicios: {ex}")
            return _fallback("servicios")

    elif nombre == "obtener_producto_saas":
        try:
            if supabase is None:
                raise Exception("Cliente Supabase no inicializado")
            result = supabase.table("productos_saas").select("*").execute()
            if not result.data:
                return _fallback("productos SaaS")
            productos_dict = {row["id"]: row for row in result.data}
            producto = args.get("producto", "todos")
            if producto == "todos":
                return {"productos": productos_dict}
            if producto in productos_dict:
                return productos_dict[producto]
            return {"error": f"Producto '{producto}' no encontrado."}
        except Exception as ex:
            print(f"[KB DB error] obtener_producto_saas: {ex}")
            return _fallback("productos SaaS")

    elif nombre == "obtener_metricas":
        try:
            if supabase is None:
                raise Exception("Cliente Supabase no inicializado")
            result = supabase.table("metricas").select("*").execute()
            if not result.data:
                return _fallback("métricas")
            return {row["clave"]: row["valor"] for row in result.data}
        except Exception as ex:
            print(f"[KB DB error] obtener_metricas: {ex}")
            return _fallback("métricas")

    elif nombre == "obtener_contacto":
        try:
            if supabase is None:
                raise Exception("Cliente Supabase no inicializado")
            result = supabase.table("empresa").select("contacto").eq("id", 1).execute()
            if not result.data or not result.data[0].get("contacto"):
                return _fallback("contacto")
            contacto = result.data[0]["contacto"].copy()
            contacto["mensaje"] = (
                "Un asesor de GoToCloud puede orientarte y preparar una propuesta personalizada. "
                "¿Te gustaría que te contactaran por WhatsApp al +57 317 427 0148?"
            )
            return contacto
        except Exception as ex:
            print(f"[KB DB error] obtener_contacto: {ex}")
            return _fallback("contacto")

    elif nombre == "obtener_beneficios_para_cliente":
        try:
            if supabase is None:
                raise Exception("Cliente Supabase no inicializado")
            
            # Fetch all servicios from DB
            result = supabase.table("servicios").select("*").execute()
            if not result.data:
                return _fallback("recomendaciones")
            
            # Fetch productos_saas for recommendations that need them
            productos_result = supabase.table("productos_saas").select("*").execute()
            productos = {row["id"]: row for row in productos_result.data} if productos_result.data else {}
            
            # Build servicios dict
            s = {row["id"]: row for row in result.data}
            
            tipo = args.get("tipo_empresa", "cualquiera")
            necesidad = args.get("necesidad", "").lower()
            recomendaciones: list[dict] = []

            if any(k in necesidad for k in ["costo", "ahorro", "finops", "gasto"]):
                recomendaciones.append({
                    "servicio": "Servicios en la Nube con FinOps",
                    "razon": "GoToCloud ofrece hasta un 40% de ahorro en costos operativos mediante FinOps.",
                    "beneficios": s.get("cloud_computing", {}).get("beneficios", []),
                })
            if any(k in necesidad for k in ["document", "factura", "contrato", "papeleo", "manual"]):
                recomendaciones.append({
                    "servicio": "OASIS AI",
                    "razon": "OASIS AI reduce en 40% el tiempo de gestión documental y en 25-30% los costos operativos.",
                    "beneficios": productos.get("oasis", {}).get("beneficios", []),
                })
            if any(k in necesidad for k in ["reporte", "dashboard", "power bi", "analítica", "datos"]):
                recomendaciones.append({
                    "servicio": "Kármán Reporting Hub + Servicios de Datos",
                    "razon": "Kármán permite distribuir reportes Power BI con ahorro en licencias.",
                    "beneficios": productos.get("karman", {}).get("beneficios", []),
                })
            if any(k in necesidad for k in ["seguridad", "protección", "cumplimiento", "hack"]):
                recomendaciones.append({
                    "servicio": "Seguridad en la Nube",
                    "razon": "GoToCloud tiene especialización avanzada en protección contra amenazas Microsoft.",
                    "beneficios": s.get("seguridad", {}).get("especializaciones", []),
                })
            if any(k in necesidad for k in ["migración", "migracion", "nube", "azure", "mover"]):
                beneficios_tipo = (
                    s.get("cloud_computing", {}).get("para_quien", {}).get("pymes", [])
                    if tipo == "pyme"
                    else s.get("cloud_computing", {}).get("para_quien", {}).get("corporativos", [])
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
                    "beneficios": s.get("datos", {}).get("especializaciones", []),
                })
            if any(k in necesidad for k in ["soporte", "administr", "mantenimiento", "operar"]):
                recomendaciones.append({
                    "servicio": "Servicios Administrados de TI",
                    "razon": "GoToCloud opera la infraestructura 24/7 para que el equipo se enfoque en el negocio.",
                    "beneficios": s.get("servicios_administrados", {}).get("beneficios", []),
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
            return {"tipo_empresa": tipo, "necesidad": necesidad or "general", "recomendaciones": recomendaciones}
        except Exception as ex:
            print(f"[KB DB error] obtener_beneficios_para_cliente: {ex}")
            return _fallback("recomendaciones")

    else:
        return {"error": f"Tool '{nombre}' no reconocida."}


# ─────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """
Eres Camila, agente de atención al cliente por voz de GoToCloud, empresa líder en soluciones cloud y transformación digital en Latinoamérica, partner certificado de Microsoft Azure.

## REGLA ABSOLUTA — TEMA ÚNICO
Tus respuestas SOLO pueden ser sobre GoToCloud y sus servicios. Si alguien pregunta sobre temas que no son de GoToCloud (tecnología general, competidores, política, ciencia, etc.), redirígelos amablemente: "Eso está fuera de mi especialidad, pero lo que sí puedo contarte es cómo GoToCloud puede ayudarte con [tema relacionado]."

## INICIO OBLIGATORIO DE CADA LLAMADA
Lo primero que debes hacer SIEMPRE, antes de cualquier otra cosa, es:
1. Saludar y presentarte como Camila de GoToCloud.
2. Pedir el nombre completo del cliente.
3. Pedir el número de cédula.
4. Llamar la tool `registrar_datos_cliente` con esos datos.
5. Luego preguntar en qué puedes ayudar.

## CÓMO USAR LAS TOOLS
- Usa SIEMPRE las tools para dar información. No inventes datos.
- Cuando alguien pregunte por servicios, productos, métricas o contacto, llama la tool correspondiente.
- Después de recibir el resultado de una tool, conviértelo en una respuesta de voz: natural, breve, sin listas largas.

## PRODUCTOS CLAVE QUE DEBES CONOCER
- **Kármán**: portal web para gestionar dashboards Power BI con ahorro en licencias
- **OASIS AI**: automatización de documentos con IA — 40% menos tiempo, 25-30% menos costos
- **DataLoom**: orquestación de datos empresariales
- **Servicios Administrados**: gestión 24/7 de Azure con ITIL, WAF, FinOps

## TONO Y ESTILO DE VOZ
- Habla como en una llamada telefónica real: frases cortas, naturales, sin listas ni bullets.
- Sé profesional pero cercana. Usa "usted" o "tú" según cómo hable el cliente.
- Si no sabes algo, di: "Permítame conectarte con un asesor especializado."
- Cuando haya interés real, ofrece conectar por WhatsApp al +57 317 427 0148.

## FLUJO DE LLAMADA
1. Saludo + presentación + pedir nombre y cédula + registrar
2. Preguntar necesidad
3. Identificar tipo de empresa (pyme, corporativo, gobierno)
4. Usar tool adecuada para dar información precisa
5. Ofrecer hablar con asesor si hay interés
""".strip()


if __name__ == "__main__":
    print("=" * 60)
    print("GoToCloud Voicebot Tool — Test rápido")
    print("=" * 60)
    tests = [
        ("registrar_datos_cliente", {"nombre": "Juan Pérez", "cedula": "1234567890"}),
        ("obtener_informacion_empresa", {}),
        ("obtener_servicios", {"servicio": "servicios_administrados"}),
        ("obtener_producto_saas", {"producto": "oasis"}),
        ("obtener_producto_saas", {"producto": "karman"}),
        ("obtener_metricas", {}),
        ("obtener_beneficios_para_cliente", {"tipo_empresa": "pyme", "necesidad": "documentos y facturas"}),
        ("obtener_contacto", {}),
    ]
    for nombre, args in tests:
        print(f"\n>> {nombre}({args})")
        print(json.dumps(ejecutar_tool(nombre, args), ensure_ascii=False, indent=2)[:400])
    print(f"\nTools OK | {len(GOTOCLOUD_TOOLS)} tools | System prompt: {len(SYSTEM_PROMPT)} chars")
