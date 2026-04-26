import uuid
import pytest

pytestmark = pytest.mark.integration


def test_create_valid(dao):
    data = {
        "title": str(uuid.uuid4()),
        "description": "This is a test"
    }

    result = dao.create(data)

    assert result["_id"] is not None


import pytest
import uuid

def test_create_missing_title(dao):
    data = {
        "description": "Missing title"
    }

    with pytest.raises(Exception):
        dao.create(data)


def test_create_wrong_type(dao):
    data = {
        "title": 123,
        "description": "Test"
    }

    with pytest.raises(Exception):
        dao.create(data)



from datetime import datetime

def test_create_with_optional_fields(dao):
    data = {
        "title": str(uuid.uuid4()),
        "description": "Test",
        "categories": ["school", "urgent"],
        "startdate": datetime.now()
    }

    result = dao.create(data)

    assert result["categories"] == ["school", "urgent"]


def test_create_invalid_categories(dao):
    data = {
        "title": str(uuid.uuid4()),
        "description": "Test",
        "categories": "not an array"
    }

    with pytest.raises(Exception):
        dao.create(data)
