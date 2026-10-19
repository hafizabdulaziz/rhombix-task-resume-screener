from src.core.config import settings
from src.main import create_app


def test_settings_loaded():
    assert settings.app_name == "Rhombix ResumeScreener Pro"
    assert settings.api_v1_str == "/api/v1"

def test_app_factory():
    app = create_app()
    assert app.title == "Rhombix ResumeScreener Pro"
