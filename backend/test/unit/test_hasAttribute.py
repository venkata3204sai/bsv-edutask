import pytest
from src.util.helpers import hasAttribute

@pytest.fixture
def obj():
    return {"name": "sai"}

@pytest.mark.unit
def test_hasAttribute1(obj):
    result = hasAttribute(obj, "name")
    assert result == True

@pytest.mark.unit
def test_hasAttribute2(obj):
    result = hasAttribute(obj, "age")
    assert result == False

@pytest.mark.unit
def test_hasAttribute3():
    result = hasAttribute({}, "name")
    assert result == False