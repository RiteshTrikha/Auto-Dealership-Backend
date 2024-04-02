from flask import jsonify, request
from . import customer_bp
from app import g
from .models import Customer
from app.exceptions import ExposedException

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response