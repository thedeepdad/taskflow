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

    @property
    def private_key(self): 
        return Path(self.path_private_key).read_text()

    @property
    def  public_key(self): 
        return Path(self.path_public_key).read_text()

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

settings = Settings()

