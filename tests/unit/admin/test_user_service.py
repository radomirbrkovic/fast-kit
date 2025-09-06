import pytest
from unittest.mock import MagicMock, patch, AsyncMock
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

@patch("services.admin.user_service.asyncio.create_task")
@patch("services.admin.user_service.UserTokenService")
@patch("services.admin.user_service.send", new_callable=AsyncMock)
@patch("services.admin.user_service.templates")
def test_create_user(mock_templates, mock_send, mock_token_service, mock_create_task, service, mock_repo):
    mock_create_task.return_value = None
    # Mock input
    obj_in = UserCreate(
        email="new@example.com",
        first_name="John",
        last_name="Doe",
        role=UserRole.USER,
        hashed_password=None
    )

    # Mock repo create
    user = MagicMock()
    user.id = 1
    user.email = "new@example.com"
    mock_repo.create.return_value = user

    # Mock token service
    mock_token = MagicMock()
    mock_token.token = "reset123"
    mock_token_service.return_value.create.return_value = mock_token

    # Mock template
    mock_template = MagicMock()
    mock_template.render.return_value = "html-content"
    mock_templates.env.get_template.return_value = mock_template

    # Mock request with url_for
    request = MagicMock(spec=Request)
    request.url_for.return_value = "http://test/reset"
    service.set_request(request)

    result = service.create(obj_in)

    assert result == user
    mock_repo.create.assert_called_once()
    mock_token_service.return_value.create.assert_called_once()
    mock_send.assert_called_once_with(
        "new@example.com", "Welcome", "html-content"
    )

def test_update_user(service, mock_repo):
    user_id = 1
    data = UserUpdate(
        first_name= "John",
        last_name= "Doe",
        email = "john.doe@example.com",
        role= UserRole.USER
    )

    user = MagicMock()
    user.id = user_id
    user.email = data.email
    user.first_name = data.first_name
    user.last_name =data.last_name
    user.role = data.role

    mock_repo.update.return_value = user

    result = service.update(user_id, data)

    mock_repo.update.assert_called_once_with(user_id, data)
    assert result.email == data.email
    assert result.first_name == data.first_name
    assert result.role == data.role
