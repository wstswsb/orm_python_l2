import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.get_best_deal_context_use_case import DealContext, GetBestDealContextUseCase
from src.structure import Structure
from tests.helpers import store_mock_data


@pytest.fixture
def sut(t_structure: Structure) -> GetBestDealContextUseCase:
    return t_structure.get_best_deal_context_use_case


@pytest.mark.asyncio
async def test_execute(
    sut: GetBestDealContextUseCase,
    t_sessionmaker: async_sessionmaker[AsyncSession],
) -> None:
    # Arrange
    await store_mock_data(t_sessionmaker)

    # Act
    result = await sut.execute()

    # Assert
    assert isinstance(result, DealContext)
    assert result.cashier.id == 5
    assert result.customer.id == 5
    expected_product_ids = [5, 11, 12, 13, 15]
    assert [p.id for p in result.products_for_all_time] == expected_product_ids
