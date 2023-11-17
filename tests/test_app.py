import pytest

from app.app import application


@pytest.fixture
def client():
    """Фикстура с созданием тестового клиента."""

    with application.test_client() as client:
        yield client


class TestSomething:

    def test_this(self, client):
        """Проверяем существование эндпоинта '/get_form'."""

        response = client.post('/get_form', json={})
        assert response.status_code == 200
