from flask import Blueprint

user_bp = Blueprint('user', __name__, template_folder='templates', static_folder='static', url_prefix='/user')

from . import user_negotiation_rts, user_scheduling_rts, user_inventory_rts, user_purchasing_rts, user_management_rts