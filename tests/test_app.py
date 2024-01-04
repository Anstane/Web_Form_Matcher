import pytest

from app.app import application


@pytest.fixture
def client():
    """Fixture with the creation of a test client."""

    with application.test_client() as client:
        yield client


class TestApp:


    def test_endpoint(self, client):
        """Checking the endpoint'/get_form'."""

        response = client.post('/get_form', json={})
        assert response.status_code == 200, f'The POST-request was not processed. Status code: {response.status_code}.'

        response = client.get('/get_form')
        assert response.status_code == 405, f'The GET-request does not return code 405. Status code: {response.status_code}.'


    def test_return_name_of_templates_first(self, client):
        """We check that the template name MyForm is returned."""

        expected_answer = "MyForm"

        response = client.post('/get_form', json={
            "f_name_1": "test@test.ru",
            "f_name_2": "+79101112233"
        })

        response_data = response.get_data(as_text=True)

        assert response.status_code == 200, f"No response was received. Status code: {response.status_code}."
        assert response_data == expected_answer, f"Expected response {expected_answer}, received {response_data}."


    def test_return_name_of_templates_second(self, client):
        """We check that the name of the Order Form template is returned."""

        expected_answer = "Order Form"

        response = client.post('/get_form', json={
            "f_name_1": "example_text",
            "f_name_2": "17.11.2023"
        })

        response_data = response.get_data(as_text=True)

        assert response.status_code == 200, f"No response was received. Status code: {response.status_code}."
        assert response_data == expected_answer, f"Expected response {expected_answer}, received {response_data}."


    def test_correctness_JSON(self, client):
        """We check that JSON is received correctly."""

        response = client.post('/get_form', json={})
        assert response.json == {}, f'The returned JSON is incorrect. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "random_text"
        })
        assert response.json == {"f_name": "text"}, f'The returned JSON is incorrect. JSON: {response.json}.'


    def test_validation_typing_email(self, client):
        """We check the email validation and typing."""

        response = client.post('/get_form', json={
            "f_name": "test@test.ru"
        })
        assert response.json == {"f_name": "email"}, f'Email validation/typing error. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "testtest.ru"
        })
        assert response.json == {"f_name": "text"}, f'The @ symbol is missing in email. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "test@testru"
        })
        assert response.json == {"f_name": "text"}, f'Error in email domain. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "@."
        })
        assert response.json == {"f_name": "text"}, f'The email was not completely recorded. JSON: {response.json}.'


    def test_validation_typing_phone(self, client):
        """We check the validation and typing of the phone number."""

        response = client.post('/get_form', json={
            "f_name": "+79101112233"
        })
        assert response.json == {"f_name": "phone"}, f'Phone number validation/typing error. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "+19101112233"
        })
        assert response.json == {"f_name": "text"}, f'The number does not start at +7. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "+7"
        })
        assert response.json == {"f_name": "text"}, f'There are not enough numbers in the number. JSON: {response.json}.'


    def test_validation_typing_date(self, client):
        """We check the date validation and typing."""
    
        response = client.post('/get_form', json={
            "f_name": "17.11.2023"
        })
        assert response.json == {"f_name": "date"}, f'Date format error DD.MM.YYYY. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "2023-11-17"
        })
        assert response.json == {"f_name": "date"}, f'YYYY-MM-DD date format error. JSON: {response.json}.'

        response = client.post('/get_form', json={
            "f_name": "20231117"
        })
        assert response.json == {"f_name": "text"}, f'Date error. JSON: {response.json}.'
