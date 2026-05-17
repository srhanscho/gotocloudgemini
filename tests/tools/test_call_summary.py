# =============================================================
#  T-018 — Unit tests for service/tools/call_summary.py
#  Tests execute() with mock KB and mock Session
#  Supabase is mocked to avoid real DB calls
# =============================================================

import pytest
from unittest.mock import patch, MagicMock

from service.tools.call_summary import execute, TOOL_DECLARATION
from service.session import Session
from service.kb import GOTOCLOUD_KB


def test_tool_declaration():
    """TOOL_DECLARATION should have correct structure."""
    assert TOOL_DECLARATION["name"] == "registrar_resumen_llamada"
    params = TOOL_DECLARATION["parameters"]
    assert "resumen" in params["required"]
    assert "intention" in params["required"]
    assert "score_lead" in params["required"]


def _mock_supabase_not_connected():
    """Patch supabase to None so execute() takes the no-DB path."""
    return patch("service.tools.call_summary.supabase", None)


def test_execute_valid_call_summary():
    """Should register a call summary with valid data."""
    session = Session(
        cliente_id=42,
        cedula="1234567890",
        nombre="Juan Pérez",
        started_at="2026-05-17T10:00:00+00:00",
    )
    args = {
        "resumen": "Cliente interesado en servicios de nube",
        "intention": "calida",
        "score_lead": 65,
        "servicios_interes": ["cloud_computing", "seguridad"],
        "recomendaciones": "Seguir con propuesta de migración",
    }
    with _mock_supabase_not_connected():
        result = execute(args, session, GOTOCLOUD_KB)

    assert result["registrado"] is True


def test_execute_no_cliente_id_error():
    """Should return error when no cliente_id in session."""
    session = Session()  # Empty session
    args = {
        "resumen": "Test resumen",
        "intention": "fria",
        "score_lead": 30,
    }
    with _mock_supabase_not_connected():
        result = execute(args, session, GOTOCLOUD_KB)

    assert "error" in result
    assert "cliente registrado" in result["error"]


def test_execute_invalid_score_lead_low():
    """Should return error for score_lead < 0."""
    session = Session(cliente_id=1)
    args = {
        "resumen": "Test",
        "intention": "calida",
        "score_lead": -5,
    }
    result = execute(args, session, GOTOCLOUD_KB)

    assert "error" in result
    assert "0 y 100" in result["error"]


def test_execute_invalid_score_lead_high():
    """Should return error for score_lead > 100."""
    session = Session(cliente_id=1)
    args = {
        "resumen": "Test",
        "intention": "calida",
        "score_lead": 150,
    }
    result = execute(args, session, GOTOCLOUD_KB)

    assert "error" in result
    assert "0 y 100" in result["error"]


def test_execute_invalid_intention():
    """Should return error for invalid intention value."""
    session = Session(cliente_id=1)
    args = {
        "resumen": "Test",
        "intention": "tibia",  # Not a valid value
        "score_lead": 50,
    }
    result = execute(args, session, GOTOCLOUD_KB)

    assert "error" in result
    assert "fria" in result["error"]


def test_execute_all_valid_intentions():
    """All three intention values should be accepted."""
    for intention in ("fria", "calida", "caliente"):
        session = Session(cliente_id=1, started_at="2026-05-17T10:00:00+00:00")
        args = {
            "resumen": "Test",
            "intention": intention,
            "score_lead": 50,
        }
        with _mock_supabase_not_connected():
            result = execute(args, session, GOTOCLOUD_KB)
        assert result.get("registrado") is True, f"Failed for intention='{intention}'"


def test_execute_boundary_scores():
    """Score boundaries (0 and 100) should be accepted."""
    for score in (0, 100):
        session = Session(cliente_id=1, started_at="2026-05-17T10:00:00+00:00")
        args = {
            "resumen": "Test",
            "intention": "calida",
            "score_lead": score,
        }
        with _mock_supabase_not_connected():
            result = execute(args, session, GOTOCLOUD_KB)
        assert result.get("registrado") is True, f"Failed for score_lead={score}"


def test_execute_optional_fields_defaults():
    """Missing optional fields should use defaults."""
    session = Session(cliente_id=1, started_at="2026-05-17T10:00:00+00:00")
    args = {
        "resumen": "Test",
        "intention": "calida",
        "score_lead": 50,
        # servicios_interes and recomendaciones omitted
    }
    with _mock_supabase_not_connected():
        result = execute(args, session, GOTOCLOUD_KB)

    assert result.get("registrado") is True


def test_execute_strips_resumen():
    """Should strip whitespace from resumen."""
    session = Session(cliente_id=1, started_at="2026-05-17T10:00:00+00:00")
    args = {
        "resumen": "  Test resumen  ",
        "intention": "calida",
        "score_lead": 50,
    }
    with _mock_supabase_not_connected():
        result = execute(args, session, GOTOCLOUD_KB)

    assert result.get("registrado") is True


def test_execute_empty_resumen():
    """Empty resumen after strip should still work (no validation on resumen content)."""
    session = Session(cliente_id=1, started_at="2026-05-17T10:00:00+00:00")
    args = {
        "resumen": "  ",
        "intention": "calida",
        "score_lead": 50,
    }
    with _mock_supabase_not_connected():
        result = execute(args, session, GOTOCLOUD_KB)

    # No validation on resumen content, just registration
    assert result.get("registrado") is True


def test_execute_supabase_success():
    """When Supabase returns data, should include llamada_id."""
    session = Session(cliente_id=1, started_at="2026-05-17T10:00:00+00:00")
    args = {
        "resumen": "Test",
        "intention": "calida",
        "score_lead": 50,
    }

    mock_result = MagicMock()
    mock_result.data = [{"id": 999}]

    mock_table = MagicMock()
    mock_table.insert.return_value.execute.return_value = mock_result

    mock_supabase = MagicMock()
    mock_supabase.table.return_value = mock_table

    with patch("service.tools.call_summary.supabase", mock_supabase):
        result = execute(args, session, GOTOCLOUD_KB)

    assert result["registrado"] is True
    assert result["llamada_id"] == 999


def test_execute_supabase_lookup_by_cedula():
    """When no cliente_id but cedula exists, should look up in Supabase."""
    session = Session(cedula="1234567890", started_at="2026-05-17T10:00:00+00:00")
    args = {
        "resumen": "Test",
        "intention": "calida",
        "score_lead": 50,
    }

    # First call: lookup by cedula returns cliente_id
    lookup_result = MagicMock()
    lookup_result.data = [{"id": 42}]

    # Second call: insert returns success
    insert_result = MagicMock()
    insert_result.data = [{"id": 100}]

    mock_table = MagicMock()
    mock_table.insert.return_value.execute.return_value = insert_result
    mock_table.select.return_value.eq.return_value.execute.return_value = lookup_result

    mock_supabase = MagicMock()
    mock_supabase.table.return_value = mock_table

    with patch("service.tools.call_summary.supabase", mock_supabase):
        result = execute(args, session, GOTOCLOUD_KB)

    assert result["registrado"] is True
    assert result["llamada_id"] == 100
