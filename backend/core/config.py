from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Mirror Reality"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/mirror_reality"
    
    # Redis Cache
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    CACHE_TTL: int = 3600  # 1 hour
    
    # Celery Task Queue
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    PROMETHEUS_PORT: int = 9090
    LOG_LEVEL: str = "INFO"
    
    # AI Model Settings
    MODEL_PATH: str = "models/"
    MODEL_BATCH_SIZE: int = 32
    MODEL_MAX_LENGTH: int = 512
    
    # Blockchain Settings
    SOLANA_RPC_URL: str = "https://api.devnet.solana.com"
    SOLANA_WS_URL: str = "wss://api.devnet.solana.com"
    
    # IPFS Settings
    IPFS_API_URL: str = "http://localhost:5001"
    IPFS_GATEWAY_URL: str = "https://ipfs.io"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 