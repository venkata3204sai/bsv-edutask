import pytest
from src.controllers.usercontroller import UserController
from unittest.mock import MagicMock

@pytest.fixture
def mock_setup():
    mock_dao = MagicMock()
    controller = UserController(mock_dao)
    return mock_dao, controller

@pytest.mark.unit
def test_single_user_returns_that_user(mock_setup):
    mock_dao, controller = mock_setup
    mock_dao.find.return_value = [{"email": "a@b.com"}]
    result = controller.get_user_by_email("a@b.com")
    assert result["email"] == "a@b.com"

@pytest.mark.unit
def test_multiple_users_returns_first(mock_setup):
    mock_dao, controller = mock_setup
    mock_dao.find.return_value = [
        {"email": "a@b.com", "name": "a1"},
        {"email": "a@b.com", "name": "a2"}]
    result = controller.get_user_by_email("a@b.com")
    assert result["email"] == "a@b.com" and result["name"] == "a1"

@pytest.mark.unit
def test_no_user_found_returns_none(mock_setup):
    mock_dao, controller = mock_setup
    mock_dao.find.return_value = []
    result = controller.get_user_by_email("a@b.com")
    assert result is None

@pytest.mark.unit
def test_invalid_email_raises_value_error(mock_setup):
    _, controller = mock_setup
    with pytest.raises(ValueError):
        controller.get_user_by_email("invalid email")

@pytest.mark.unit
def test_dao_exception(mock_setup):
    mock_dao, controller = mock_setup
    mock_dao.find.side_effect = Exception("Database Problem!!!")
    with pytest.raises(Exception):
        controller.get_user_by_email("a@b.com")