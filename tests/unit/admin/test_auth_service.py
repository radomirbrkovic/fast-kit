import pytest
from unittest.mock import MagicMock, patch
from fastapi import Request

from services.auth_service import AuthService
from models.user import Users
from models.enums import UserRole


@pytest.fixture
def auth_service():
    service = AuthService()
    service.db = MagicMock()
    service.model = MagicMock()
    return service

def _get_user(id: int = 1, email: str = "test@example.com", hashed_password: str ="hashed123", role: str =UserRole.ADMIN):
    return Users(id=id, email=email, hashed_password=hashed_password, role=role)

def test_authenticate_user_not_found(auth_service):
    auth_service.model.filter.return_value.first.return_value = None
    result = auth_service.authenticate("unknown@example.com", "password", UserRole.ADMIN)
    assert result is None

def test_authenticate_wrong_password(auth_service, monkeypatch):
    user = _get_user()
    auth_service.model.filter.return_value.first.return_value = user

    monkeypatch.setattr(auth_service, "verify_password", lambda p, h: False)

    result = auth_service.authenticate("test@example.com", "badpassword", UserRole.ADMIN)
    assert result is None

def test_authenticate_wrong_role(auth_service, monkeypatch):
    user = _get_user(role=UserRole.USER)
    auth_service.model.filter.return_value.first.return_value = user

    monkeypatch.setattr(auth_service, "verify_password", lambda p, h: True)

    result = auth_service.authenticate("test@example.com", "password", UserRole.ADMIN)
    assert result is None

def test_authenticate_success(auth_service, monkeypatch):
    user = _get_user()
    auth_service.model.filter.return_value.first.return_value = user
    monkeypatch.setattr(auth_service, "verify_password", lambda p, h: True)

    result = auth_service.authenticate("test@example.com", "password", UserRole.ADMIN)

    assert result == user
    auth_service.model.filter.assert_called_once()

def test_user_with_valid_session(auth_service):
    user = _get_user(role=UserRole.SUPER_ADMIN)
    auth_service.model.filter.return_value.first.return_value = user

    request = MagicMock(spec=Request)
    request.session = {"auth_id": 1}

    result = auth_service.user(request)
    assert result == user

def test_user_with_invalid_session(auth_service):
    auth_service.model.filter.return_value.first.return_value = None
    request = MagicMock(spec=Request)
    request.session = {'auth_id': 99}

    result = auth_service.user(request=request)
    assert result is None

def test_user_without_session(auth_service):
    request = MagicMock(spec=Request)
    request.session = {}

    assert auth_service.user(request) is None

def test_reset_password_user_not_found(auth_service):
    auth_service.model.filter.return_value.first.return_value = None
    request = MagicMock(spec=Request)

    result = auth_service.reset_password("notfound@example.com", request)

    assert result is False
    auth_service.model.filter.assert_called_once()

@patch("services.auth_service.UserTokenService")
def test_reset_password_success(mock_user_token_service_cls, auth_service):
    user = _get_user()
    auth_service.model.filter.return_value.first.return_value = user
    request = MagicMock(spec=Request)

    mock_user_token_service = MagicMock()
    mock_user_token_service.create.return_value = MagicMock(id=123)
    mock_user_token_service_cls.return_value = mock_user_token_service

    auth_service._send_reset_password_email = MagicMock()

    result = auth_service.reset_password("test@example.com", request)

    assert result is True
    mock_user_token_service_cls.assert_called_once()  # service created
    mock_user_token_service.create.assert_called_once()
    auth_service._send_reset_password_email.assert_called_once_with(
        user, mock_user_token_service.create.return_value, request
    )
