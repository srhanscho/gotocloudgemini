# =============================================================
#  T-018 — Unit tests for service/tools/contact_info.py
# =============================================================

from service.tools.contact_info import execute, TOOL_DECLARATION
from service.session import Session
from service.kb import GOTOCLOUD_KB


def test_tool_declaration():
    assert TOOL_DECLARATION["name"] == "obtener_contacto"
    assert TOOL_DECLARATION["parameters"]["required"] == []


def test_execute_returns_contact_info():
    """Should return whatsapp, web, linkedin."""
    session = Session()
    result = execute({}, session, GOTOCLOUD_KB)

    assert result["whatsapp"] == "+57 317 427 0148"
    assert result["web"] == "https://www.gotocloud.ai"
    assert "linkedin" in result


def test_execute_includes_mensaje():
    """Should include a helper mensaje field."""
    session = Session()
    result = execute({}, session, GOTOCLOUD_KB)

    assert "mensaje" in result
    assert "WhatsApp" in result["mensaje"]
    assert "+57 317 427 0148" in result["mensaje"]


def test_execute_returns_copy():
    """Should return a copy so mutations don't affect KB."""
    session = Session()
    result1 = execute({}, session, GOTOCLOUD_KB)
    result2 = execute({}, session, GOTOCLOUD_KB)
    assert result1 is not result2
    result1["whatsapp"] = "MODIFIED"
    assert result2["whatsapp"] == "+57 317 427 0148"
