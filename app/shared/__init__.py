from flask import Blueprint

shared_bp = Blueprint('shared', __name__, template_folder='templates', static_folder='static')

from . import routes  # Import routes to ensure they're registered with the blueprint
