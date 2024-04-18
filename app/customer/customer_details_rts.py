from flask import jsonify, request, current_app, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import customer_bp
from flasgger import swag_from
from .models import Customer
from .services import CustomerServices
from app.exceptions import ExposedException

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

#get customer details
@customer_bp.route('/details', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get Customer Details',
    'tags': ['Customer'],
    'security': [{'BearerAuth': []}],
    'responses': {
        '200': {
            'description': 'Customer details',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'object',
                        'properties': {
                            'first_name': {'type': 'string'},
                            'last_name': {'type': 'string'},
                            'email': {'type': 'string'},
                            'birth_date': {'type': 'string'},
                            'drivers_license': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def get_customer_details():
    try:
        customer_id = get_jwt_identity().get('customer_id')
        customer_dict = CustomerServices().get_customer_details(customer_id)
        return standardize_response(data=customer_dict)
    except Exception as e:
        current_app.logger.exception(e)
        raise e