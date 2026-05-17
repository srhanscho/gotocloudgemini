# =============================================================
#  VOICE SESSION — Per-call session state
#  Replaces the global _cliente_actual dict
# =============================================================

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Session:
    """Session state for a single voice call.

    Replaces the module-level _cliente_actual dict that caused race conditions
    when multiple WebSocket connections ran concurrently.
    """

    cliente_id: int | None = None
    cedula: str = ""
    nombre: str = ""
    empresa: str = ""
    telefono: str = ""
    started_at: str = ""

    def mark_started(self) -> None:
        """Record the UTC ISO timestamp when the call started."""
        self.started_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict[str, str | int | None]:
        """Convert to dict format compatible with the old _cliente_actual schema."""
        return {
            "cliente_id": self.cliente_id,
            "nombre": self.nombre,
            "cedula": self.cedula,
            "empresa": self.empresa,
            "telefono": self.telefono,
            "started_at": self.started_at,
        }


__all__ = ["Session"]
