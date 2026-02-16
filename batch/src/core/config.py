from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configuration settings for the batch application."""
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "rag-cosense-batch"
    LOG_LEVEL: str = "info"

    # External Services
    ELASTICSEARCH_URL: str = "http://elasticsearch:9200"
    ENCODER_SERVICE_URL: str = "http://encoder:8001"
    
    # Cosense Configuration
    COSENSE_PROJECT_NAME: str = ""
    COSENSE_SID: str = ""

settings = Settings()
