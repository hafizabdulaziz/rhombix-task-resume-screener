from src.services.audit import AuditLogger


def test_audit_logger():
    entry = AuditLogger.log_action(
        actor="recruiter@rhombix.com",
        action="SHORTLIST_CANDIDATE",
        target_type="Candidate",
        target_id="12345",
        details={"score": 92.5}
    )
    assert entry["actor"] == "recruiter@rhombix.com"
    assert entry["action"] == "SHORTLIST_CANDIDATE"
    assert entry["target_id"] == "12345"
    assert entry["details"]["score"] == 92.5
    assert "timestamp" in entry
