from flask import Blueprint

customer_bp = Blueprint('customer', __name__, template_folder='templates', static_folder='static')

from . import customer_negotiation_rts, customer_scheduling_rts, customer_purchasing_rts, customer_details_rts, customer_vehicle_rts, customer_financing_rts

