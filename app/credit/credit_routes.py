from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required
import requests
#from app.utilities import Utilities
from . import credit_bp
from flasgger import swag_from


#standardize_response = Utilities.standardize_response

@credit_bp.route('/customer/credit-score', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Request customer credit score',
    'description': 'Post a customer\'s details and retrieve their credit score from an external service.',
    'tags': ['Credit Score'],
    'security': [{'BearerAuth': []}],
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
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    ssn = data.get('ssn')
    birth_date = data.get('birth_date')
    address = data.get('address')

    current_app.logger.debug(f"Received data: {data}")

    try:
        credit_score_api_url = 'http://127.0.0.1:8080/customers/credit-score'
        payload = {
            'first_name': first_name, 'last_name': last_name,
            'ssn': ssn, 'birth_date': birth_date, 'address': address
        }
        response = requests.post(credit_score_api_url, json=payload)

        if response.status_code == 200 or response.status_code == 201:
            return jsonify(credit_score=response.json().get('credit_score')), 200
        else:
            current_app.logger.error(f"not Failed to retrieve credit score: {response.text}")
            return jsonify(error='not Failed to retrieve credit score'), response.status_code

    except requests.RequestException as e:
        current_app.logger.error(f"Request failed: {str(e)}")
        return jsonify(error='Internal server error'), 500
from flask_testing import TestCase

class MyTest(TestCase):

    def test_credit_score_route(self):
        response = self.client.post('/api/customer/credit-score', json={
            'first_name': 'John', 'last_name': 'Doe',
            'ssn': '123-45-6789', 'birth_date': '1980-01-01',
            'address': '123 Elm St'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('credit_score', response.json)
