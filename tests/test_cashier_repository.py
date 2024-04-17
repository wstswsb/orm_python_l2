from datetime import date

import pytest

from src.repositories.cashier_repository import CashierRepository
from src.structure import Structure
from tests.helpers import store_mock_data


@pytest.fixture
def sut(t_structure: Structure) -> CashierRepository:
    return t_structure.cashier_repository


@pytest.mark.skipif(
    date.today() > date(year=2024, month=4, day=17),
    reason="Test depends on today's date, which is computed on the database side",
)
@pytest.mark.asyncio
async def test_top_seller_last_month(sut: CashierRepository) -> None:
    # Arrange
    await store_mock_data(sut.sessionmaker)

    # Act 5
    result = await sut.get_top_seller_last_month()

    # Assert
    assert result is not None
    assert result.id == 5
