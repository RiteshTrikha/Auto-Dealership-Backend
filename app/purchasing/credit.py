from flask import jsonify, request, current_app, g, request
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from . import purchasing_bp
from .services import LoanService
from app import db  # Import database context
from app.utilities import Utilities
from app.customer.models import Customer, CreditReport
import requests

standardize_response = Utilities.standardize_response

@purchasing_bp.route('/customer/credit-score', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Get and Save Customer Credit Score',
    'tags': ['Customer Credit'],
    'security': [{'jwt': []}],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'first_name': {'type': 'string'},
                        'last_name': {'type': 'string'},
                        'ssn': {'type': 'string'},
                        'birth_date': {'type': 'string'},
                        'address': {'type': 'string'}
                    },
                    'required': ['first_name', 'last_name', 'ssn', 'birth_date', 'address']
                }
            }
        }
    },
    'responses': {
        '201': {
            'description': 'Credit score saved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'credit_score': {'type': 'integer'}
                }
            }
        }
    }
})
def get_and_save_credit_score():
    try:
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']
        ssn = data['ssn']
        birth_date = data['birth_date']
        address = data['address']

        # Assuming you have a valid external service to fetch the credit score
        credit_score = request_credit_score(first_name, last_name, ssn, birth_date, address)

        # Check if customer exists or create new
        customer = Customer.query.filter_by(ssn=ssn).first()
        if not customer:
            customer = Customer(first_name=first_name, last_name=last_name, ssn=ssn, birth_date=birth_date)
            db.session.add(customer)
            db.session.commit()

        # Create or update the credit report
        credit_report = CreditReport.query.filter_by(customer_id=customer.id).first()
        if not credit_report:
            credit_report = CreditReport(customer_id=customer.id, score=credit_score)
        else:
            credit_report.score = credit_score

        db.session.add(credit_report)
        db.session.commit()

        return standardize_response(data={'credit_score': credit_score}, message='Credit score saved successfully', code=201)
    except Exception as e:
        current_app.logger.error(f"Error saving credit score: {str(e)}")
        return jsonify({"error": "An error occurred processing your request"}), 500

def request_credit_score(first_name, last_name, ssn, birth_date, address):
    credit_score_api_url = 'http://127.0.0.1:5000/customer/credit-score'  # Update with actual URL
    payload = {
        'first_name': first_name,
        'last_name': last_name,
        'ssn': ssn,
        'birth_date': birth_date,
        'address': address
    }
    response = requests.post(credit_score_api_url, json=payload)
    response_data = response.json()
    return response_data['credit_score']
