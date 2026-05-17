# =============================================================
#  T-016 — Unit tests for service/session.py
#  Tests Session class: creation, state transitions, to_dict()
# =============================================================

from service.session import Session


# ── Default construction ─────────────────────────────────────────────────────

def test_session_defaults():
    """New session should have all fields empty/None."""
    s = Session()
    assert s.cliente_id is None
    assert s.cedula == ""
    assert s.nombre == ""
    assert s.empresa == ""
    assert s.telefono == ""
    assert s.started_at == ""


def test_session_with_initial_values():
    """Session should accept initial values via dataclass constructor."""
    s = Session(
        cliente_id=42,
        cedula="1234567890",
        nombre="Juan Pérez",
        empresa="GoToCloud",
        telefono="+57 300 123 4567",
    )
    assert s.cliente_id == 42
    assert s.cedula == "1234567890"
    assert s.nombre == "Juan Pérez"
    assert s.empresa == "GoToCloud"
    assert s.telefono == "+57 300 123 4567"


# ── mark_started ─────────────────────────────────────────────────────────────

def test_mark_started_sets_timestamp():
    """mark_started should set started_at to a non-empty ISO string."""
    s = Session()
    assert s.started_at == ""
    s.mark_started()
    assert s.started_at != ""
    assert "T" in s.started_at  # ISO 8601 format


def test_mark_started_utc():
    """Timestamp should include UTC offset."""
    s = Session()
    s.mark_started()
    # Should contain timezone info (+00:00 or Z)
    assert "+" in s.started_at or "Z" in s.started_at


def test_mark_started_idempotent():
    """Calling mark_started twice should still produce a valid timestamp."""
    s = Session()
    s.mark_started()
    first = s.started_at
    s.mark_started()
    second = s.started_at
    assert second != ""
    # Second call should be >= first (time moved forward)
    assert second >= first


# ── to_dict ──────────────────────────────────────────────────────────────────

def test_to_dict_empty_session():
    """to_dict on empty session should return dict with None/empty values."""
    s = Session()
    d = s.to_dict()
    assert d["cliente_id"] is None
    assert d["nombre"] == ""
    assert d["cedula"] == ""
    assert d["empresa"] == ""
    assert d["telefono"] == ""
    assert d["started_at"] == ""


def test_to_dict_populated_session():
    """to_dict should reflect all populated fields."""
    s = Session(
        cliente_id=1,
        cedula="1234567890",
        nombre="Ana García",
        empresa="Empresa XYZ",
        telefono="+57 310 987 6543",
    )
    s.mark_started()
    d = s.to_dict()
    assert d["cliente_id"] == 1
    assert d["nombre"] == "Ana García"
    assert d["cedula"] == "1234567890"
    assert d["empresa"] == "Empresa XYZ"
    assert d["telefono"] == "+57 310 987 6543"
    assert d["started_at"] != ""


def test_to_dict_returns_new_dict():
    """to_dict should return a new dict each call."""
    s = Session(cliente_id=1, nombre="Test")
    d1 = s.to_dict()
    d2 = s.to_dict()
    assert d1 is not d2
    d1["nombre"] = "MODIFIED"
    assert d2["nombre"] == "Test"


def test_to_dict_has_expected_keys():
    """to_dict should have exactly the backward-compat keys."""
    s = Session()
    d = s.to_dict()
    expected_keys = {"cliente_id", "nombre", "cedula", "empresa", "telefono", "started_at"}
    assert set(d.keys()) == expected_keys


# ── State transitions ────────────────────────────────────────────────────────

def test_session_populate_then_to_dict():
    """Simulate real flow: empty session → populate → to_dict."""
    s = Session()
    # Simulate registrar_datos_cliente populating session
    s.nombre = "Carlos López"
    s.cedula = "9876543210"
    s.empresa = "TechCorp"
    s.telefono = "+57 320 111 2233"
    s.mark_started()
    s.cliente_id = 99

    d = s.to_dict()
    assert d["nombre"] == "Carlos López"
    assert d["cedula"] == "9876543210"
    assert d["cliente_id"] == 99
    assert d["started_at"] != ""


def test_multiple_sessions_independent():
    """Two sessions should be completely independent."""
    s1 = Session(cliente_id=1, nombre="User1")
    s2 = Session(cliente_id=2, nombre="User2")
    assert s1.cliente_id != s2.cliente_id
    assert s1.nombre != s2.nombre
    s1.nombre = "Modified1"
    assert s2.nombre == "User2"  # Unaffected
