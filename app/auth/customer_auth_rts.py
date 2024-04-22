from flask import jsonify, request, g, current_app
from flasgger import swag_from
from . import auth_bp
from .models import *
from app import db
from .services import AuthService

# import Utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

@auth_bp.route('/customer/register', methods=['POST'])
@swag_from({
    'summary': 'Register Customer',
    'tags': ['Auth Customer'],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'first_name': {'type': 'string'},
                        'last_name': {'type': 'string'},
                        'email': {'type': 'string'},
                        'password': {'type': 'string'},
                        'birth_date': {'type': 'string'},
                        'drivers_license': {'type': 'string'}
                    }
                }
            }
        }
    },
    'responses': {
        '201': {
            'description': 'Customer registered',
            'schema': {
                'type': 'object',
                'properties': {
                    'customer_id': {'type': 'integer'}
                }
            }
        }
    }
})
def register_customer():
    try:
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        birth_date = data.get('birth_date')
        drivers_license = data.get('drivers_license')
        customer_id_dict = AuthService().register_customer(first_name=first_name, last_name=last_name, 
                                                      email=email, password=password, 
                                                      birth_date=birth_date, 
                                                      drivers_license=drivers_license)
        return standardize_response(data=customer_id_dict, code=201)
    except Exception as e:
        raise e
    
@auth_bp.route('/customer/login', methods=['POST'])
@swag_from({
    'summary': 'Login Customer',
    'tags': ['Auth Customer'],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'email': {'type': 'string'},
                        'password': {'type': 'string'}
                    }
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Customer logged in',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': 
                    {
                        'type': 'object',
                        'properties': {
                            'access_token': {'type': 'string'},
                            'user_type': {'type': 'string'},
                            'customer_id': {'type': 'integer'},
                            'first_name': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def login_customer():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        access_token_dict = AuthService().login_customer(email=email, password=password)
        return standardize_response(data=access_token_dict, code=200)
    except Exception as e:
        raise e
    
