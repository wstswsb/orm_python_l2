from decimal import Decimal
from typing import Annotated

from sqlalchemy import MetaData, Numeric
from sqlalchemy.orm import DeclarativeBase, mapped_column

decimal_10_2 = Annotated[Decimal, mapped_column(Numeric(10, 2))]


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        },
    )
