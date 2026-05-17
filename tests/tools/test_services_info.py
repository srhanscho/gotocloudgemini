# =============================================================
#  T-018 — Unit tests for service/tools/services_info.py
# =============================================================

from service.tools.services_info import execute, TOOL_DECLARATION
from service.session import Session
from service.kb import GOTOCLOUD_KB


def test_tool_declaration():
    assert TOOL_DECLARATION["name"] == "obtener_servicios"
    params = TOOL_DECLARATION["parameters"]["properties"]["servicio"]
    assert params["enum"] == [
        "cloud_computing",
        "modernizacion_apps",
        "seguridad",
        "servicios_administrados",
        "datos",
        "soluciones_saas",
        "todos",
    ]


def test_execute_all_services():
    """Should return list of all services when servicio='todos'."""
    session = Session()
    result = execute({"servicio": "todos"}, session, GOTOCLOUD_KB)

    assert "servicios" in result
    assert isinstance(result["servicios"], list)
    assert len(result["servicios"]) == 6
    # Each entry should have id, nombre, descripcion
    for svc in result["servicios"]:
        assert "id" in svc
        assert "nombre" in svc
        assert "descripcion" in svc


def test_execute_default_is_all():
    """Default (no args) should return all services."""
    session = Session()
    result = execute({}, session, GOTOCLOUD_KB)
    assert "servicios" in result
    assert len(result["servicios"]) == 6


def test_execute_specific_service():
    """Should return full service definition for a specific ID."""
    session = Session()
    result = execute({"servicio": "cloud_computing"}, session, GOTOCLOUD_KB)

    assert result["nombre"] == "Servicios en la Nube"
    assert "descripcion" in result
    assert "beneficios" in result


def test_execute_specific_service_seguridad():
    """Should return security service details."""
    session = Session()
    result = execute({"servicio": "seguridad"}, session, GOTOCLOUD_KB)

    assert result["nombre"] == "Seguridad en la Nube"
    assert "especializaciones" in result
    assert "partners" in result


def test_execute_invalid_service():
    """Should return error dict for unknown service ID."""
    session = Session()
    result = execute({"servicio": "servicio_inexistente"}, session, GOTOCLOUD_KB)

    assert "error" in result
    assert "servicio_inexistente" in result["error"]


def test_execute_soluciones_saas():
    """Should return SaaS solutions service with productos."""
    session = Session()
    result = execute({"servicio": "soluciones_saas"}, session, GOTOCLOUD_KB)

    assert result["nombre"] == "Soluciones SaaS"
    assert "productos" in result
    assert "karman" in result["productos"]
    assert "oasis" in result["productos"]
    assert "dataloom" in result["productos"]
