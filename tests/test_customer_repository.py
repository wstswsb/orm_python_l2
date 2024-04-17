import pytest

from src.repositories.customer_repository import CustomerRepository
from src.structure import Structure
from tests.helpers import store_mock_data


@pytest.fixture
def sut(t_structure: Structure) -> CustomerRepository:
    return t_structure.customer_repository


@pytest.mark.asyncio
async def test_get_most_frequent(sut: CustomerRepository) -> None:
    # Arrange
    await store_mock_data(sut.sessionmaker)

    # Act
    result = await sut.get_most_frequent(5)

    # Assert
    assert len(result) == 5

    assert result[0].id == 3
    assert result[1].id == 4
    assert result[2].id == 5
    assert result[3].id == 1
    assert result[4].id == 2
