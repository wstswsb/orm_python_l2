from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, decimal_10_2


class SoldProductModel(Base):
    __tablename__ = "sold_product"

    id: Mapped[int] = mapped_column(
        BigInteger,
        autoincrement=True,
        primary_key=True,
    )
    quantity: Mapped[int]
    total_price: Mapped[decimal_10_2]
    date_of_sale: Mapped[datetime]

    cashier_id: Mapped[int] = mapped_column(ForeignKey("cashier.id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    product_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            column="product.id",
            ondelete="SET NULL",
        )
    )
