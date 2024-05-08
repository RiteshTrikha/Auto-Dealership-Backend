from flask import Blueprint

negotiation_bp = Blueprint('negotiation', __name__, template_folder='templates', static_folder='static')
