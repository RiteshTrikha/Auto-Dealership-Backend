from flask import Blueprint

credit_bp = Blueprint('credit', __name__, template_folder='templates', static_folder='static')