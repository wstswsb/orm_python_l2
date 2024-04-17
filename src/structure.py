from functools import cached_property

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.connection_manager import ConnectionManager
from src.get_best_deal_context_use_case import GetBestDealContextUseCase
from src.repositories.cashier_repository import CashierRepository
from src.repositories.customer_repository import CustomerRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.sold_product_repository import SoldProductRepository
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

    @cached_property
    def cashier_repository(self) -> CashierRepository:
        return CashierRepository(sessionmaker=self.sessionmaker)

    @cached_property
    def sold_product_repository(self) -> SoldProductRepository:
        return SoldProductRepository(sessionmaker=self.sessionmaker)

    @cached_property
    def get_best_deal_context_use_case(self) -> GetBestDealContextUseCase:
        return GetBestDealContextUseCase(
            cashier_repository=self.cashier_repository,
            product_repository=self.product_repository,
            customer_repository=self.customer_repository,
            sold_product_repository=self.sold_product_repository,
        )


_db_settings = DBSettings()
print(_db_settings.connection_url)
structure = Structure(_db_settings)
