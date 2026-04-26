import pytest
from src.util.dao import DAO

@pytest.fixture
def dao():
    dao = DAO("task")
    yield dao
    dao.drop()