import re
from datetime import datetime


def validate_email(email: str) -> bool:
    """Простая валидация email с использованием регулярного выражения."""

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    return re.match(email_regex, email) is not None


def validate_phone(phone: str) -> bool:
    """Валидация номера телефона в формате +7XXXXXXXXXX."""

    phone_regex = r'^\+7\d{10}$'

    return re.match(phone_regex, phone) is not None


def validate_date(date: str) -> bool:
    """Валидация даты в форматах DD.MM.YYYY или YYYY-MM-DD."""

    date_formats = ['%d.%m.%Y', '%Y-%m-%d']

    for date_format in date_formats:

        try: # Если будет ValueError - функция не упадёт и в итоге вернёт False.
            datetime.strptime(date, date_format)
            return True

        except ValueError:
            pass

    return False


def get_template_type(data):
    """
    Общий валидатор принимающий данные и отдающий тип поля.
    """

    types = {} # Создаём новый словарь с типами данных.

    for field_name, value in data.items():
        if validate_email(value):
            types[field_name] = "email"

        elif validate_phone(value):
            types[field_name] = "phone"

        elif validate_date(value):
            types[field_name] = "date"

        else:
            types[field_name] = "text"

    return types
