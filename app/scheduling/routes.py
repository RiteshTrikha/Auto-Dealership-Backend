from flask import jsonify, request
from . import scheduling_bp
from .models import *
from app import db

@scheduling_bp.route('/api/scheduling/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from scheduling_bp!'})