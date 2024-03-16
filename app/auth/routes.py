from flask import jsonify, request
from . import auth_bp
from .models import *
from app import db

@auth_bp.route('/api/auth/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from auth_bp!'})