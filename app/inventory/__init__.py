from flask import Blueprint

inventory_bp = Blueprint('inventory', __name__, template_folder='templates', static_folder='static', url_prefix='/inventory')

from . import inventory_vehicle_rts, inventory_service_rts

