from flask import jsonify, request, g, current_app
from flasgger import swag_from
from . import auth_bp
from .models import *
from app import db
from .services import AuthService

# import Utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# login user
@auth_bp.route('/user/login', methods=['POST'])
@swag_from({
    'summary': 'Login User',
    'tags': ['Auth User'],
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
            'description': 'User logged in',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'object',
                        'properties': {
                            'access_token': {'type': 'string'},
                            'user_type': {'type': 'string'},
                            'user_id': {'type': 'integer'},
                            'role': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def login_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        access_token_dict = AuthService().login_user(email=email, password=password)
        return standardize_response(data=access_token_dict)
    except Exception as e:
        raise e