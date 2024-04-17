from dataclasses import dataclass

from src.models import CashierModel, CustomerModel, ProductModel
from src.repositories.cashier_repository import CashierRepository
from src.repositories.customer_repository import CustomerRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.sold_product_repository import SoldProductRepository


@dataclass(frozen=True, slots=True)
class DealContext:
    customer: CustomerModel
    cashier: CashierModel
    products_for_all_time: list[ProductModel]


class GetBestDealContextUseCase:
    def __init__(
        self,
        cashier_repository: CashierRepository,
        customer_repository: CustomerRepository,
        product_repository: ProductRepository,
        sold_product_repository: SoldProductRepository,
    ):
        self._cashier_repository = cashier_repository
        self._customer_repository = customer_repository
        self._product_repository = product_repository
        self._sold_product_repository = sold_product_repository

    async def execute(self) -> DealContext:
        sold_product = (
            await self._sold_product_repository.get_with_largest_total_price()
        )
        if sold_product is None:
            raise ValueError("Sold product is None")

        cashier = await self._cashier_repository.get(sold_product.cashier_id)
        if cashier is None:
            raise ValueError("Cashier is None")

        customer = await self._customer_repository.get(sold_product.customer_id)
        if customer is None:
            raise ValueError("Customer is None")
        products = await self._product_repository.get_customer_products(customer.id)
        return DealContext(
            customer=customer,
            cashier=cashier,
            products_for_all_time=products,
        )
