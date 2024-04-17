from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class CustomerModel(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(
        BigInteger,
        autoincrement=True,
        primary_key=True,
    )
    fullname: Mapped[str]
    date_of_birth: Mapped[datetime]
    email: Mapped[str]
    phone_number: Mapped[str]
