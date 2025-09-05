import pytest
from unittest.mock import MagicMock, patch
from starlette.requests import Request

from models.user import Users
from services.admin.user_service import UserService
from schemas.admin.users import UserCreate, UserUpdate, UserOut
from schemas.admin.user_tokens import UserTokenCreate, UserTokenType
from models.enums import UserRole

@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo):
    return UserService(repo=mock_repo)

def _get_user():
    return  Users(
        id=1,
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        is_active=True,
        role=UserRole.ADMIN,  # or string if your enum uses str
        phone_number="123456"
    )

def test_get_users(service, mock_repo):
    mock_repo.get.return_value = [_get_user()]

    result = service.get()
    assert isinstance(result[0], UserOut)
    mock_repo.get.assert_called_once()