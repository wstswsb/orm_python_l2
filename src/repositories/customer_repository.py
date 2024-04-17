from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.models import CustomerModel, SoldProductModel


class CustomerRepository:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self.sessionmaker = sessionmaker

    async def get(self, ident: int) -> CustomerModel | None:
        async with self.sessionmaker() as session:
            result = await session.get(CustomerModel, ident)
        return result

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
                    most_frequent_ids_subquery.c.purchases.desc(),  # noqa
                    CustomerModel.id.asc(),
                )
            )
            result = await session.scalars(statement)

        return list(result)

    async def get_least_frequent(self) -> CustomerModel | None:
        async with self.sessionmaker() as session:
            least_frequent_id_subquery = (
                select(SoldProductModel.customer_id)
                .group_by(SoldProductModel.customer_id)
                .order_by(asc(func.count()), asc(SoldProductModel.customer_id))
                .limit(1)
                .scalar_subquery()
            )  # fmt: skip
            statement = select(CustomerModel).where(
                CustomerModel.id == least_frequent_id_subquery
            )
            result = await session.scalar(statement)
        return result
