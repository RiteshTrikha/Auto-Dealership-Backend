from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user.get('user_type') == 'user' and current_user.get('role') == 'admin':
            return fn(*args, **kwargs)
        else:
            return standardize_response(status='fail', message='Admin access required', code=403)
    return wrapper

def manager_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user.get('user_type') == 'user' and current_user.get('role') == 'manager' or current_user.get('role') == 'admin':
            return fn(*args, **kwargs)
        else:
            return standardize_response(status='fail', message='Manager access required', code=403)
    return wrapper

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user.get('user_type') == 'user':
            return fn(*args, **kwargs)
        else:
            return standardize_response(status='fail', message='User access required', code=403)
    return wrapper