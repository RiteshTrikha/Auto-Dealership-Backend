from flask import jsonify, request
from . import user_bp
from .models import *
from app import db

@user_bp.route('/api/user/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from user_bp!'})
