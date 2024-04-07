from flask import jsonify, request, g
from . import auth_bp
from .models import *
from app import db
from .services import AuthService

# import Utilities
from utilities import Utilities
standard_response = Utilities.standard_response

@auth_bp.route('/customer/register', methods=['POST'])
def register_customer():
    try:
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        birth_date = data.get('birth_date')
        drivers_license = data.get('drivers_license')
        customer_id = AuthService().register_customer(first_name=first_name, last_name=last_name, 
                                                      email=email, password=password, 
                                                      birth_date=birth_date, 
                                                      drivers_license=drivers_license)
        return standard_response(data=customer_id, status_code=201)
    except Exception as e:
        raise e
    
@auth_bp.route('/customer/login', methods=['POST'])
def login_customer():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        AuthService().login_customer(email=email, password=password)
        return standard_response(data='Success', status_code=200)
    except Exception as e:
        raise e
        
@auth_bp.route('/customer/logout', methods=['POST'])
def logout_customer():
    try:
        AuthService().logout_customer()
        return standard_response(data='Success', status_code=200)
    except Exception as e:
        raise e