from datetime import UTC, datetime
from typing import Any

import structlog

logger = structlog.get_logger()

class AuditLogger:
    """
    Immutable system activity and audit logging engine.
    Records HR actions such as candidate status updates, job creation, and export events.
    """
    
    @staticmethod
    def log_action(actor: str, action: str, target_type: str, target_id: str, details: dict[str, Any] = None):
        audit_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "actor": actor,
            "action": action,
            "target_type": target_type,
            "target_id": target_id,
            "details": details or {}
        }
        logger.info("audit_event_recorded", **audit_entry)
        return audit_entry
