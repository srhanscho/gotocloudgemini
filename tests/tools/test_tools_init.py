# =============================================================
#  T-017 — Unit tests for service/tools/__init__.py
#  Tests tool registry, declarations, and TOOL_EXECUTORS dispatch
# =============================================================

import pytest

from service.tools import (
    GOTOCLOUD_TOOLS,
    TOOL_EXECUTORS,
    register_tool,
)


# ── GOTOCLOUD_TOOLS registry ─────────────────────────────────────────────────

def test_gotocloud_tools_has_8_entries():
    """Should have exactly 8 tool declarations."""
    assert len(GOTOCLOUD_TOOLS) == 8


def test_all_tool_names_present():
    """All expected tool names should be in the registry."""
    expected_names = {
        "registrar_datos_cliente",
        "obtener_informacion_empresa",
        "obtener_servicios",
        "obtener_producto_saas",
        "obtener_metricas",
        "obtener_contacto",
        "obtener_beneficios_para_cliente",
        "registrar_resumen_llamada",
    }
    actual_names = {t["name"] for t in GOTOCLOUD_TOOLS}
    assert actual_names == expected_names


def test_each_tool_has_required_fields():
    """Each tool declaration must have name, description, parameters."""
    for tool in GOTOCLOUD_TOOLS:
        assert "name" in tool, f"Tool missing 'name': {tool}"
        assert "description" in tool, f"Tool missing 'description': {tool}"
        assert "parameters" in tool, f"Tool missing 'parameters': {tool}"
        assert "type" in tool["parameters"], f"Tool params missing 'type': {tool}"


def test_tool_names_are_unique():
    """No duplicate tool names allowed."""
    names = [t["name"] for t in GOTOCLOUD_TOOLS]
    assert len(names) == len(set(names)), f"Duplicate names found: {names}"


def test_registrar_datos_cliente_has_required_params():
    """Customer registration tool must require nombre and cedula."""
    tool = next(t for t in GOTOCLOUD_TOOLS if t["name"] == "registrar_datos_cliente")
    params = tool["parameters"]
    assert "nombre" in params["required"]
    assert "cedula" in params["required"]


def test_registrar_resumen_llamada_has_required_params():
    """Call summary tool must require resumen, intention, score_lead."""
    tool = next(t for t in GOTOCLOUD_TOOLS if t["name"] == "registrar_resumen_llamada")
    params = tool["parameters"]
    assert "resumen" in params["required"]
    assert "intention" in params["required"]
    assert "score_lead" in params["required"]


def test_obtener_informacion_empresa_no_required_params():
    """Company info tool should have no required parameters."""
    tool = next(t for t in GOTOCLOUD_TOOLS if t["name"] == "obtener_informacion_empresa")
    assert tool["parameters"]["required"] == []


def test_obtener_metricas_no_required_params():
    """Metrics tool should have no required parameters."""
    tool = next(t for t in GOTOCLOUD_TOOLS if t["name"] == "obtener_metricas")
    assert tool["parameters"]["required"] == []


# ── TOOL_EXECUTORS dispatch map ──────────────────────────────────────────────

def test_tool_executors_has_8_entries():
    """Should have exactly 8 executor callables."""
    assert len(TOOL_EXECUTORS) == 8


def test_tool_executors_keys_match_tool_names():
    """Executor keys should match tool declaration names."""
    executor_names = set(TOOL_EXECUTORS.keys())
    tool_names = {t["name"] for t in GOTOCLOUD_TOOLS}
    assert executor_names == tool_names


def test_all_executors_are_callable():
    """Every executor value must be callable."""
    for name, executor in TOOL_EXECUTORS.items():
        assert callable(executor), f"Executor for '{name}' is not callable"


def test_executor_dispatch_returns_dict():
    """Each executor should return a dict when called with empty args."""
    from service.session import Session
    from service.kb import GOTOCLOUD_KB

    session = Session()
    for name, executor in TOOL_EXECUTORS.items():
        if name == "registrar_resumen_llamada":
            # This tool requires a registered client; skip for basic test
            continue
        result = executor({}, session, GOTOCLOUD_KB)
        assert isinstance(result, dict), f"Executor '{name}' did not return dict"


def test_unknown_tool_name_not_in_executors():
    """A made-up tool name should not be in executors."""
    assert "tool_inexistente" not in TOOL_EXECUTORS


# ── register_tool function ───────────────────────────────────────────────────

def test_register_tool_appends():
    """register_tool should add a declaration to the list."""
    initial_count = len(GOTOCLOUD_TOOLS)
    test_decl = {"name": "test_tool", "description": "test", "parameters": {"type": "object", "properties": {}}}
    register_tool(test_decl)
    assert len(GOTOCLOUD_TOOLS) == initial_count + 1
    assert GOTOCLOUD_TOOLS[-1] == test_decl
    # Clean up
    GOTOCLOUD_TOOLS.pop()
