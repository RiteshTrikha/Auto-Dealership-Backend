from flask import Blueprint

credit_bp = Blueprint('credit', __name__, template_folder='templates', static_folder='static')

from . import credit_routes  # Import routes to ensure they're registered with the blueprint