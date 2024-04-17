import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.connection_manager import ConnectionManager
from src.models.base import Base
from src.settings import DBSettings
from src.structure import Structure


@pytest.fixture(scope="session")
def t_db_settings() -> DBSettings:
    db_settings = DBSettings()
    db_settings.debug = True
    db_settings.name = "test-db"
    return db_settings


@pytest_asyncio.fixture
async def t_sessionmaker(t_db_settings: DBSettings):  # type: ignore
    connection_manager = ConnectionManager(
        connection_url=t_db_settings.connection_url,
        echo=t_db_settings.debug,
    )
    async with connection_manager.engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield connection_manager.sessionmaker
    async with connection_manager.engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def t_structure(
    t_sessionmaker: async_sessionmaker[AsyncSession],
    t_db_settings: DBSettings,
) -> Structure:
    structure = Structure(t_db_settings)
    structure.sessionmaker = t_sessionmaker  # noqa
    return structure
