from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required
import requests
from . import credit_bp
from flasgger import swag_from

@credit_bp.route('/customer/credit-score', methods=['GET'])
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
def request_credit_score(first_name, last_name, ssn, birth_date, address):
    # Stub or actual API endpoint
    try:
        credit_score_api_url = 'http://127.0.0.1:8080/customer/credit-score'  # Replace with real URL
        payload = {
            'first_name': first_name, 'last_name': last_name,
            'ssn': ssn, 'birth_date': birth_date, 'address': address
        }
        response = requests.post(credit_score_api_url, json=payload)
        if response.status_code == 200:
            return jsonify(credit_score=response.json()['credit_score']), 200
        else:
            current_app.logger.error('Failed to retrieve credit score')
            return jsonify(error='Failed to retrieve credit score'), 400
    except requests.RequestException as e:
        current_app.logger.error(f"Request failed: {str(e)}")
        return jsonify(error='Internal server error'), 500


# Example of a simple test case
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
