from flask import Blueprint

contracts_bp = Blueprint('contracts', __name__, template_folder='templates', static_folder='static')
