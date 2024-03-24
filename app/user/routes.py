from flask import jsonify, request
from . import user_bp
from .models import *
from app import db

@user_bp.route('/api/user/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from user_bp!'})

@user_bp.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.query(User).filter(User.user_id == user_id).first()
    if user:
        return jsonify(user.serialize())
    else:
        return jsonify({'message': 'User not found'}), 404
