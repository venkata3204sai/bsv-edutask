# coding=utf-8
import pytest
import pymongo
from unittest.mock import patch

from src.util.dao import DAO


# ---------------------------------------------------------------------------
# Validator schema (mirrors task.json exactly, passed as the MongoDB validator)
# ---------------------------------------------------------------------------
TASK_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "description"],
        "properties": {
            "title": {
                "bsonType": "string",
                "description": "the title of a task must be determined",
                "uniqueItems": True
            },
            "description": {
                "bsonType": "string",
                "description": "the description of a task must be determined"
            },
            "todos": {
                "bsonType": "array",
                "items": {"bsonType": "objectId"}
            }
        }
    }
}


# ---------------------------------------------------------------------------
# Fixture: real MongoDB, mocked getValidator, isolated test collection
# ---------------------------------------------------------------------------
@pytest.fixture
def dao_instance():
    """
    Provides a real DAO connected to a dedicated test collection.

    - getValidator is mocked so the fixture does not depend on the file system;
      the real validator schema is injected directly.
    - The collection is dropped after every test to guarantee isolation and
      to reset the uniqueItems constraint between runs.
    """
    with patch("src.util.dao.getValidator") as mock_get_validator:
        mock_get_validator.return_value = TASK_VALIDATOR
        dao = DAO("task_integration_test")
        yield dao
        dao.drop()


# ---------------------------------------------------------------------------
# TC1 – title present | description present | title is string | title is unique
# Expected: success – document inserted and returned
# ---------------------------------------------------------------------------
@pytest.mark.integration
def test_create_success(dao_instance):
    """All required fields present with correct bsonTypes → document created."""
    data = {"title": "Task One", "description": "A valid task"}
    result = dao_instance.create(data)

    assert result is not None
    assert result["title"] == "Task One"
    assert result["description"] == "A valid task"
    assert "_id" in result


# ---------------------------------------------------------------------------
# TC2 – title MISSING | description present | (type N/A) | (unique N/A)
# Expected: failure – WriteError raised because required field is absent
# ---------------------------------------------------------------------------
@pytest.mark.integration
def test_create_missing_title(dao_instance):
    """Missing required field 'title' → WriteError raised."""
    data = {"description": "No title provided"}

    with pytest.raises(pymongo.errors.WriteError):
        dao_instance.create(data)


# ---------------------------------------------------------------------------
# TC3 – title present | description MISSING | title is string | (unique N/A)
# Expected: failure – WriteError raised because required field is absent
# ---------------------------------------------------------------------------
@pytest.mark.integration
def test_create_missing_description(dao_instance):
    """Missing required field 'description' → WriteError raised."""
    data = {"title": "Task Without Description"}

    with pytest.raises(pymongo.errors.WriteError):
        dao_instance.create(data)


# ---------------------------------------------------------------------------
# TC4 – title present | description present | title NOT a string (int) | (unique N/A)
# Expected: failure – WriteError raised because bsonType constraint violated
# ---------------------------------------------------------------------------
@pytest.mark.integration
def test_create_invalid_title_type(dao_instance):
    """'title' with wrong bsonType (integer) → WriteError raised."""
    data = {"title": 42, "description": "Title is an integer"}

    with pytest.raises(pymongo.errors.WriteError):
        dao_instance.create(data)


# ---------------------------------------------------------------------------
# TC5 – title present | description present | description NOT a string (int) | title is unique
# Expected: failure – WriteError raised because bsonType constraint on description violated
# ---------------------------------------------------------------------------
@pytest.mark.integration
def test_create_invalid_description_type(dao_instance):
    """'description' with wrong bsonType (integer) → WriteError raised."""
    data = {"title": "Task Five", "description": 999}

    with pytest.raises(pymongo.errors.WriteError):
        dao_instance.create(data)


# ---------------------------------------------------------------------------
# TC6 – title present | description present | title is string | title is unique
#        (optional field included)
# Expected: success – optional fields do not prevent insertion
# ---------------------------------------------------------------------------
@pytest.mark.integration
def test_create_with_optional_field(dao_instance):
    """All required fields present plus an optional field → document created."""
    data = {
        "title": "Task With Optional",
        "description": "Has an optional field",
        "todos": []          # optional array field
    }
    result = dao_instance.create(data)

    assert result is not None
    assert result["title"] == "Task With Optional"