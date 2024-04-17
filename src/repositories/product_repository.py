from collections.abc import Iterable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.models import ProductModel


class ProductRepository:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self.sessionmaker = sessionmaker

    async def save_many(self, models: Iterable[ProductModel]) -> list[ProductModel]:
        async with self.sessionmaker() as session:
            session.add_all(models)
            await session.flush()
            await session.commit()
        return list(models)
