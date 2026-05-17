# =============================================================
#  T-015 — Unit tests for service/kb.py
#  Tests all 5 typed accessors + GOTOCLOUD_KB structure
# =============================================================

import pytest

from service.kb import (
    GOTOCLOUD_KB,
    get_service,
    get_product,
    get_contact,
    get_metrics,
    get_company_info,
)


# ── GOTOCLOUD_KB structure integrity ─────────────────────────────────────────

def test_kb_has_top_level_keys():
    """KB must have empresa, servicios, metricas sections."""
    assert "empresa" in GOTOCLOUD_KB
    assert "servicios" in GOTOCLOUD_KB
    assert "metricas" in GOTOCLOUD_KB


def test_kb_empresa_has_contact():
    """empresa section must include contact info."""
    assert "contacto" in GOTOCLOUD_KB["empresa"]
    assert "whatsapp" in GOTOCLOUD_KB["empresa"]["contacto"]
    assert "web" in GOTOCLOUD_KB["empresa"]["contacto"]
    assert "linkedin" in GOTOCLOUD_KB["empresa"]["contacto"]


def test_kb_servicios_has_soluciones_saas():
    """servicios must include soluciones_saas with productos."""
    saas = GOTOCLOUD_KB["servicios"]["soluciones_saas"]
    assert "productos" in saas
    assert "karman" in saas["productos"]
    assert "oasis" in saas["productos"]
    assert "dataloom" in saas["productos"]


def test_kb_metricas_not_empty():
    """metricas section must have entries."""
    assert len(GOTOCLOUD_KB["metricas"]) > 0


# ── get_service accessor ─────────────────────────────────────────────────────

def test_get_service_existing():
    """Should return the full service definition for a known ID."""
    result = get_service("cloud_computing")
    assert result["nombre"] == "Servicios en la Nube"
    assert "descripcion" in result
    assert "beneficios" in result


def test_get_service_nonexistent():
    """Should return empty dict for unknown service ID."""
    result = get_service("servicio_inexistente")
    assert result == {}


def test_get_service_all_ids():
    """All 6 service IDs should return non-empty results."""
    service_ids = [
        "cloud_computing",
        "modernizacion_apps",
        "seguridad",
        "servicios_administrados",
        "datos",
        "soluciones_saas",
    ]
    for sid in service_ids:
        result = get_service(sid)
        assert result != {}, f"get_service('{sid}') returned empty"
        assert "nombre" in result


# ── get_product accessor ─────────────────────────────────────────────────────

def test_get_product_existing():
    """Should return the full product definition for a known ID."""
    result = get_product("oasis")
    assert result["nombre"] == "OASIS AI"
    assert "descripcion" in result
    assert "funcionalidades" in result


def test_get_product_nonexistent():
    """Should return empty dict for unknown product ID."""
    result = get_product("producto_inexistente")
    assert result == {}


def test_get_product_all_ids():
    """All 3 product IDs should return non-empty results."""
    product_ids = ["karman", "oasis", "dataloom"]
    for pid in product_ids:
        result = get_product(pid)
        assert result != {}, f"get_product('{pid}') returned empty"
        assert "nombre" in result


# ── get_contact accessor ─────────────────────────────────────────────────────

def test_get_contact_returns_dict():
    """Should return a dict with whatsapp, web, linkedin."""
    result = get_contact()
    assert isinstance(result, dict)
    assert result["whatsapp"] == "+57 317 427 0148"
    assert result["web"] == "https://www.gotocloud.ai"
    assert "linkedin" in result


def test_get_contact_returns_copy():
    """Should return a copy, not the original dict."""
    result1 = get_contact()
    result2 = get_contact()
    assert result1 is not result2
    # Mutating one should not affect the other
    result1["whatsapp"] = "MODIFIED"
    assert result2["whatsapp"] == "+57 317 427 0148"


# ── get_metrics accessor ─────────────────────────────────────────────────────

def test_get_metrics_returns_dict():
    """Should return a dict with metric entries."""
    result = get_metrics()
    assert isinstance(result, dict)
    assert "empresas_transformadas" in result
    assert "servidores_migrados" in result
    assert "satisfaccion_cliente" in result


def test_get_metrics_returns_copy():
    """Should return a copy, not the original dict."""
    result1 = get_metrics()
    result2 = get_metrics()
    assert result1 is not result2
    result1["empresas_transformadas"] = "MODIFIED"
    assert "Más de 100" in result2["empresas_transformadas"]


# ── get_company_info accessor ────────────────────────────────────────────────

def test_get_company_info():
    """Should return company info with all expected keys."""
    result = get_company_info()
    assert result["nombre"] == "GoToCloud"
    assert "descripcion" in result
    assert "presencia" in result
    assert "propuesta_valor" in result
    assert "clientes_destacados" in result
    assert "partners" in result
    assert "reconocimientos" in result


def test_get_company_info_returns_copy():
    """Should return a copy, not the original dict."""
    result1 = get_company_info()
    result2 = get_company_info()
    assert result1 is not result2
    result1["nombre"] = "MODIFIED"
    assert result2["nombre"] == "GoToCloud"
