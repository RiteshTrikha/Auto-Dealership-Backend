from flask import jsonify, request
from . import customer_bp
from app import g
from .models import Customer