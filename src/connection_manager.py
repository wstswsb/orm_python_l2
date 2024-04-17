from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class ConnectionManager:
    def __init__(
        self,
        connection_url: str,
        echo: bool,
    ) -> None:
        self._connection_url = connection_url
        self._echo = echo
        self._engine = self._build_engine()
        self._sessionmaker = self._build_sessionmaker()

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        return self._sessionmaker

    def _build_engine(self) -> AsyncEngine:
        return create_async_engine(self._connection_url, echo=self._echo)

    def _build_sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
