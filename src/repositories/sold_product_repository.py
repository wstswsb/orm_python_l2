from sqlalchemy import asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.models import SoldProductModel


class SoldProductRepository:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self.sessionmaker = sessionmaker

    async def get_with_largest_total_price(self) -> SoldProductModel | None:
        async with self.sessionmaker() as session:
            result = await session.scalar(
                select(SoldProductModel)
                .order_by(
                    desc(SoldProductModel.total_price),
                    asc(SoldProductModel.product_id),
                )
                .limit(1)
            )  # fmt: skip
        return result
