import pytest

from app.app import application


@pytest.fixture
def client():
    """Фикстура с созданием тестового клиента."""

    with application.test_client() as client:
        yield client


class TestApp:


    def test_endpoint(self, client):
        """Проверяем эндпоинт '/get_form'."""

        response = client.post('/get_form', json={})
        assert response.status_code == 200, f'POST-запрос не обработан. Статус код: {response.status_code}.'

        response = client.get('/get_form')
        assert response.status_code == 405, f'GET-запрос не возвращает код 405. Статус код: {response.status_code}.'


    def test_return_name_of_templates_first(self, client):
        """Проверяем, что возвращается имя шаблона MyForm."""

        expected_answer = "MyForm"

        response = client.post('/get_form', json={
            "f_name_1": "test@test.ru",
            "f_name_2": "+79101112233"
        })

        response_data = response.get_data(as_text=True)

        assert response.status_code == 200, f"Ответ не был получен. Статус код: {response.status_code}."
        assert response_data == expected_answer, f"Ожидаемый ответ '{expected_answer}', получен '{response_data}'."


    def test_return_name_of_templates_second(self, client):
        """Проверяем, что возвращается имя шаблона Order Form."""

        expected_answer = "Order Form"

        response = client.post('/get_form', json={
            "f_name_1": "example_text",
            "f_name_2": "17.11.2023"
        })

        response_data = response.get_data(as_text=True)

        assert response.status_code == 200, f"Ответ не был получен. Статус код: {response.status_code}."
        assert response_data == expected_answer, f"Ожидаемый ответ '{expected_answer}', получен '{response_data}'."


    def test_correctness_JSON(self, client):
        """Проверяем, что JSON корректно принимается."""

        response = client.post('/get_form', json={})
        assert response.json == {}, f'Возвращаемый JSON некорректен. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "random_text"
        })
        assert response.json == {"f_name": "text"}, f'Возвращаемый JSON некорректен. JSON: {response.json}.'


    def test_validation_typing_email(self, client):
        """Проверяем валидацию и типизацию эл.почты."""

        response = client.post('/get_form', json={
            "f_name": "test@test.ru"
        })
        assert response.json == {"f_name": "email"}, f'Ошибка валидации/типизации эл.почты. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "testtest.ru"
        })
        assert response.json == {"f_name": "text"}, f'Символ @ отсутствует в эл.почте. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "test@testru"
        })
        assert response.json == {"f_name": "text"}, f'Ошибка в домене эл.почты. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "@."
        })
        assert response.json == {"f_name": "text"}, f'Эл.почта записана не полностью. JSON: {response.json}.'


    def test_validation_typing_phone(self, client):
        """Проверяем валидацию и типизацию номера телефона."""

        response = client.post('/get_form', json={
            "f_name": "+79101112233"
        })
        assert response.json == {"f_name": "phone"}, f'Ошибка валидации/типизации номера телефона. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "+19101112233"
        })
        assert response.json == {"f_name": "text"}, f'Номер начинается не на +7. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "+7"
        })
        assert response.json == {"f_name": "text"}, f'В номере недостаточно цифр. JSON: {response.json}.'


    def test_validation_typing_date(self, client):
        """Проверяем валидацию и типизацию даты."""
    
        response = client.post('/get_form', json={
            "f_name": "17.11.2023"
        })
        assert response.json == {"f_name": "date"}, f'Ошибка формата даты DD.MM.YYYY. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "2023-11-17"
        })
        assert response.json == {"f_name": "date"}, f'Ошибка формата даты YYYY-MM-DD. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "20231117"
        })
        assert response.json == {"f_name": "text"}, f'Ошибка даты. JSON: {response.json}.'
