# =============================================================
#  T-018 — Unit tests for service/tools/company_info.py
# =============================================================

from service.tools.company_info import execute, TOOL_DECLARATION
from service.session import Session
from service.kb import GOTOCLOUD_KB


def test_tool_declaration():
    assert TOOL_DECLARATION["name"] == "obtener_informacion_empresa"
    assert TOOL_DECLARATION["parameters"]["required"] == []


def test_execute_returns_company_data():
    """Should return all company info fields from KB."""
    session = Session()
    result = execute({}, session, GOTOCLOUD_KB)

    assert result["nombre"] == "GoToCloud"
    assert "descripcion" in result
    assert "presencia" in result
    assert "propuesta_valor" in result
    assert "clientes_destacados" in result
    assert "partners" in result
    assert "reconocimientos" in result


def test_execute_propuesta_valor_is_list():
    """propuesta_valor should be a non-empty list."""
    session = Session()
    result = execute({}, session, GOTOCLOUD_KB)
    assert isinstance(result["propuesta_valor"], list)
    assert len(result["propuesta_valor"]) > 0


def test_execute_partners_includes_microsoft():
    """Partners list should include Microsoft."""
    session = Session()
    result = execute({}, session, GOTOCLOUD_KB)
    assert "Microsoft" in result["partners"]


def test_execute_ignores_args():
    """Company info tool ignores args (no parameters)."""
    session = Session()
    result1 = execute({}, session, GOTOCLOUD_KB)
    result2 = execute({"ignored": "value"}, session, GOTOCLOUD_KB)
    assert result1 == result2
