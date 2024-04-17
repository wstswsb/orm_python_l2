from collections.abc import Iterable

from sqlalchemy import asc, delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.models import ProductModel, SoldProductModel


class ProductRepository:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self.sessionmaker = sessionmaker

    async def get_customer_products(self, customer_id: int) -> list[ProductModel]:
        async with self.sessionmaker() as session:
            product_ids_subquery = (
                select(SoldProductModel.product_id)
                .where(SoldProductModel.customer_id == customer_id)
                .distinct()
            )
            statement = (
                select(ProductModel)
                .where(ProductModel.id.in_(product_ids_subquery))
                .order_by(asc(ProductModel.id))
            )  # fmt: skip

            scalar_result = await session.scalars(statement)
            product_models = scalar_result.all()
        return list(product_models)

    async def save_many(self, models: Iterable[ProductModel]) -> list[ProductModel]:
        async with self.sessionmaker() as session:
            session.add_all(models)
            await session.flush()
            await session.commit()
        return list(models)

    async def get_best_selling(self) -> ProductModel | None:
        async with self.sessionmaker() as session:
            best_selling_id_subquery = (
                select(SoldProductModel.product_id)
                .group_by(SoldProductModel.product_id)
                .order_by(
                    desc(func.sum(SoldProductModel.quantity)),
                    asc(SoldProductModel.product_id),
                )
                .limit(1)
                .scalar_subquery()
            )  # fmt: skip
            statement = (
                select(ProductModel)
                .where(ProductModel.id == best_selling_id_subquery)
            )  # fmt: skip
            result = await session.scalar(statement)
        return result

    async def get_cheapest_from_best_selling(self, top_n: int) -> ProductModel | None:
        async with self.sessionmaker() as session:
            best_selling_ids_subquery = (
                select(SoldProductModel.product_id)
                .group_by(SoldProductModel.product_id)
                .order_by(
                    desc(func.sum(SoldProductModel.quantity)),
                    asc(SoldProductModel.product_id),
                )
                .limit(top_n)
            )
            statement = (
                select(ProductModel)
                .where(ProductModel.id.in_(best_selling_ids_subquery))
                .order_by(
                    asc(ProductModel.price),
                    asc(ProductModel.id),
                )
                .limit(1)
            )
            result = await session.scalar(statement)
        return result

    async def delete_least_sold(self, top_n: int) -> None:
        async with self.sessionmaker() as session:
            least_selling_ids_subquery = (
                select(SoldProductModel.product_id)
                .group_by(SoldProductModel.product_id)
                .order_by(
                    asc(func.sum(SoldProductModel.quantity)),
                    asc(SoldProductModel.product_id)
                )
                .limit(top_n)
            )  # fmt: skip
            statement = (
                delete(ProductModel)
                .where(ProductModel.id.in_(least_selling_ids_subquery))
            )  # fmt: skip

            await session.execute(statement)
            await session.commit()
