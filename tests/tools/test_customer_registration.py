# =============================================================
#  T-018 — Unit tests for service/tools/customer_registration.py
#  Tests execute() with mock KB and mock Session
#  Supabase is mocked to avoid real DB calls
# =============================================================

from unittest.mock import patch, MagicMock

from service.tools.customer_registration import execute, TOOL_DECLARATION
from service.session import Session
from service.kb import GOTOCLOUD_KB


def test_tool_declaration():
    """TOOL_DECLARATION should have correct structure."""
    assert TOOL_DECLARATION["name"] == "registrar_datos_cliente"
    assert "nombre" in TOOL_DECLARATION["parameters"]["required"]
    assert "cedula" in TOOL_DECLARATION["parameters"]["required"]


def _mock_supabase_not_connected():
    """Patch supabase to None so execute() takes the no-DB path."""
    return patch("service.tools.customer_registration.supabase", None)


def test_execute_new_customer():
    """Should register a new customer and populate session."""
    session = Session()
    args = {
        "nombre": "Juan Pérez",
        "cedula": "1234567890",
        "empresa": "TechCorp",
        "telefono": "+57 300 123 4567",
    }
    with _mock_supabase_not_connected():
        result = execute(args, session, GOTOCLOUD_KB)

    assert result["registrado"] is True
    assert result["ya_registrado"] is False
    assert result["nombre"] == "Juan Pérez"
    assert result["cedula"] == "1234567890"
    assert result["empresa"] == "TechCorp"
    assert result["telefono"] == "+57 300 123 4567"
    assert "mensaje" in result
    # Session should be populated
    assert session.nombre == "Juan Pérez"
    assert session.cedula == "1234567890"
    assert session.empresa == "TechCorp"
    assert session.telefono == "+57 300 123 4567"
    assert session.started_at != ""


def test_execute_minimal_args():
    """Should work with only required fields (nombre, cedula)."""
    session = Session()
    args = {"nombre": "Ana García", "cedula": "0987654321"}
    with _mock_supabase_not_connected():
        result = execute(args, session, GOTOCLOUD_KB)

    assert result["registrado"] is True
    assert result["ya_registrado"] is False
    assert result["empresa"] == ""
    assert result["telefono"] == ""


def test_execute_strips_whitespace():
    """Should strip whitespace from input values."""
    session = Session()
    args = {
        "nombre": "  Carlos López  ",
        "cedula": "  1111111111  ",
        "empresa": "  Empresa XYZ  ",
        "telefono": "  +57 310 000 0000  ",
    }
    with _mock_supabase_not_connected():
        result = execute(args, session, GOTOCLOUD_KB)

    assert result["nombre"] == "Carlos López"
    assert result["cedula"] == "1111111111"
    assert result["empresa"] == "Empresa XYZ"
    assert result["telefono"] == "+57 310 000 0000"


def test_execute_empty_strings_treated_as_missing():
    """Empty strings after strip should be treated as missing."""
    session = Session()
    args = {"nombre": "Test", "cedula": "999", "empresa": "  ", "telefono": "  "}
    with _mock_supabase_not_connected():
        result = execute(args, session, GOTOCLOUD_KB)

    assert result["empresa"] == ""
    assert result["telefono"] == ""


def test_execute_missing_keys_defaults():
    """Missing keys in args should default to empty strings."""
    session = Session()
    args = {"nombre": "Test", "cedula": "555"}
    with _mock_supabase_not_connected():
        result = execute(args, session, GOTOCLOUD_KB)

    assert result["registrado"] is True
    assert result["empresa"] == ""
    assert result["telefono"] == ""


def test_execute_supabase_new_customer():
    """When Supabase returns no existing client, should INSERT."""
    session = Session()
    args = {"nombre": "New User", "cedula": "9998887776"}

    # Simulate: no existing client found, then insert succeeds
    lookup_result = MagicMock()
    lookup_result.data = []  # No existing client

    insert_result = MagicMock()
    insert_result.data = [{"id": 42}]

    mock_table = MagicMock()
    mock_table.select.return_value.eq.return_value.execute.return_value = lookup_result
    mock_table.insert.return_value.execute.return_value = insert_result

    mock_supabase = MagicMock()
    mock_supabase.table.return_value = mock_table

    with patch("service.tools.customer_registration.supabase", mock_supabase):
        result = execute(args, session, GOTOCLOUD_KB)

    assert result["registrado"] is True
    assert result["ya_registrado"] is False
    assert result["cliente_id"] == 42
    assert session.cliente_id == 42


def test_execute_supabase_existing_customer():
    """When Supabase finds existing client, should UPDATE."""
    session = Session()
    args = {"nombre": "Existing User", "cedula": "1234567890"}

    # Simulate: existing client found, then update succeeds
    lookup_result = MagicMock()
    lookup_result.data = [{"id": 7}]

    mock_table = MagicMock()
    mock_table.select.return_value.eq.return_value.execute.return_value = lookup_result
    mock_table.update.return_value.eq.return_value.execute.return_value = MagicMock()

    mock_supabase = MagicMock()
    mock_supabase.table.return_value = mock_table

    with patch("service.tools.customer_registration.supabase", mock_supabase):
        result = execute(args, session, GOTOCLOUD_KB)

    assert result["registrado"] is True
    assert result["ya_registrado"] is True
    assert result["cliente_id"] == 7
    assert session.cliente_id == 7
    assert "actualizado" in result["mensaje"].lower()


def test_execute_supabase_error_graceful():
    """When Supabase raises, should still return registered=True."""
    session = Session()
    args = {"nombre": "Error User", "cedula": "1112223333"}

    mock_table = MagicMock()
    mock_table.select.return_value.eq.return_value.execute.side_effect = Exception("DB down")

    mock_supabase = MagicMock()
    mock_supabase.table.return_value = mock_table

    with patch("service.tools.customer_registration.supabase", mock_supabase):
        result = execute(args, session, GOTOCLOUD_KB)

    # Should still return registered=True (graceful degrade)
    assert result["registrado"] is True
    assert result["ya_registrado"] is False
