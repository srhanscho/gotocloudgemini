# =============================================================
#  T-018 — Unit tests for service/tools/recommendations.py
#  Tests keyword matching for each necesidad category
# =============================================================

from service.tools.recommendations import execute, TOOL_DECLARATION
from service.session import Session
from service.kb import GOTOCLOUD_KB


def test_tool_declaration():
    assert TOOL_DECLARATION["name"] == "obtener_beneficios_para_cliente"
    params = TOOL_DECLARATION["parameters"]["properties"]
    assert "tipo_empresa" in params
    assert "necesidad" in params


def test_execute_cost_keyword():
    """Should recommend cloud services with FinOps for cost-related needs."""
    session = Session()
    result = execute({"necesidad": "quiero reducir costos operativos"}, session, GOTOCLOUD_KB)

    services = [r["servicio"] for r in result["recomendaciones"]]
    assert any("FinOps" in s for s in services)


def test_execute_document_keyword():
    """Should recommend OASIS AI for document-related needs."""
    session = Session()
    result = execute({"necesidad": "tenemos muchas facturas y contratos"}, session, GOTOCLOUD_KB)

    services = [r["servicio"] for r in result["recomendaciones"]]
    assert any("OASIS" in s for s in services)


def test_execute_dashboard_keyword():
    """Should recommend Kármán for dashboard/reporting needs."""
    session = Session()
    result = execute({"necesidad": "necesitamos dashboards y reportes"}, session, GOTOCLOUD_KB)

    services = [r["servicio"] for r in result["recomendaciones"]]
    assert any("Kármán" in s for s in services)


def test_execute_security_keyword():
    """Should recommend security services for security needs."""
    session = Session()
    result = execute({"necesidad": "nos preocupa la seguridad y protección de datos"}, session, GOTOCLOUD_KB)

    services = [r["servicio"] for r in result["recomendaciones"]]
    assert any("Seguridad" in s for s in services)


def test_execute_migration_keyword():
    """Should recommend cloud migration services."""
    session = Session()
    result = execute({"necesidad": "queremos migrar a la nube azure"}, session, GOTOCLOUD_KB)

    services = [r["servicio"] for r in result["recomendaciones"]]
    assert any("Nube" in s for s in services)


def test_execute_ai_keyword():
    """Should recommend OASIS AI + modernization for AI needs."""
    session = Session()
    result = execute({"necesidad": "necesitamos inteligencia artificial y automatización"}, session, GOTOCLOUD_KB)

    services = [r["servicio"] for r in result["recomendaciones"]]
    assert any("OASIS" in s or "Modernización" in s for s in services)


def test_execute_support_keyword():
    """Should recommend managed services for support needs."""
    session = Session()
    result = execute({"necesidad": "necesitamos soporte y mantenimiento"}, session, GOTOCLOUD_KB)

    services = [r["servicio"] for r in result["recomendaciones"]]
    assert any("Administrados" in s for s in services)


def test_execute_fallback_general():
    """Should return consulting recommendation for unrecognized needs."""
    session = Session()
    result = execute({"necesidad": "algo que no coincide"}, session, GOTOCLOUD_KB)

    assert len(result["recomendaciones"]) == 1
    assert result["recomendaciones"][0]["servicio"] == "Consultoría GoToCloud"


def test_execute_empty_necesidad():
    """Empty necesidad should trigger fallback."""
    session = Session()
    result = execute({"necesidad": ""}, session, GOTOCLOUD_KB)

    assert result["necesidad"] == "general"
    assert result["recomendaciones"][0]["servicio"] == "Consultoría GoToCloud"


def test_execute_default_necesidad():
    """No necesidad arg should trigger fallback."""
    session = Session()
    result = execute({}, session, GOTOCLOUD_KB)

    assert result["necesidad"] == "general"


def test_execute_tipo_empresa_pyme():
    """Pyme type should affect migration recommendation benefits."""
    session = Session()
    result = execute({
        "tipo_empresa": "pyme",
        "necesidad": "migración a la nube",
    }, session, GOTOCLOUD_KB)

    assert result["tipo_empresa"] == "pyme"
    # Find the cloud migration recommendation
    cloud_rec = next(
        (r for r in result["recomendaciones"] if "Nube" in r["servicio"]),
        None,
    )
    assert cloud_rec is not None
    assert isinstance(cloud_rec["beneficios"], list)


def test_execute_tipo_empresa_corporativo():
    """Corporativo type should affect migration recommendation benefits."""
    session = Session()
    result = execute({
        "tipo_empresa": "corporativo",
        "necesidad": "migración a la nube",
    }, session, GOTOCLOUD_KB)

    assert result["tipo_empresa"] == "corporativo"


def test_execute_multiple_matches():
    """Multiple keyword matches should return multiple recommendations."""
    session = Session()
    result = execute({
        "necesidad": "reducir costos y automatizar documentos con IA",
    }, session, GOTOCLOUD_KB)

    # Should match: cost (FinOps), document (OASIS), AI (OASIS)
    assert len(result["recomendaciones"]) >= 2


def test_execute_case_insensitive():
    """Keyword matching should be case insensitive."""
    session = Session()
    result1 = execute({"necesidad": "COSTOS"}, session, GOTOCLOUD_KB)
    result2 = execute({"necesidad": "costos"}, session, GOTOCLOUD_KB)
    assert result1 == result2


def test_execute_recommendation_structure():
    """Each recommendation should have servicio, razon, beneficios."""
    session = Session()
    result = execute({"necesidad": "costos"}, session, GOTOCLOUD_KB)

    for rec in result["recomendaciones"]:
        assert "servicio" in rec
        assert "razon" in rec
        assert "beneficios" in rec
        assert isinstance(rec["beneficios"], list)
