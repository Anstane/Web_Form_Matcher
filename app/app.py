import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from tinydb import TinyDB

from .validation import get_template_type


application = Flask(__name__)
db = TinyDB(
    os.path.abspath(
        f"{os.path.dirname(__file__)}/templates/templates.json"
    )
)

log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
log_handler = RotatingFileHandler('file_log.log', maxBytes=100000, backupCount=1)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)


def find_matching_template(request_data):
    """Function for searching suitable templates inside the database."""

    templates = db.all()

    for template in templates:
        template_values = set(template.values()) - {template['name']} # Remove duplicates and the name field.
        request_values = set(request_data.values()) # We collect fields from request into set.

        if template_values == request_values: # Compare templates from the database and request.
            return template['name']
    
    return None


@application.route('/get_form', methods=['POST'])
def get_form():
    """Basic application logic."""

    data = request.json
    validated_data = get_template_type(data)
    template_name = find_matching_template(validated_data)

    try:
        if template_name:
            logger.info(f"Template found: {template_name}")
            return template_name, 200
        else:
            logger.info(f"Template not found <(_ _)>. Type of fields: "
                        f"{', '.join(type for type in validated_data.values())}")
            return validated_data, 200

    except Exception as error:
        logger.error(f"Error: {error}")
        return error, 500


if __name__ == '__main__':
    application.run(debug=True)
