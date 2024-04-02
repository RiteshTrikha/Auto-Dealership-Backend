from flask import Blueprint

customer_bp = Blueprint('customer', __name__, template_folder='templates', static_folder='static', url_prefix='/customer')

from . import customer_negotiation_rts, customer_scheduling_rts