import pytest
from unittest.mock import MagicMock
from app.services.admin.page_service import PageService
from app.schemas.admin.pages import PageCreate, PageUpdate
from app.models.page import Page


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

def test_update_page_regenerates_slug(service, mock_repo):
    page_data =  PageUpdate(title="Title Updated", content="Content Updated")
    page = _get_page(title="Title Updated", content="Content Updated", slug="title-updated")
    mock_repo.is_slug_exists.return_value = False
    mock_repo.update.return_value = page

    result = service.update(1, page_data)

    assert page_data.slug == "title-updated"
    mock_repo.is_slug_exists.assert_called_once_with("title-updated")
    mock_repo.update.assert_called_once_with(1, page_data)
    assert result == page

def test_get_slug_handles_duplicates(service, mock_repo):
    mock_repo.is_slug_exists.side_effect = [True, True, False]
    slug = service._get_slug("My Page")

    assert slug == "my-page-2"

def test_find_page(service, mock_repo):
    page = _get_page()
    mock_repo.find.return_value = page

    result = service.find(1)

    mock_repo.find.assert_called_once_with(1)
    assert result == page

def test_get_pages(service, mock_repo):
    pages = [_get_page()]
    mock_repo.get.return_value = pages

    result = service.get()

    mock_repo.get.assert_called_once_with(None)
    assert result == pages

def test_delete_page(service, mock_repo):
    mock_repo.delete.return_value = None

    result = service.delete(1)

    mock_repo.delete.assert_called_once_with(1)
    assert result is None
