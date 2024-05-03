from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required
import requests
from app.customer.models import Customer, CreditReport
from . import credit_bp
from flasgger import swag_from

@credit_bp.route('/customer/credit-score', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Request customer credit score',
    'description': 'Post a customer\'s details including income and downpayment to retrieve their credit score from an external service.',
    'tags': ['Credit Score'],
    'security': [{'BearerAuth': []}],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'customer_id': {'type': 'integer', 'example': 1},  # This is an example of a field that may not be needed
                        'first_name': {'type': 'string', 'example': 'John'},
                        'last_name': {'type': 'string', 'example': 'Doe'},
                        'birth_date': {'type': 'string', 'example': '1980-01-01'},
                        'address': {'type': 'string', 'example': '123 Elm St'},
                        'annual_income': {'type': 'integer', 'example': 50000},
                        'downpayment': {'type': 'integer', 'example': 10000}
                    },
                    'required': ['first_name', 'last_name', 'ssn', 'birth_date', 'address', 'annual_income', 'downpayment']
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Credit score successfully retrieved',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'credit_score': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {'description': 'Bad request'},
        '500': {'description': 'Internal server error'}
    }
})
def request_credit_score():
    data = request.get_json()
    customer_id = data.get('customer_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    birth_date = data.get('birth_date')
    address = data.get('address')
    annual_income = data.get('annual_income')
    downpayment = data.get('downpayment')
    print("again",data)

    current_app.logger.debug(f"Received data: {data}")

    try:
        credit_score_api_url = 'http://127.0.0.1:8080/customers/credit-score'
        payload = {
            'first_name': first_name,
            'last_name': last_name,
            'birth_date': birth_date,
            'address': address,
            'annual_income': annual_income,
            'loan_amount': downpayment  # Ensure 'loan_amount' is correct key expected by your Flask-RestX API
            #monthly owed
        }
        response = requests.post(credit_score_api_url, json=payload)
        print("this is a responce",response.json()), "end of responce"

        # Parse the response and handle different cases
        if response.status_code == 200:
            return jsonify(response.json()), 200
        elif response.status_code == 201:
            return jsonify(response.json()), 201
        elif response.status_code == 400:
            current_app.logger.warning("Bad request made to credit score API.")
            return jsonify({'error': 'Bad request to credit score API', 'details': response.json()}), 400
        elif response.status_code == 500:
            current_app.logger.error("Server error in the credit score API.")
            return jsonify({'error': 'Server error in credit score API'}), 500
        else:
            current_app.logger.error(f"Unexpected status code {response.status_code}: {response.text}")
            return jsonify({'error': 'Unexpected error from credit score API'}), response.status_code
    except requests.RequestException as e:
        current_app.logger.error(f"Request failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'exception': str(e)}), 500