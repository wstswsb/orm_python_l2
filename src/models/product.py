from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, decimal_10_2


class ProductModel(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(
        BigInteger,
        autoincrement=True,
        primary_key=True,
    )
    title: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[decimal_10_2]
