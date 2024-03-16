from flask import jsonify, request
from . import negotiation_bp
from .models import *
from app import db

@negotiation_bp.route('/api/negotiation/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from negotiation_bp!'})