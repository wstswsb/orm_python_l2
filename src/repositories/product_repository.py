from collections.abc import Iterable

from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.models import ProductModel, SoldProductModel


class ProductRepository:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self.sessionmaker = sessionmaker

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
