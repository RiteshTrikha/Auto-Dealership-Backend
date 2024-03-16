from flask import jsonify, request
from . import shared_bp
from .models import *
from app import db

@shared_bp.route('/api/shared/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from shared_bp!'})

