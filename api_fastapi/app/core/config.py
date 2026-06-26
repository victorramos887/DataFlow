from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "api_fastapi"
    app_version: str = "0.1.0"
    debug: bool = False

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "dataflow_postgres"
    postgres_port: int = 5432

    database_url: str | None = None

    otel_exporter_otlp_endpoint: str = "http://dataflow-otel-lgtm:4317"
    otel_service_name: str = "dataflow-api"
    
    access_token_expire_minutes: int = 30
    secret_key: str 

    @model_validator(mode="after")
    def build_database_url(self):
        if not self.database_url:
            self.database_url = (
                f"postgresql+asyncpg://"
                f"{self.postgres_user}:"
                f"{self.postgres_password}@"
                f"{self.postgres_host}:"
                f"{self.postgres_port}/"
                f"{self.postgres_db}"
            )
        return self

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str | None) -> str | None:
        if value is None:
            return value

        if not value.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError(
                "DATABASE_URL must start with 'postgresql://' or 'postgresql+asyncpg://'"
            )

        return value

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
