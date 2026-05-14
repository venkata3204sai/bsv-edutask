import uuid
import pytest

from unittest.mock import patch
from src.util.dao import DAO

pytestmark = pytest.mark.integration


@pytest.fixture
def dao_instance():

    # Mock validator dependency
    with patch("src.util.dao.getValidator") as mock_validator:

        # minimal valid mocked validator
        mock_validator.return_value = {
            "$jsonSchema": {
                "bsonType": "object"
            }
        }

        dao = DAO("task")

        yield dao

        dao.drop()


def build_task():
    return {
        "title": f"task-{uuid.uuid4()}",
        "description": "integration testing task"
    }


def test_create_success(dao_instance):

    task = build_task()

    result = dao_instance.create(task)

    assert result["_id"] is not None
    assert result["title"] == task["title"]


def test_create_missing_title(dao_instance):

    invalid_task = {
        "description": "missing title"
    }

    result = dao_instance.create(invalid_task)

    assert result["_id"] is not None


def test_create_invalid_type(dao_instance):

    invalid_task = {
        "title": 12345,
        "description": "wrong datatype"
    }

    result = dao_instance.create(invalid_task)

    assert result["_id"] is not None


def test_create_with_optional_fields(dao_instance):

    task = {
        "title": f"optional-{uuid.uuid4()}",
        "description": "optional field test",
        "done": False
    }

    result = dao_instance.create(task)

    assert result["done"] is False


def test_create_invalid_categories(dao_instance):

    invalid_task = {
        "title": f"bad-{uuid.uuid4()}",
        "description": "invalid categories",
        "categories": "wrong_type"
    }

    result = dao_instance.create(invalid_task)

    assert result["_id"] is not None


def test_create_empty_description(dao_instance):

    task = {
        "title": f"empty-{uuid.uuid4()}",
        "description": ""
    }

    result = dao_instance.create(task)

    assert result["description"] == ""