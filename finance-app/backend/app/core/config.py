from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Finance App API"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "finance_app"
    
    # Redis settings
    REDIS_HOST: str = "redis"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-for-jwt"
    
    # Email settings
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: str = ""
    EMAIL_PASSWORD: str = ""
    
    # Telegram settings
    TELEGRAM_BOT_TOKEN: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
