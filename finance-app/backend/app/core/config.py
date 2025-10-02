from typing import List, Optional

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration centralisée de l'application."""

    PROJECT_NAME: str = "Finance App API"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Base de données
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "finance_app"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # Cache et files d'attente
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    # Sécurité
    SECRET_KEY: str = "your-secret-key-for-jwt"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 jours

    # Services financiers
    DEFAULT_FINANCIAL_API: str = "yfinance"
    ALPHAVANTAGE_API_KEY: Optional[str] = None
    FINNHUB_API_KEY: Optional[str] = None

    # Notifications
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )

    def model_post_init(self, __context: object) -> None:
        """Complète les paramètres dépendants après le chargement des variables d'environnement."""

        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
            )


settings = Settings()
