from sqlalchemy import Interval, asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.sql.functions import concat

from src.models import CashierModel, SoldProductModel


class CashierRepository:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self.sessionmaker = sessionmaker

    async def get_top_seller_last_month(self) -> CashierModel | None:
        async with self.sessionmaker() as session:
            top_seller_subquery = (
                select(SoldProductModel.cashier_id)
                .where(
                    SoldProductModel.date_of_sale.between(
                        func.current_date() - func.cast(concat(1, "month"), Interval) ,
                        func.current_date(),
                    )
                )
                .group_by(SoldProductModel.cashier_id)
                .order_by(
                    desc(func.sum(SoldProductModel.total_price)),
                    asc(SoldProductModel.cashier_id),
                )
                .limit(1)
                .scalar_subquery()
            )  # fmt: skip
            statement = (
                select(CashierModel)
                .where(CashierModel.id == top_seller_subquery)
            )  # fmt: skip
            result = await session.scalar(statement)
        return result
