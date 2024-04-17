from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class CashierModel(Base):
    __tablename__ = "cashier"

    id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, primary_key=True)
    fullname: Mapped[str]
    email: Mapped[str]
