from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = os.getenv('ENV_FILE', '.env')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ENV_FILE,
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # application
    title: str
    localhost: str
    format_logging: str

    # security
    path_private_key: str
    path_public_key: str
    algorithm: str
    access_token_exp: int
    refresh_token_exp: int

    # database
    db_name: str
    db_user: str
    db_password: str
    db_port: int
    db_host: str

    # rabbitmq
    rabbit_user: str
    rabbit_password: str
    rabbit_port: int
    rabbit_port_gui: int
    rabbit_host: str
    rabbit_exchange: str = 'taskflow.events'
    rabbit_queue_email: str = 'email_events'

    # smtp
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    smtp_from: str

    @property
    def private_key(self): return Path(self.path_private_key).read_text()

    @property
    def public_key(self): return Path(self.path_public_key).read_text()

    @property
    def async_db_url(self):
        return (
            f'postgresql+asyncpg://'
            f'{self.db_user}:{self.db_password}@'
            f'{self.db_host}:{self.db_port}/'
            f'{self.db_name}'
        )

    @property
    def sync_db_url(self):
        return (
            f'postgresql://{self.db_user}:{self.db_password}@'
            f'{self.db_host}:{self.db_port}/'
            f'{self.db_name}'
        )

    @property
    def rabbit_url(self):
        return (
            f"amqp://{self.rabbit_user}:{self.rabbit_password}"
            f"@{self.rabbit_host}:{self.rabbit_port}/"
        )


settings = Settings()
