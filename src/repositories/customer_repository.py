from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.models import CustomerModel, SoldProductModel


class CustomerRepository:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self.sessionmaker = sessionmaker

    async def get_most_frequent(self, max_number: int) -> list[CustomerModel]:
        async with self.sessionmaker() as session:
            most_frequent_ids_subquery = (
                select(
                    SoldProductModel.customer_id,
                    func.count().label("purchases")
                )
                .group_by(SoldProductModel.customer_id)
                .order_by(desc("purchases"), SoldProductModel.customer_id.asc())
                .limit(max_number)
                .subquery()
            )  # fmt: skip
            statement = (
                select(CustomerModel)
                .join(
                    most_frequent_ids_subquery,
                    CustomerModel.id == most_frequent_ids_subquery.c.customer_id,
                )
                .order_by(
                    most_frequent_ids_subquery.c.purchases.desc(),
                    CustomerModel.id.asc(),
                )
            )
            result = await session.scalars(statement)

        return list(result)
