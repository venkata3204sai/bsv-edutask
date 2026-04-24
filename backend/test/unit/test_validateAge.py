import pytest
from src.util.helpers import ValidationHelper
from unittest.mock import MagicMock

@pytest.fixture
def mock_setup():
    mock_usercontroller = MagicMock()
    helper = ValidationHelper(mock_usercontroller)
    return helper, mock_usercontroller

@pytest.mark.unit
@pytest.mark.parametrize("age_input, expected_values",[
    (-1, "invalid"),
    (0, "underaged"),
    (1, "underaged"),
    (17, "underaged"),
    (18, "underaged"),
    (19, "valid"),
    (119, "valid"),
    (120, "valid"),
    (121, "invalid")
])
def test_validateAge(mock_setup, age_input, expected_values):
    helper, mock_usercontroller = mock_setup
    mock_usercontroller.get.return_value = {"age": age_input}
    result = helper.validateAge("user123")
    assert result == expected_values

