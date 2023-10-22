from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    TELEGRAM_BOT_TOKEN: SecretStr = SecretStr("default")
    TELEGRAM_BOT_ADMIN_IDS: list[int]

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USER: str = ""
    REDIS_PASSWORD: SecretStr
    REDIS_DB: str

    def build_db_connection_uri(
        self,
        *,
        driver: str | None = None,
        host: str | None = None,
        port: int | None = None,
        user: str | None = None,
        password: str | None = None,
        database: str | None = None,
    ) -> str:
        return "postgresql+{}://{}:{}@{}:{}/{}".format(
            driver or "asyncpg",
            user or self.POSTGRES_USER,
            password or self.POSTGRES_PASSWORD.get_secret_value(),
            host or self.POSTGRES_HOST,
            port or self.POSTGRES_PORT,
            database or self.POSTGRES_DB,
        )

    def build_redis_connection_uri(
        self,
        *,
        host: str | None = None,
        port: int | None = None,
        user: str | None = None,
        password: str | None = None,
        database: str | None = None,
    ) -> str:
        return "redis://{}:{}@{}:{}/{}".format(
            user or self.REDIS_USER,
            password or self.REDIS_PASSWORD.get_secret_value(),
            host or self.REDIS_HOST,
            port or self.REDIS_PORT,
            database or self.REDIS_DB,
        )
