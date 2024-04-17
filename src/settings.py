from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["db_settings"]


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_prefix="db_",
    )
    driver: str
    username: str
    password: str
    host: str
    port: int
    name: str
    debug: bool

    @property
    def connection_url(self) -> str:
        return (
            f"{self.driver}://"
            f"{self.username}:{self.password}"
            f"@{self.host}:{self.port}"
            f"/{self.name}"
        )


db_settings = DBSettings()
