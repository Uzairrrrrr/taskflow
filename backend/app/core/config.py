import os

class Settings:
    PROJECT_NAME: str = "TaskFlow API"
    PROJECT_VERSION: str = "1.0.0"
    SECRET_KEY: str = "your-local-development-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

settings = Settings()