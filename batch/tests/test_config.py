from src.core.config import Settings

def test_should_have_correct_default_settings():
    """Test default values for settings attributes.
    
    Arrange: Instantiate Settings object.
    Act: No direct action needed.
    Assert: Check that all defaults match expectations.
    """
    settings = Settings()
    
    assert settings.PROJECT_NAME == "rag-cosense-batch"
    assert settings.LOG_LEVEL == "info"
    assert settings.ELASTICSEARCH_URL == "http://elasticsearch:9200"
    assert settings.ENCODER_SERVICE_URL == "http://encoder:8001"

def test_should_override_settings_with_env_vars(monkeypatch):
    """Test environment variable overrides for calibration.
    
    Arrange: Mock environment variables using monkeypatch.
    Act: Instantiate Settings object.
    Assert: Check for overridden values.
    """
    monkeypatch.setenv("PROJECT_NAME", "batch-test")
    monkeypatch.setenv("LOG_LEVEL", "debug")
    
    settings = Settings()
    assert settings.PROJECT_NAME == "batch-test"
    assert settings.LOG_LEVEL == "debug"
