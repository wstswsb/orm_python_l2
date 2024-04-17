import asyncio
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

mock_customer_sql = Path("tests/mock_sql/customer.sql").read_text()
mock_product_sql = Path("tests/mock_sql/product.sql").read_text()
mock_cashier_sql = Path("tests/mock_sql/cashier.sql").read_text()
mock_sold_product_sql = Path("tests/mock_sql/sold_product.sql").read_text()


async def store_mock_data(sessionmaker: async_sessionmaker[AsyncSession]) -> None:
    async with sessionmaker() as session:
        await session.execute(text(mock_customer_sql))
        await session.execute(text(mock_product_sql))
        await session.execute(text(mock_cashier_sql))
        await session.execute(text(mock_sold_product_sql))
        await session.commit()


if __name__ == "__main__":
    from src.structure import structure

    asyncio.run(store_mock_data(structure.sessionmaker))
