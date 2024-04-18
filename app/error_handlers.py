from flask import jsonify, current_app
from app.exceptions import ExposedException

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

def handle_exception(e):
    if isinstance(e, ExposedException):
        return standardize_response(status='error', message=e.message, code=e.code)
    current_app.logger.exception(e)
    return standardize_response(status='error', message='An error occurred: please try again later.', code=500)

def register_error_handlers(app):
    app.register_error_handler(Exception, handle_exception)
