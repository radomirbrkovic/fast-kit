import pytest
from unittest.mock import MagicMock
from fastapi import Request
from passlib.context import CryptContext

from services.auth_service import AuthService
from models.user import Users
from models.enums import UserRole


@pytest.fixture
def auth_service():
    service = AuthService()
    service.db = MagicMock()
    service.model = MagicMock()
    return service

def test_authenticate_user_not_found(auth_service):
    auth_service.model.filter.return_value.first.return_value = None
    result = auth_service.authenticate("unknown@example.com", "password", UserRole.ADMIN)
    assert result is None

def test_authenticate_wrong_password(auth_service, monkeypatch):
    user = Users(id=1, email="test@example.com", hashed_password="hashed123", role=UserRole.ADMIN)
    auth_service.model.filter.return_value.first.return_value = user

    monkeypatch.setattr(auth_service, "verify_password", lambda p, h: False)

    result = auth_service.authenticate("test@example.com", "badpassword", UserRole.ADMIN)
    assert result is None