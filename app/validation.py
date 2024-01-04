import re
from datetime import datetime


def validate_email(email: str) -> bool:
    """Simple email validation using regular expression."""

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    return re.match(email_regex, email) is not None


def validate_phone(phone: str) -> bool:
    """Validation of the phone number in the format +7XXXXXXXXXX."""

    phone_regex = r'^\+7\d{10}$'

    return re.match(phone_regex, phone) is not None


def validate_date(date: str) -> bool:
    """Date validation in DD.MM.YYYY or YYYY-MM-DD formats."""

    date_formats = ['%d.%m.%Y', '%Y-%m-%d']

    for date_format in date_formats:

        try: # If there is a ValueError, the function will not fail and will eventually return False.
            datetime.strptime(date, date_format)
            return True

        except ValueError:
            pass

    return False


def get_template_type(data):
    """
    A general validator that receives data and outputs a field type.
    """

    types = {} # Create a new dictionary with data types.

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
