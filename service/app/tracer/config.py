from typing import List, Optional

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator, RedisDsn


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v

    PROJECT_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: Optional[str] = None
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    REDIS_URI: RedisDsn = "redis://redis:6379/0"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v, values):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
            port=values.get("POSTGRES_PORT" or "5432"),
        )

    ENV: str
    REINITIALIZE_DB: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
print(settings.dict())
