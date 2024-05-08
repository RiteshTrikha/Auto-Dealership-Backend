from flask import jsonify, request, current_app, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import customer_bp
from flasgger import swag_from

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# get customer finances
@customer_bp.route('/finances', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get Customer Finances',
    'tags': ['Customer Finances'],
    'security': [{'BearerAuth': []}],
    'responses': {
        '200': {
            'description': 'Customer finances',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'object',
                        'properties': {
                            'finances': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'finance_id': {'type': 'integer'},
                                        'purchase_id': {'type': 'integer'},
                                        'start_date': {'type': 'string'},
                                        'end_date': {'type': 'string'},
                                        'loan_amount': {'type': 'number'},
                                        'down_payment': {'type': 'number'},
                                        'total_loan_amount': {'type': 'number'},
                                        'monthly_payment': {'type': 'number'},
                                        'apr': {'type': 'number'},
                                        'term': {'type': 'integer'},
                                        'paid': {'type': 'boolean'},
                                        'finance_status': {'type': 'string'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_customer_finances():
    try:
        customer_id = get_jwt_identity().get('customer_id')
        finances_dict = g.purchasing_service.get_customer_finances(customer_id)
        return standardize_response(data=finances_dict)
    except Exception as e:
        current_app.logger.exception(e)
        raise e
    
# get customer finance by finance_id
@customer_bp.route('/finances/<int:finance_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get Finance details',
    'tags': ['Customer Finances'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'finance_id',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': 'Customer finance',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'object',
                        'properties': {
                            'finance': {
                                'type': 'object',
                                'properties': {
                                    'finance_id': {'type': 'integer'},
                                    'purchase_id': {'type': 'integer'},
                                    'start_date': {'type': 'string'},
                                    'end_date': {'type': 'string'},
                                    'loan_amount': {'type': 'number'},
                                    'down_payment': {'type': 'number'},
                                    'total_loan_amount': {'type': 'number'},
                                    'monthly_payment': {'type': 'number'},
                                    'apr': {'type': 'number'},
                                    'term': {'type': 'integer'},
                                    'paid': {'type': 'boolean'},
                                    'finance_status': {'type': 'string'}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_customer_finance_by_finance_id(finance_id):
    try:
        finance_dict = g.purchasing_service.get_finance_details(finance_id)
        return standardize_response(data=finance_dict)
    except Exception as e:
        current_app.logger.exception(e)
        raise e