from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"
    API_BASE_URL: str = "http://localhost:8000"
    
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    TOP_K: int = 4
    SCORE_THRESHOLD: float = 0.0
    VECTOR_STORE_DIR: str = "vector_store"
    
    LLM_MODEL: str = "gemini-flash-latest"
    LLM_TEMPERATURE: float = 0.7
    LLM_TOP_P: float = 0.95
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

settings = Settings()
