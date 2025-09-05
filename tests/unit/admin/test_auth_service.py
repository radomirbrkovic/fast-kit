import pytest
from unittest.mock import MagicMock
from fastapi import Request
from passlib.context import CryptContext

from services.auth_service import AuthService
from models.user import Users


@pytest.fixture
def auth_service():
    service = AuthService()
    service.db = MagicMock()
    service.model = MagicMock()
    return service

def test_authenticate_user_not_found(auth_service):
    auth_service.model.filter.return_value.first.return_value = None
    result = auth_service.authenticate("unknown@example.com", "password", "admin")
    assert result is None