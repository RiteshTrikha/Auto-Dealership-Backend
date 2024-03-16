from flask import jsonify, request
from . import purchasing_bp
from .models import *
from app import db

@purchasing_bp.route('/api/purchasing/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from purchasing_bp!'})