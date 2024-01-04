from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_USER: str  # You may want to adjust the type depending on your use case
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    WAIT_TIME_SETTINGS: int
    NUM_OF_REQUESTS_TO_HIDE_MSG: int
    MAX_MEDIA_SIZE_BYTES: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')


settings = Settings()
