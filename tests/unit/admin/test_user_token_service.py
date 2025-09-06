import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, UTC

from services.admin.user_token_service import UserTokenService
from schemas.admin.user_tokens import UserTokenCreate
from models.enums import UserTokenType

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return UserTokenService(repo=mock_repo)

def test_create_user_token(service, mock_repo):
    data = UserTokenCreate(user_id=1, type=UserTokenType.RESET_PASSWORD)
    mock_repo.create.return_value = {"id": 1, "user_id": 1, "token": "token123", "type": UserTokenType.RESET_PASSWORD}

    with patch("services.admin.user_token_service.secrets.token_urlsafe", return_value="securetoken"):
        result = service.create(data)

    mock_repo.create.assert_called_once()
    args, _ = mock_repo.create.call_args
    created_data = args[0]

    assert created_data["user_id"] == 1
    assert created_data["token"] == "securetoken"
    assert created_data["type"] == UserTokenType.RESET_PASSWORD
    assert created_data["expires_at"] > datetime.now(UTC)
    assert result == mock_repo.create.return_value