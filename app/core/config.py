"""Application configuration loaded from environment variables or a .env file."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Central settings for the application.

    Values are read from environment variables (case-insensitive). A `.env`
    file in the working directory is also supported as a fallback.

    Attributes:
        database_url: SQLAlchemy-compatible connection string for PostgreSQL.
        secret_key: Secret used to sign JWT tokens. Must be changed before
            deploying to production.
        token_expire_minutes: Lifetime of an issued JWT token in minutes.
            Defaults to one week (10 080 minutes).
    """

    database_url: str = "postgresql://mt:mt@localhost:5432/moneytracker"
    secret_key: str = "changeme"
    token_expire_minutes: int = 60 * 24 * 7

    model_config = {"env_file": ".env"}


settings = Settings()
