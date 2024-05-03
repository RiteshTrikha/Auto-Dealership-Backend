from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Customer, CreditReport, CreditReport
import requests
from . import credit_bp
from flasgger import swag_from

@credit_bp.route('/customer/credit-score', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Request customer credit score',
    'description': 'Post a customer\'s details and retrieve their credit score from an external service.',
    'tags': ['Credit Score'],
    'security': [{'jwt': []}],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'first_name': {'type': 'string', 'example': 'John'},
                        'last_name': {'type': 'string', 'example': 'Doe'},
                        'ssn': {'type': 'string', 'example': '123-45-6789'},
                        'birth_date': {'type': 'string', 'example': '1980-01-01'},
                        'address': {'type': 'string', 'example': '123 Elm St'}
                    },
                    'required': ['first_name', 'last_name', 'ssn', 'birth_date', 'address']
                }
            }
        }
    }
})
def request_credit_score():
    user_id = get_jwt_identity()
    data = request.get_json()
    customer = Customer.query.filter_by(ssn=data['ssn']).first()
    credit_report = CreditReport.query.filter_by(customer_id=customer.id).first()


    if customer is None:
        try:
            credit_score_api_url = 'http://127.0.0.1:8080/customer/credit-score'
            response = requests.post(credit_score_api_url, json=data)
            if response.status_code == 200:
                credit_data = response.json()
                new_credit_report = CreditReport(
                    customer_id=customer.id,
                    score=credit_data['credit_score'],
                    apy=credit_data['apy']  # Assuming 'apy' is part of the response
                )
                db.session.add(new_credit_report)
                db.session.commit()
                return jsonify(credit_data), 200
            else:
                return jsonify({'error': 'Failed to retrieve credit score'}), response.status_code
        except requests.RequestException as e:
            current_app.logger.error(f"Request failed: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    else:
        # Assuming credit score is already saved and linked with the customer
        credit_report = CreditReport.query.filter_by(customer_id=customer.id).first()
        return jsonify({
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'ssn': customer.ssn,
            'credit_score': credit_report.score,
            'apy': credit_report.apy
        }), 200
