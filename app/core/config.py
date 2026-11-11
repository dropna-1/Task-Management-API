from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

setting = Setting()