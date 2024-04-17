from decimal import Decimal

import pytest
from sqlalchemy import select

from src.models import ProductModel
from src.repositories.product_repository import ProductRepository
from src.structure import Structure
from tests.helpers import store_mock_data


@pytest.fixture
def sut(t_structure: Structure) -> ProductRepository:
    return t_structure.product_repository


@pytest.mark.asyncio
async def test_save_many(sut: ProductRepository) -> None:
    # Arrange
    await store_mock_data(sut.sessionmaker)
    models = [
        ProductModel(title=f"t_{i}", quantity=i, price=Decimal(f"{i}.{i}"))
        for i in range(5)
    ]

    # Act
    result = await sut.save_many(models)

    # Assert
    assert len(result) == 5


@pytest.mark.asyncio
async def test_get_best_selling(sut: ProductRepository) -> None:
    # Arrange
    await store_mock_data(sut.sessionmaker)

    # Act
    result = await sut.get_best_selling()

    # Assert
    assert result is not None
    assert result.id == 15


@pytest.mark.asyncio
async def test_get_cheapest_from_best_selling(sut: ProductRepository) -> None:
    # Arrange
    await store_mock_data(sut.sessionmaker)

    # Act
    result = await sut.get_cheapest_from_best_selling(top_n=5)

    # Assert
    assert result is not None
    assert result.id == 14


@pytest.mark.asyncio
async def test_delete_leas_sold(sut: ProductRepository) -> None:
    # Arrange
    await store_mock_data(sut.sessionmaker)
    async with sut.sessionmaker() as session:
        all_product_ids_before = await session.scalars(select(ProductModel.id))

    # Act
    await sut.delete_least_sold(top_n=5)

    # Assert
    async with sut.sessionmaker() as session:
        all_product_ids_after = await session.scalars(select(ProductModel.id))

    expected_deleted_ids = {1, 2, 3, 4, 5}
    deleted_ids = set(all_product_ids_before).difference(all_product_ids_after)
    assert expected_deleted_ids == deleted_ids
