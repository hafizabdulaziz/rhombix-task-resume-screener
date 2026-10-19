from src.services.export import ReportExporter


def test_export_excel_and_csv():
    mock_results = [
        {
            "candidate_name": "John Doe",
            "candidate_email": "john@example.com",
            "composite_score": 88.5,
            "skill_match_score": 90.0,
            "experience_match_score": 100.0,
            "semantic_score": 75.0,
            "status": "shortlisted",
            "skill_scores": [
                {"skill_name": "python", "is_matched": True, "match_type": "exact"},
                {"skill_name": "docker", "is_matched": False, "match_type": "missing"}
            ]
        }
    ]

    excel_bytes = ReportExporter.generate_excel_report("Python Engineer", mock_results)
    assert isinstance(excel_bytes, bytes)
    assert len(excel_bytes) > 0

    csv_str = ReportExporter.generate_csv_report(mock_results)
    assert isinstance(csv_str, str)
    assert "John Doe" in csv_str
    assert "88.5" in csv_str
