"""
Application settings.

Loads environment variables from the .env file using Pydantic.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    openai_api_key: str | None = None
    groq_api_key: str
    tavily_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()