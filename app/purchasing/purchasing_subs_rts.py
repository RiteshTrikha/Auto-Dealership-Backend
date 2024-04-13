from flask import jsonify, request, current_app, g
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from . import purchasing_bp
from .services import LoanService
from app.utilities import Utilities

standardize_response = Utilities.standardize_response

@purchasing_bp.route('/loan/request', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Request Loan',
    'tags': ['Customer Loan'],
    'security': [{'jwt': []}],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'customer_id': {'type': 'integer'},
                        'vehicle_id': {'type': 'integer'},
                        'requested_loan_amount': {'type': 'number'}
                    },
                    'required': ['customer_id', 'vehicle_id', 'requested_loan_amount']
                }
            }
        }
    },
    'responses': {
        '201': {
            'description': 'Loan requested successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'request_id': {'type': 'integer'}
                }
            }
        }
    }
})
def request_loan():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        vehicle_id = data.get('vehicle_id')
        requested_loan_amount = data.get('requested_loan_amount')

        loan_service = LoanService()
        request_id = loan_service.request_loan(customer_id, vehicle_id, requested_loan_amount)

        return standardize_response(data={'request_id': request_id}, message='Loan requested successfully', code=201)
    except Exception as e:
        raise e

@purchasing_bp.route('/loan/requests/<int:customer_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get Loan Requests',
    'tags': ['Customer Loan'],
    'security': [{'jwt': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'customer_id',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the customer'
        }
    ],
    'responses': {
        '200': {
            'description': 'Loan requests retrieved successfully'
        }
    }
})
def get_loan_requests(customer_id):
    try:
        loan_service = LoanService()
        loan_requests = loan_service.get_loan_requests(customer_id)
        return standardize_response(data=loan_requests)
    except Exception as e:
        raise e

@purchasing_bp.route('/loan/payment', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Make Loan Payment',
    'tags': ['Customer Loan'],
    'security': [{'jwt': []}],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'customer_id': {'type': 'integer'},
                        'loan_request_id': {'type': 'integer'},
                        'amount_paid': {'type': 'number'}
                    },
                    'required': ['customer_id', 'loan_request_id', 'amount_paid']
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Payment made successfully'
        }
    }
})
def make_payment():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        loan_request_id = data.get('loan_request_id')
        amount_paid = data.get('amount_paid')

        loan_service = LoanService()
        loan_service.make_payment(customer_id, loan_request_id, amount_paid)

        return standardize_response(message='Payment made successfully')
    except Exception as e:
        raise e

@purchasing_bp.route('/loan/monthly-payments', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Generate Monthly Payments',
    'tags': ['Customer Loan'],
    'security': [{'jwt': []}],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'loan_request_id': {'type': 'integer'}
                    },
                    'required': ['loan_request_id']
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Monthly payments generated successfully'
        }
    }
})
def generate_monthly_payments():
    try:
        data = request.get_json()
        loan_request_id = data.get('loan_request_id')

        loan_service = LoanService()
        monthly_payments = loan_service.generate_monthly_payments(loan_request_id)

        return standardize_response(data=monthly_payments, message='Monthly payments generated successfully')
    except Exception as e:
        raise e
