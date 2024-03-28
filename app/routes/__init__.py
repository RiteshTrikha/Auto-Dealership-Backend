from flask import Blueprint

routes_bp = Blueprint('routes', __name__, template_folder='templates', static_folder='static')

from . import inventory_routes, negotiation_routes
