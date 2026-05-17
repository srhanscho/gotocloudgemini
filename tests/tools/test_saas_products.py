# =============================================================
#  T-018 — Unit tests for service/tools/saas_products.py
# =============================================================

from service.tools.saas_products import execute, TOOL_DECLARATION
from service.session import Session
from service.kb import GOTOCLOUD_KB


def test_tool_declaration():
    assert TOOL_DECLARATION["name"] == "obtener_producto_saas"
    params = TOOL_DECLARATION["parameters"]["properties"]["producto"]
    assert "karman" in params["enum"]
    assert "oasis" in params["enum"]
    assert "dataloom" in params["enum"]
    assert "todos" in params["enum"]


def test_execute_all_products():
    """Should return all products when producto='todos'."""
    session = Session()
    result = execute({"producto": "todos"}, session, GOTOCLOUD_KB)

    assert "productos" in result
    assert "karman" in result["productos"]
    assert "oasis" in result["productos"]
    assert "dataloom" in result["productos"]


def test_execute_default_is_all():
    """Default (no args) should return all products."""
    session = Session()
    result = execute({}, session, GOTOCLOUD_KB)
    assert "productos" in result


def test_execute_karman():
    """Should return Kármán product details."""
    session = Session()
    result = execute({"producto": "karman"}, session, GOTOCLOUD_KB)

    assert result["nombre"] == "Kármán Reporting Hub"
    assert "descripcion" in result
    assert "funcionalidades" in result
    assert "beneficios" in result


def test_execute_oasis():
    """Should return OASIS AI product details."""
    session = Session()
    result = execute({"producto": "oasis"}, session, GOTOCLOUD_KB)

    assert result["nombre"] == "OASIS AI"
    assert "funcionalidades" in result
    assert "seguridad" in result


def test_execute_dataloom():
    """Should return DataLoom product details."""
    session = Session()
    result = execute({"producto": "dataloom"}, session, GOTOCLOUD_KB)

    assert result["nombre"] == "DataLoom"
    assert "beneficios" in result


def test_execute_invalid_product():
    """Should return error dict for unknown product ID."""
    session = Session()
    result = execute({"producto": "producto_inexistente"}, session, GOTOCLOUD_KB)

    assert "error" in result
    assert "producto_inexistente" in result["error"]
