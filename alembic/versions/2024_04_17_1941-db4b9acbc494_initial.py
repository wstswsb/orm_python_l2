"""initial

Revision ID: db4b9acbc494
Revises:
Create Date: 2024-04-17 19:41:25.086155

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "db4b9acbc494"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cashier",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("fullname", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cashier")),
    )
    op.create_table(
        "customer",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("fullname", sa.String(), nullable=False),
        sa.Column("date_of_birth", sa.DateTime(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone_number", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_customer")),
    )
    op.create_table(
        "product",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_product")),
    )
    op.create_table(
        "sold_product",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("total_price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("date_of_sale", sa.DateTime(), nullable=False),
        sa.Column("cashier_id", sa.BigInteger(), nullable=False),
        sa.Column("customer_id", sa.BigInteger(), nullable=False),
        sa.Column("product_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cashier_id"],
            ["cashier.id"],
            name=op.f("fk_sold_product_cashier_id_cashier"),
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customer.id"],
            name=op.f("fk_sold_product_customer_id_customer"),
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
            name=op.f("fk_sold_product_product_id_product"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sold_product")),
    )


def downgrade() -> None:
    op.drop_table("sold_product")
    op.drop_table("product")
    op.drop_table("customer")
    op.drop_table("cashier")
