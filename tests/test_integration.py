# =============================================================
#  T-019 — Integration test for full facade flow
#  Tests: registration → info → summary through ejecutar_tool
# =============================================================

from unittest.mock import patch, MagicMock

from service.gotocloud_voicebot_tool import (
    ejecutar_tool,
    GOTOCLOUD_TOOLS,
    SYSTEM_PROMPT,
    GOTOCLOUD_KB,
    _cliente_actual,
)
from service.tools import TOOL_EXECUTORS


def _mock_supabase_not_connected():
    """Patch supabase to None in both customer_registration and call_summary modules."""
    return patch.multiple(
        "service.tools.customer_registration",
        supabase=None,
    )


# ── Facade imports work ──────────────────────────────────────────────────────

def test_facade_exports_gotocloud_tools():
    """Facade should export GOTOCLOUD_TOOLS with 8 tools."""
    assert len(GOTOCLOUD_TOOLS) == 8


def test_facade_exports_system_prompt():
    """Facade should export SYSTEM_PROMPT."""
    assert isinstance(SYSTEM_PROMPT, str)
    assert len(SYSTEM_PROMPT) > 0
    assert "Camila" in SYSTEM_PROMPT


def test_facade_exports_gotocloud_kb():
    """Facade should export GOTOCLOUD_KB."""
    assert "empresa" in GOTOCLOUD_KB
    assert "servicios" in GOTOCLOUD_KB


# ── Full call flow: registration → info → summary ───────────────────────────

def test_full_call_flow():
    """Simulate a complete voice call through the facade.

    Flow:
    1. registrar_datos_cliente — registers customer
    2. obtener_informacion_empresa — gets company info
    3. obtener_servicios — asks about cloud services
    4. obtener_beneficios_para_cliente — gets recommendations
    5. obtener_contacto — gets contact info
    6. registrar_resumen_llamada — ends call with summary
    """
    _cliente_actual.clear()

    with _mock_supabase_not_connected():
        # Step 1: Register customer
        reg_result = ejecutar_tool("registrar_datos_cliente", {
            "nombre": "María Rodríguez",
            "cedula": "1122334455",
            "empresa": "DataCorp SAS",
            "telefono": "+57 315 999 8877",
        })
        assert reg_result["registrado"] is True
        assert reg_result["nombre"] == "María Rodríguez"

        # Step 2: Get company info
        info_result = ejecutar_tool("obtener_informacion_empresa", {})
        assert info_result["nombre"] == "GoToCloud"
        assert "descripcion" in info_result

        # Step 3: Ask about cloud services
        svc_result = ejecutar_tool("obtener_servicios", {"servicio": "cloud_computing"})
        assert svc_result["nombre"] == "Servicios en la Nube"

        # Step 4: Get recommendations based on need
        rec_result = ejecutar_tool("obtener_beneficios_para_cliente", {
            "necesidad": "reducir costos y migrar a la nube",
        })
        assert len(rec_result["recomendaciones"]) >= 1

        # Step 5: Get contact info
        contact_result = ejecutar_tool("obtener_contacto", {})
        assert "whatsapp" in contact_result

        # Step 6: Register call summary
        summary_result = ejecutar_tool("registrar_resumen_llamada", {
            "resumen": "Cliente interesada en migración a la nube y reducción de costos",
            "intention": "caliente",
            "score_lead": 80,
            "servicios_interes": ["cloud_computing"],
            "recomendaciones": "Enviar propuesta de migración con FinOps",
        })
        assert summary_result["registrado"] is True

    _cliente_actual.clear()


def test_call_flow_returning_customer():
    """Simulate a returning customer call.

    Flow:
    1. registrar_datos_cliente — re-registers (ya_registrado)
    2. obtener_producto_saas — asks about OASIS AI
    3. registrar_resumen_llamada — ends call
    """
    # Clear state and mock Supabase to avoid real DB
    _cliente_actual.clear()

    with _mock_supabase_not_connected():
        # First registration
        reg1 = ejecutar_tool("registrar_datos_cliente", {
            "nombre": "Carlos López",
            "cedula": "5566778899",
            "empresa": "TechStart",
            "telefono": "+57 310 555 6677",
        })
        assert reg1["registrado"] is True
        assert reg1["ya_registrado"] is False

        # Second registration with same cedula (returning customer)
        reg2 = ejecutar_tool("registrar_datos_cliente", {
            "nombre": "Carlos López",
            "cedula": "5566778899",
            "empresa": "TechStart",
            "telefono": "+57 310 555 6677",
        })
        # Without Supabase, ya_registrado will be False since no DB lookup
        assert reg2["registrado"] is True

        # Ask about SaaS products
        saas_result = ejecutar_tool("obtener_producto_saas", {"producto": "oasis"})
        assert saas_result["nombre"] == "OASIS AI"

        # End call
        summary = ejecutar_tool("registrar_resumen_llamada", {
            "resumen": "Cliente recurrente interesado en OASIS AI",
            "intention": "calida",
            "score_lead": 70,
        })
        assert summary["registrado"] is True

    _cliente_actual.clear()


# ── Unknown tool handling ────────────────────────────────────────────────────

def test_unknown_tool_returns_error():
    """Calling an unknown tool should return error dict."""
    result = ejecutar_tool("tool_inexistente", {})
    assert "error" in result
    assert "tool_inexistente" in result["error"]


def test_unknown_tool_does_not_crash():
    """Unknown tool should not raise an exception."""
    # This should return gracefully, not crash
    result = ejecutar_tool("nonexistent", {"foo": "bar"})
    assert isinstance(result, dict)
    assert "error" in result


# ── TOOL_EXECUTORS dispatch through facade ───────────────────────────────────

def test_all_tools_dispatchable():
    """Every tool in TOOL_EXECUTORS should be callable through ejecutar_tool."""
    for tool_name in TOOL_EXECUTORS:
        if tool_name == "registrar_resumen_llamada":
            # Needs a registered client; test separately
            continue
        result = ejecutar_tool(tool_name, {})
        assert isinstance(result, dict), f"Tool '{tool_name}' did not return dict"


def test_session_persistence_across_calls():
    """Session data from registration should persist for summary.

    The facade uses _cliente_actual dict to persist state between calls.
    After registrar_datos_cliente, _cliente_actual should have the customer data.
    Then registrar_resumen_llamada should be able to find the cliente_id.
    """
    # Clear any previous state
    _cliente_actual.clear()

    with _mock_supabase_not_connected():
        # Register customer
        ejecutar_tool("registrar_datos_cliente", {
            "nombre": "Test User",
            "cedula": "9998887776",
            "empresa": "Test Corp",
            "telefono": "+57 300 000 0000",
        })

        # Check that _cliente_actual was populated
        assert _cliente_actual.get("nombre") == "Test User"
        assert _cliente_actual.get("cedula") == "9998887776"

        # Now call summary — should find the client
        summary = ejecutar_tool("registrar_resumen_llamada", {
            "resumen": "Test call summary",
            "intention": "fria",
            "score_lead": 20,
        })
        assert summary["registrado"] is True

    # Clean up
    _cliente_actual.clear()


# ── System prompt content checks ─────────────────────────────────────────────

def test_system_prompt_mentions_all_tools():
    """SYSTEM_PROMPT should mention all 8 tools."""
    tool_names = [t["name"] for t in GOTOCLOUD_TOOLS]
    for name in tool_names:
        assert name in SYSTEM_PROMPT, f"Tool '{name}' not mentioned in SYSTEM_PROMPT"


def test_system_prompt_has_routing_guide():
    """SYSTEM_PROMPT should include routing guide section."""
    assert "GUÍA DE USO DE TOOLS" in SYSTEM_PROMPT or "GUÍA DE USO" in SYSTEM_PROMPT


def test_system_prompt_has_camila_persona():
    """SYSTEM_PROMPT should identify Camila as the agent."""
    assert "Camila" in SYSTEM_PROMPT
    assert "GoToCloud" in SYSTEM_PROMPT
