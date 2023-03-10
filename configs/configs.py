from pathlib import Path
from typing import List

from pydantic import BaseModel, BaseSettings, Field, SecretStr


class CommonConfig(BaseSettings):
    token: SecretStr = Field(..., env="token")
    admins: List[int] = Field(..., env="admins")
    log_cfg_path: str = Field(
        f"{Path(__file__).parent}/logging.json", env="log_cfg_path"
    )
    task_limit: int = Field(5, env="task_limit")
    throttling_limit: int = Field(1, env="throttling_limit")

    class Config:
        case_sentive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


class DbConfig(BaseSettings):
    driver: str = Field(..., env="driver")
    user: str = Field(..., env="user")
    password: SecretStr = Field(..., env="password")
    host: str = Field(..., env="host")
    port: int = Field(..., env="port")
    sid: str = Field("", env="sid")

    url: str = Field(None, env="url")

    echo_db_queries: bool = Field(False, env="echo_db_queries")
    echo_db_pool: bool = Field(False, env="echo_db_pool")

    @property
    def dsn(self):
        return (
            f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.sid}"
            if self.url is None
            else self.url
        )

    class Config:
        case_sentive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


class ConfigProvider(BaseModel):
    db: DbConfig = DbConfig()
    common: CommonConfig = CommonConfig()
