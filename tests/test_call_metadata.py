"""Tests para el sistema de metadata de llamadas (call-metadata).

Cubre:
- Tool `registrar_datos_cliente` con persistencia de empresa/teléfono
- Tool `registrar_resumen_llamada` con validación de parámetros
- Fallback timeout (lógica de defaults)
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# ── Mock Supabase ANTES de importar el módulo ──────────────────────
mock_supabase = MagicMock()
# Mock cadena: supabase.table("x").insert(y).execute() → data[0]["id"]
mock_result = MagicMock()
mock_result.data = [{"id": 42}]
mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_result

_module_path = str(Path(__file__).parent.parent)
if _module_path not in sys.path:
    sys.path.insert(0, _module_path)

with patch.dict("sys.modules", {
    "backend.supabase_client": MagicMock(
        supabase=mock_supabase,
        is_connected=lambda: True,
    )
}):
    from service.gotocloud_voicebot_tool import (
        _cliente_actual,
        ejecutar_tool,
    )


# ═══════════════════════════════════════════════════════════════
#  Helpers
# ═══════════════════════════════════════════════════════════════

def _reset_cliente():
    """Limpia _cliente_actual entre tests."""
    _cliente_actual.clear()


def _registrar_cliente():
    """Helper: registra un cliente de prueba y devuelve el response."""
    return ejecutar_tool("registrar_datos_cliente", {
        "nombre": "Juan Pérez",
        "cedula": "1234567890",
        "empresa": "Empresa SA",
        "telefono": "3001234567",
    })


# ═══════════════════════════════════════════════════════════════
#  registrar_datos_cliente
# ═══════════════════════════════════════════════════════════════

class TestRegistrarDatosCliente:
    def setup_method(self):
        _reset_cliente()

    def test_registra_datos_basicos(self):
        resp = _registrar_cliente()
        assert resp["registrado"] is True
        assert resp["nombre"] == "Juan Pérez"
        assert resp["cedula"] == "1234567890"
        assert resp["empresa"] == "Empresa SA"
        assert resp["telefono"] == "3001234567"

    def test_retorna_cliente_id(self):
        resp = _registrar_cliente()
        assert "cliente_id" in resp
        assert resp["cliente_id"] == 42

    def test_guarda_en_memoria(self):
        _registrar_cliente()
        assert _cliente_actual["nombre"] == "Juan Pérez"
        assert _cliente_actual["cedula"] == "1234567890"
        assert _cliente_actual["empresa"] == "Empresa SA"
        assert _cliente_actual["telefono"] == "3001234567"
        assert _cliente_actual["cliente_id"] == 42

    def test_funciona_solo_con_requeridos(self):
        _reset_cliente()
        resp = ejecutar_tool("registrar_datos_cliente", {
            "nombre": "Ana",
            "cedula": "9876543210",
        })
        assert resp["registrado"] is True
        assert resp["nombre"] == "Ana"
        assert resp["cedula"] == "9876543210"
        # Sin empresa/telefono no debe fallar
        assert resp.get("empresa") == ""
        assert resp.get("telefono") == ""


# ═══════════════════════════════════════════════════════════════
#  registrar_resumen_llamada
# ═══════════════════════════════════════════════════════════════

class TestRegistrarResumenLlamada:
    def setup_method(self):
        _reset_cliente()
        _registrar_cliente()

    def test_registra_resumen_valido(self):
        resp = ejecutar_tool("registrar_resumen_llamada", {
            "resumen": "Cliente interesado en cloud computing y seguridad.",
            "intention": "calida",
            "score_lead": 75,
            "servicios_interes": ["cloud_computing", "seguridad"],
            "recomendaciones": "Enviar propuesta de servicios administrados.",
        })
        assert resp["registrado"] is True
        assert "llamada_id" in resp

    def test_rechaza_score_menor_a_0(self):
        resp = ejecutar_tool("registrar_resumen_llamada", {
            "resumen": "Test",
            "intention": "calida",
            "score_lead": -1,
        })
        assert "error" in resp
        assert "score_lead" in resp["error"].lower()

    def test_rechaza_score_mayor_a_100(self):
        resp = ejecutar_tool("registrar_resumen_llamada", {
            "resumen": "Test",
            "intention": "calida",
            "score_lead": 101,
        })
        assert "error" in resp
        assert "score_lead" in resp["error"].lower()

    def test_rechaza_intention_invalida(self):
        resp = ejecutar_tool("registrar_resumen_llamada", {
            "resumen": "Test",
            "intention": "super_caliente",
            "score_lead": 50,
        })
        assert "error" in resp
        assert "intention" in resp["error"].lower()

    def test_acepta_intention_fria(self):
        resp = ejecutar_tool("registrar_resumen_llamada", {
            "resumen": "Solo preguntó precios.",
            "intention": "fria",
            "score_lead": 10,
        })
        assert resp["registrado"] is True

    def test_acepta_intention_caliente(self):
        resp = ejecutar_tool("registrar_resumen_llamada", {
            "resumen": "Quiere comprar ya.",
            "intention": "caliente",
            "score_lead": 95,
        })
        assert resp["registrado"] is True

    def test_sin_servicios_no_opcionales_no_falla(self):
        resp = ejecutar_tool("registrar_resumen_llamada", {
            "resumen": "Consulta general.",
            "intention": "fria",
            "score_lead": 5,
        })
        assert resp["registrado"] is True


# ═══════════════════════════════════════════════════════════════
#  registrar_resumen_llamada — sin cliente registrado
# ═══════════════════════════════════════════════════════════════

class TestResumenSinCliente:
    def setup_method(self):
        _reset_cliente()

    def test_rechaza_sin_cliente(self):
        resp = ejecutar_tool("registrar_resumen_llamada", {
            "resumen": "Test",
            "intention": "fria",
            "score_lead": 50,
        })
        assert "error" in resp
        assert "cliente" in resp["error"].lower()


# ═══════════════════════════════════════════════════════════════
#  Fallback timeout — defaults correctos
# ═══════════════════════════════════════════════════════════════

class TestFallbackDefaults:
    def setup_method(self):
        _reset_cliente()
        _registrar_cliente()

    def test_fallback_defaults_son_validos(self):
        """Los defaults del timeout fallback deben pasar validación."""
        resp = ejecutar_tool("registrar_resumen_llamada", {
            "resumen": "Llamada finalizada por tiempo de espera.",
            "intention": "calida",
            "score_lead": 50,
            "servicios_interes": [],
            "recomendaciones": "Cliente no completó la conversación.",
        })
        assert resp["registrado"] is True

    def test_fallback_con_resumen_vacio(self):
        """Resumen vacío debe ser aceptado (es válido)."""
        resp = ejecutar_tool("registrar_resumen_llamada", {
            "resumen": "",
            "intention": "calida",
            "score_lead": 50,
        })
        assert resp["registrado"] is True
