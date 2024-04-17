from functools import cached_property

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.connection_manager import ConnectionManager
from src.repositories.customer_repository import CustomerRepository
from src.repositories.product_repository import ProductRepository
from src.settings import DBSettings


class Structure:
    def __init__(self, db_settings: DBSettings):
        self.db_settings = db_settings

    @cached_property
    def sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        return self.connection_manager.sessionmaker

    @cached_property
    def connection_manager(self) -> ConnectionManager:
        return ConnectionManager(
            connection_url=self.db_settings.connection_url,
            echo=self.db_settings.debug,
        )

    @cached_property
    def product_repository(self) -> ProductRepository:
        return ProductRepository(sessionmaker=self.sessionmaker)

    @cached_property
    def customer_repository(self) -> CustomerRepository:
        return CustomerRepository(sessionmaker=self.sessionmaker)


_db_settings = DBSettings()
print(_db_settings.connection_url)
structure = Structure(_db_settings)
