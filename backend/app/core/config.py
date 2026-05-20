from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "demonzest"
    api_prefix: str = "/api"
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    admin_email: str | None = None
    admin_password: str | None = None
    admin_name: str = "Admin"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
