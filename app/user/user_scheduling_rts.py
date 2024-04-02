from flask import jsonify, request, current_app, g
from . import user_bp
from app.negotiation.models import Negotiation, Offer
from app.inventory.models import Vehical
from app.exceptions import ExposedException

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response