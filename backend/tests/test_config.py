import os
import pytest
from src.core.config import Settings

def test_should_have_correct_default_settings():
    """Test default values for settings.
    
    Arrange: Create a Settings instance.
    Act: No direct action needed.
    Assert: Check default values.
    """
    settings = Settings()
    
    assert settings.PROJECT_NAME == "rag-cosense"
    assert settings.API_V1_STR == "/api/v1"
    assert settings.ELASTICSEARCH_URL == "http://elasticsearch:9200"
    assert settings.OLLAMA_BASE_URL == "http://ollama:11434"
    assert settings.ENCODER_SERVICE_URL == "http://encoder:8001"
    assert settings.EMBEDDING_MODEL == "gemma3"

def test_should_override_settings_with_env_vars(monkeypatch):
    """Test environment variable overrides for settings using monkeypatch.
    
    Arrange: Set environment variables using monkeypatch.
    Act: Create a Settings instance.
    Assert: Verify overridden settings values.
    """
    monkeypatch.setenv("PROJECT_NAME", "test-project")
    monkeypatch.setenv("LOG_LEVEL", "debug")
    
    settings = Settings()
    assert settings.PROJECT_NAME == "test-project"
    assert settings.LOG_LEVEL == "debug"

# Clean up environment variables if we used os.environ.update (although dict update on environ is not directly possible)
# Actually, using mock or os.environ for individual keys is better.
