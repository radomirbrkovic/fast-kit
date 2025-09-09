import pytest
from unittest.mock import MagicMock
from services.admin.page_service import PageService
from schemas.admin.pages import PageCreate, PageUpdate
from models.page import Page


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo):
    return PageService(repo=mock_repo)

def _get_page(id: int =1, title: str = "Title", content: str = "Content", slug: str = "title"):
    return Page(id=id, title=title, content=content, slug=slug)

def test_create_page_generates_slug_and_saves(service, mock_repo):
    page_data  = PageCreate(title="Title", content="Content")
    page = _get_page()
    mock_repo.is_slug_exists.return_value = False
    mock_repo.create.return_value = page

    result = service.create(page_data)
    assert page_data.slug == "title"
    mock_repo.is_slug_exists.assert_called_once_with("title")
    mock_repo.create.assert_called_once_with(page_data)
    assert result == page