from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configuration settings for the application.

    Attributes:
        PROJECT_NAME (str): Name of the project.
        API_V1_STR (str): API version string.
        LOG_LEVEL (str): Logging level (debug, info, warning, error).
        ELASTICSEARCH_URL (str): Connection URL for Elasticsearch.
        OLLAMA_BASE_URL (str): Base URL for Ollama API.
        COSENSE_PROJECT_NAME (str): Name of the target Cosense project.
        COSENSE_SID (str): Session ID for Cosense API.
    """
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "rag-cosense"
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = "info"

    # External Services
    ELASTICSEARCH_URL: str = "http://elasticsearch:9200"
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    ENCODER_SERVICE_URL: str = "http://encoder:8001"
    EMBEDDING_MODEL: str = "gemma3"

    # Cosense Configuration
    COSENSE_PROJECT_NAME: str = ""
    COSENSE_SID: str = ""

settings = Settings()
