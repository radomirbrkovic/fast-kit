from fastapi import HTTPException
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, UTC, timedelta

from app.services.admin.user_token_service import UserTokenService
from app.schemas.admin.user_tokens import UserTokenCreate
from app.models.enums import UserTokenType

TOKEN = "token123"

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return UserTokenService(repo=mock_repo)

def test_create_user_token(service, mock_repo):
    data = UserTokenCreate(user_id=1, type=UserTokenType.RESET_PASSWORD)
    mock_repo.create.return_value = {"id": 1, "user_id": 1, "token": TOKEN, "type": UserTokenType.RESET_PASSWORD}

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

def test_get_reset_password_token_success(service, mock_repo):
    token = MagicMock()
    token.expires_at = datetime.now(UTC) + timedelta(hours=1)
    mock_repo.findByTokenAndType.return_value = token

    result = service.getResetPasswordToken(TOKEN)

    mock_repo.findByTokenAndType.assert_called_once_with(TOKEN, UserTokenType.RESET_PASSWORD)
    assert result == token

def test_get_reset_password_not_found(service, mock_repo):
    mock_repo.findByTokenAndType.return_value = None

    with pytest.raises(HTTPException) as exc:
        service.getResetPasswordToken("invalid")

    assert exc.value.status_code == 404
    assert "doesn't exists" in exc.value.detail

def test_get_reset_password_token_expired(service, mock_repo):
    expired_token = MagicMock()
    expired_token.expires_at = datetime.now(UTC) - timedelta(hours=1)
    mock_repo.findByTokenAndType.return_value = expired_token

    with pytest.raises(HTTPException) as exc:
        service.getResetPasswordToken("expired")

    assert exc.value.status_code == 404
    assert "expired" in exc.value.detail

def test_delete_user_token(service, mock_repo):
    mock_repo.delete.return_value = True
    result = service.delete(1)

    mock_repo.delete.assert_called_once_with(1)
    assert result is True
