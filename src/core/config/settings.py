"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    civitai_api_token: str = ""
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    def validate_token(self) -> None:
        """Validate that API token is set."""
        if not self.civitai_api_token:
            raise ValueError(
                "CIVITAI_API_TOKEN not set. Please create a .env file with your API token.\n"
                "Get your token from: https://civitai.com/user/account"
            )


settings = Settings()
