import pytest
from src.db import CustomDB
from collections import defaultdict


@pytest.fixture
def db():
    """Чистый экземпляр CustomDB."""
    return CustomDB()


@pytest.fixture
def db_with_data(db):
    """Фикстура с предзаполненными данными."""
    db.set("A", "1")
    db.set("B", "2")
    db.set("C", "3")
    return db


@pytest.fixture
def db_in_transaction(db_with_data):
    """Фикстура с активной транзакцией."""
    db_with_data.begin()
    db_with_data.set("C", "5")
    return db_with_data
