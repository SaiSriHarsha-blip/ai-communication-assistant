from functools import lru_cache
from typing import List, Union
# pyrefly: ignore [missing-import]
from pydantic import Field, SecretStr, field_validator
# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application configuration managed via pydantic-settings.
    """
    GEMINI_API_KEY: SecretStr = Field(
        default=SecretStr(""),
        description="Google Gemini API Key",
    )
    GEMINI_MODEL: str = Field(
        default="gemini-2.5-flash",
        description="Gemini model name to use for generation",
    )
    FRONTEND_URL: str = Field(
        default="http://localhost:3000",
        description="Primary frontend URL",
    )
    ALLOWED_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://ai-communication-assistant-sri-harsha.vercel.app",
        ],
        description="Allowed CORS origins",
    )
    ENVIRONMENT: str = Field(
        default="development",
        description="Deployment environment (development, staging, production)",
    )
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level",
    )
    RATE_LIMIT: str = Field(
        default="10/minute",
        description="Default endpoint rate limit",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: Union[str, List[str]]) -> List[str]:
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return []
            if value.startswith("[") and value.endswith("]"):
                import json
                try:
                    return json.loads(value)
                except Exception:
                    pass
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    def get_all_allowed_origins(self) -> List[str]:
        """
        Merge ALLOWED_ORIGINS and FRONTEND_URL without duplicates.
        """
        origins = list(self.ALLOWED_ORIGINS)
        if self.FRONTEND_URL and self.FRONTEND_URL not in origins:
            origins.append(self.FRONTEND_URL)
        return origins


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
