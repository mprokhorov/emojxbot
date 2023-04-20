from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    empty_emoji_id: SecretStr

    redis_host: SecretStr
    redis_port: SecretStr
    redis_username: SecretStr
    redis_password: SecretStr

    webhook_host: SecretStr
    webhook_path: SecretStr

    webapp_host: SecretStr
    webapp_port: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
