from flask import Blueprint

tests_bp = Blueprint('tests', __name__, template_folder='templates', static_folder='static', url_prefix='/tests')