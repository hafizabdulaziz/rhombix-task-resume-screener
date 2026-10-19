from src.services.education_parser import EducationParser


def test_education_parser_phd_tier1():
    text = "Ph.D. in Computer Science from Stanford University"
    res = EducationParser.parse_education(text)
    assert res["degree_level"] == "PhD"
    assert res["is_tier_one"] is True
    assert res["score"] == 100.0

def test_education_parser_master():
    text = "Master of Science in Software Engineering"
    res = EducationParser.parse_education(text)
    assert res["degree_level"] == "Master"
    assert res["is_tier_one"] is False
    assert res["score"] == 85.0
