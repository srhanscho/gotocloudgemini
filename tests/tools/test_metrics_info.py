# =============================================================
#  T-018 — Unit tests for service/tools/metrics_info.py
# =============================================================

from service.tools.metrics_info import execute, TOOL_DECLARATION
from service.session import Session
from service.kb import GOTOCLOUD_KB


def test_tool_declaration():
    assert TOOL_DECLARATION["name"] == "obtener_metricas"
    assert TOOL_DECLARATION["parameters"]["required"] == []


def test_execute_returns_metrics():
    """Should return all metrics from KB."""
    session = Session()
    result = execute({}, session, GOTOCLOUD_KB)

    assert "empresas_transformadas" in result
    assert "servidores_migrados" in result
    assert "satisfaccion_cliente" in result
    assert "ahorro_costos_cloud" in result


def test_execute_returns_copy():
    """Should return a copy so mutations don't affect KB."""
    session = Session()
    result1 = execute({}, session, GOTOCLOUD_KB)
    result2 = execute({}, session, GOTOCLOUD_KB)
    assert result1 is not result2
    result1["empresas_transformadas"] = "MODIFIED"
    assert "MODIFIED" not in result2["empresas_transformadas"]


def test_execute_ignores_args():
    """Metrics tool ignores args."""
    session = Session()
    result1 = execute({}, session, GOTOCLOUD_KB)
    result2 = execute({"ignored": "value"}, session, GOTOCLOUD_KB)
    assert result1 == result2


def test_execute_all_values_are_strings():
    """All metric values should be strings."""
    session = Session()
    result = execute({}, session, GOTOCLOUD_KB)
    for key, value in result.items():
        assert isinstance(value, str), f"Metric '{key}' is not a string: {type(value)}"
