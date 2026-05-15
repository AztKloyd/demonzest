##Appname, API Prefixのような設定値を管理するファイル

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "demonzest"
    api_prefix: str = "/api"
    database_url: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
