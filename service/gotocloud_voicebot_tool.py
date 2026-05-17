# =============================================================
#  GOTOCLOUD VOICEBOT TOOL — Backward-compatible facade
#  Re-exports from kb.py, tools/*, and session.py
#  Dispatch via TOOL_EXECUTORS dict (replaces if/elif chain)
# =============================================================

from __future__ import annotations

import logging
from typing import Any

# ─────────────────────────────────────────────
# Re-export KB (extracted to standalone module)
# ─────────────────────────────────────────────
from .kb import GOTOCLOUD_KB  # noqa: F401

# ─────────────────────────────────────────────
# Re-export tool declarations (aggregated from tools/*)
# ─────────────────────────────────────────────
from .tools import GOTOCLOUD_TOOLS  # noqa: F401

# ─────────────────────────────────────────────
# Session and dispatch infrastructure
# ─────────────────────────────────────────────
from .session import Session
from .tools import TOOL_EXECUTORS

_logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# Backward-compat: module-level client state
# The original code used _cliente_actual as a shared dict across
# tool calls within the same WebSocket connection. We preserve this
# for backward compatibility while the new tool modules use Session.
# ─────────────────────────────────────────────
_cliente_actual: dict[str, Any] = {}


def _sync_session_from_dict(session: Session, data: dict[str, Any]) -> None:
    """Populate Session fields from the backward-compat dict."""
    if data.get("nombre"):
        session.nombre = data["nombre"]
    if data.get("cedula"):
        session.cedula = data["cedula"]
    if data.get("empresa"):
        session.empresa = data["empresa"]
    if data.get("telefono"):
        session.telefono = data["telefono"]
    if data.get("cliente_id"):
        session.cliente_id = data["cliente_id"]
    if data.get("started_at"):
        session.started_at = data["started_at"]


def _sync_dict_from_session(session: Session, data: dict[str, Any]) -> None:
    """Update the backward-compat dict from Session fields."""
    if session.nombre:
        data["nombre"] = session.nombre
    if session.cedula:
        data["cedula"] = session.cedula
    if session.empresa:
        data["empresa"] = session.empresa
    if session.telefono:
        data["telefono"] = session.telefono
    if session.cliente_id is not None:
        data["cliente_id"] = session.cliente_id
    if session.started_at:
        data["started_at"] = session.started_at


def ejecutar_tool(nombre: str, args: dict[str, Any] | None = None) -> dict[str, Any]:
    """Backward-compatible tool dispatcher.

    Replaces the original if/elif chain with dict-based dispatch
    using TOOL_EXECUTORS from service/tools/__init__.py.

    Signature preserved: ejecutar_tool(nombre, args) -> dict
    """
    args = args or {}

    executor = TOOL_EXECUTORS.get(nombre)
    if executor is None:
        _logger.error(f"Tool '{nombre}' no reconocida.")
        return {"error": f"Tool '{nombre}' no reconocida."}

    # Create a per-call Session, seeded from backward-compat dict
    session = Session()
    _sync_session_from_dict(session, _cliente_actual)

    try:
        result = executor(args, session, GOTOCLOUD_KB)
    except Exception as ex:
        _logger.exception(f"Error ejecutando tool '{nombre}': {ex}")
        return {"error": "Error interno. Intenta más tarde."}

    # Sync session state back to backward-compat dict
    _sync_dict_from_session(session, _cliente_actual)

    return result


# ─────────────────────────────────────────────
# SYSTEM PROMPT — Camila persona + routing
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """
Eres Camila, agente de atención al cliente por voz de GoToCloud, empresa líder en soluciones cloud y transformación digital en Latinoamérica, partner certificado de Microsoft Azure.

## REGLA ABSOLUTA — TEMA ÚNICO
Tus respuestas SOLO pueden ser sobre GoToCloud y sus servicios. Si alguien pregunta sobre temas que no son de GoToCloud (tecnología general, competidores, política, ciencia, etc.), redirígelos amablemente: "Eso está fuera de mi especialidad, pero lo que sí puedo contarte es cómo GoToCloud puede ayudarte con [tema relacionado]."

## INICIO OBLIGATORIO DE CADA LLAMADA
Lo primero que debes hacer SIEMPRE, antes de cualquier otra cosa, es:
1. Saludar y presentarte como Camila de GoToCloud.
2. Informar que "esta llamada queda registrada bajo nuestra política de tratamiento de datos personales".
3. Pedir el nombre completo del cliente.
4. Pedir el número de cédula.
5. Pedir el nombre de la empresa u organización donde trabaja.
6. Pedir un número de teléfono de contacto.
7. Llamar la tool `registrar_datos_cliente` con todos esos datos.
8. Revisar la respuesta: si `ya_registrado` es `true`, saluda al cliente como ya conocido ("Qué bueno tenerte de vuelta, [nombre]") y confirma si sus datos siguen igual.
9. Luego preguntar en qué puedes ayudar.

## GUÍA DE USO DE TOOLS — Cuándo llamar cada una
- **Inicio de llamada** → `registrar_datos_cliente` (OBLIGATORIO, siempre primero)
- **Preguntas sobre GoToCloud** (quiénes son, dónde operan, partners, premios) → `obtener_informacion_empresa`
- **Preguntas sobre servicios** (qué ofrecen, cloud, seguridad, datos, etc.) → `obtener_servicios`
- **Preguntas sobre productos** (Kármán, OASIS AI, DataLoom, soluciones propias) → `obtener_producto_saas`
- **Preguntas sobre cifras o resultados** (cuántas empresas, ahorros, métricas) → `obtener_metricas`
- **Cliente quiere hablar con asesor o pedir cotización** → `obtener_contacto`
- **Cliente describe un problema o necesidad** → `obtener_beneficios_para_cliente`
- **Final de llamada** → `registrar_resumen_llamada` (SOLO cuando el cliente se va)

Si no estás seguro de qué tool usar, preguntá clarificando al cliente antes de llamar una tool.

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
1. Saludo + presentación + aviso política de datos + pedir nombre, cédula, empresa y teléfono + registrar
2. Preguntar necesidad
3. Identificar tipo de empresa (pyme, corporativo, gobierno)
4. Usar tool adecuada para dar información precisa
5. Ofrecer hablar con asesor si hay interés

## CIERRE DE LLAMADA
Al final de la conversación, cuando el cliente indique que se va, agradezca o no tenga más preguntas:
1. Pregunta si hay algo más en lo que puedas ayudar
2. Si el cliente confirma que no, llama la tool `registrar_resumen_llamada` con:
   - Resumen: qué preguntó, qué le interesó, en qué estado quedó
   - Intención: 'fria' (solo consultas), 'calida' (interés real sin urgencia), 'caliente' (necesidad inmediata)
   - Score: 0-100 según probabilidad de compra
   - Servicios de interés: solo los que mencionó explícitamente
   - Recomendaciones: qué debería hacer el vendedor en el seguimiento
3. Después de recibir la confirmación de la tool, despidete cordialmente
""".strip()


if __name__ == "__main__":
    import json

    print("=" * 60)
    print("GoToCloud Voicebot Tool — Test rápido (facade)")
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
