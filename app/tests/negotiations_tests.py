import os
import sys
sys.path.append('.')

import unittest
from app import create_app, db, current_app
from config import TestingConfig
import shutil
from sqlalchemy import text


class NegotiationsTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

        self.customer_token = self.customer_login()['data']['access_token']
        self.manager_token = self.manager_login()['data']['access_token']

    def customer_login(self):
        response = self.client.post('api/auth/customer/login', json={
            'email': 'email',
            'password': 'password'
        })
        return response.json

    def manager_login(self):
        response = self.client.post('api/auth/user/login', json={
            'email': 'manager',
            'password': 'manager'
        })
        return response.json


    # Tests

    def test_create_negotiation_1(self):
        response = self.client.post('api/customer/negotiation/negotiation', headers={
            'Authorization': f'Bearer {self.customer_token}'
        }, json={
            'vehicle_id': 1,
            'offer_price': 10000,
            'message': 'I want to buy this car.'
        })
        print(response.json)
        self.assertEqual(response.json['code'], 201)

    # def test_get_customer_negotiations(self):
    #     response = self.client.get('api/customer/negotiation/negotiations', headers={
    #         'Authorization': f'Bearer {self.customer_token}'
    #     })
    #     print(response.json)
    #     self.assertEqual(response.json['code'], 200)

    # def test_get_customer_negotiation_details(self):
    #     response = self.client.get('api/customer/negotiation/negotiation/1', headers={
    #         'Authorization': f'Bearer {self.customer_token}'
    #     })
    #     print(response.json)
    #     self.assertEqual(response.json['code'], 200)

    # def test_user_get_all_negotiations(self):
    #     response = self.client.get('api/user/negotiation/negotiations', headers={
    #         'Authorization': f'Bearer {self.manager_token}'
    #     })
        
    #     self.assertEqual(response.json['code'], 200)

    # def test_user_get_negotiation_details(self):
    #     response = self.client.get('api/user/negotiation/negotiation/1', headers={
    #         'Authorization': f'Bearer {self.manager_token}'
    #     })

    #     self.assertEqual(response.json['code'], 200)
    
    # def test_user_place_counter_offer(self):
    #     response = self.client.post('api/user/negotiation/negotiation/1/counter-offer', headers={
    #         'Authorization': f'Bearer {self.manager_token}'
    #     }, json={
    #         'offer_price': 12000,
    #         'message': 'I can\'t go lower than this.'
    #     })

    #     self.assertEqual(response.json['code'], 200)

    # def test_customer_place_additional_offer(self):
    #     response = self.client.post('api/customer/negotiation/negotiation/1/offer', headers={
    #         'Authorization': f'Bearer {self.customer_token}'
    #     }, json={
    #         'offer_price': 11000,
    #         'message': 'I can\'t go higher than this.'
    #     })

    #     self.assertEqual(response.json['code'], 201)

    # def test_user_accept_offer(self):
    #     response = self.client.post('api/user/negotiation/negotiation/1/accept-offer', headers={
    #         'Authorization': f'Bearer {self.manager_token}'
    #     })

    #     self.assertEqual(response.json['code'], 200)

    # def test_user_reject_offer_2(self):
    #     response = self.client.post('api/user/negotiation/negotiation/2/reject-offer', headers={
    #         'Authorization': f'Bearer {self.manager_token}'
    #     })

    #     self.assertEqual(response.json['code'], 200)

    def tearDown(self):
        with self.app.app_context():
            db.session.execute(text('DELETE FROM offer'))
            db.session.execute(text('DELETE FROM negotiation'))
            db.session.execute(text('ALTER TABLE offer AUTO_INCREMENT = 1'))
            db.session.execute(text('ALTER TABLE negotiation AUTO_INCREMENT = 1'))
            db.session.commit()
            db.session.close()



if __name__ == '__main__':
    unittest.main()

# from flask import jsonify, request, current_app, g
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from . import customer_bp
# from flasgger import swag_from
# from .models import Customer
# from app.negotiation.models import Negotiation, Offer
# from app.inventory.models import Vehicle
# from app.exceptions import ExposedException

# # import utilities
# from app.utilities import Utilities
# standardize_response = Utilities.standardize_response

# # Place initial offer and create negotiation
# @customer_bp.route('/negotiation/negotiation', methods=['POST'])
# @jwt_required()
# @swag_from({
#     'summary': 'Create negotiation',
#     'tags': ['Customer Negotiation'],
#     'security': [{'BearerAuth': []}],
#     'requestBody': {
#         'content': {
#             'application/json': {
#                 'schema': {
#                     'type': 'object',
#                     'properties': {
#                         'vehicle_id': {'type': 'integer', 'example': 1},
#                         'offer_price': {'type': 'integer', 'example': 10000},
#                         'message': {'type': 'string', 'example': 'I like the car. but I noticed a scratch on the bumper... can I get a discount?'}
#                     }
#                 }
#             }
#         }
#     },
#     'responses': {
#         '201': {
#             'description': 'Negotiation created',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'string', 'description': 'Request status'},
#                     'data': {'type': 'integer', 'description': 'Negotiation id'},
#                     'message': {'type': 'string', 'description': 'Status message'},
#                     'code': {'type': 'integer', 'description': 'HTTP status code'}
#                 }
#             }
#         },
#         '400': {
#             'description': 'Bad request'
#         }
#     }
# })
# def create_negotiation():
#   try:
#       data = request.get_json()
#       customer_id = get_jwt_identity().get('customer_id')
#       vehicle_id = data['vehicle_id'] 
#       offer_price = data['offer_price']
#       message = data['message']
#       negotiation_id = g.negotiation_service.create_negotiation(vehicle_id=vehicle_id, customer_id=customer_id, 
#                                                                 offer_price=offer_price, message=message)
#       return standardize_response(data=negotiation_id, 
#                                   message='Successfully created negotiation',
#                                   code=201)
#   except Exception as e:
#       raise e

# # get list of negotiations by customer
# @customer_bp.route('/negotiation/negotiations/', methods=['GET'])
# @jwt_required()
# @swag_from({
#   'summary': 'Get list of negotiations by customer',
#   'tags': ['Customer Negotiation'],
#   'security': [{'BearerAuth': []}],
#   'responses': {
#     '200': {
#       'description': 'Negotiations found',
#       'schema': {
#         'type': 'object',
#         'properties': {
#           'status': {'type': 'string'},
#           'data': {
#             'type': 'array',
#             'items': {
#               'type': 'object',
#               'properties': {
#                   'negotiation_id': {'type': 'integer'},
#                   'vehicle': {
#                       'type': 'object',
#                       'properties': {
#                           'vehicle_id': {'type': 'integer'},
#                           'year': {'type': 'integer'},
#                           'make': {'type': 'string'},
#                           'model': {'type': 'string'},
#                           'image': {'type': 'string'}
#                       }
#                   },
#                   'customer_id': {'type': 'integer'},
#                   'current_offer': {'type': 'integer'},
#                   'negotiation_status': {'type': 'string'},
#                   'start_date': {'type': 'string'},
#                   'end_date': {'type': 'string'}
#               }
#             }
#           },
#           'message': {'type': 'string'},
#           'code': {'type': 'integer'}
#         }
#       }
#     },
#     '404': {
#       'description': 'No negotiations found',
#     },
#     '400': {
#       'description': 'Bad request',
#     },
#   }
# })
# def get_negotiations():
#     try:
#         customer_id = get_jwt_identity().get('customer_id')
#         negotiations = g.negotiation_service.get_negotiations(customer_id)
#         return standardize_response(data=negotiations, message='Successfully retrieved negotiations',
#                                     code=200)
#     except Exception as e:
#         raise e        

# # get negotiation details
# @customer_bp.route('/negotiation/negotiation/<int:negotiation_id>', methods=['GET'])
# @jwt_required()
# @swag_from({
#     'summary': 'Get negotiation details',
#     'tags': ['Customer Negotiation'],
#     'security': [{'BearerAuth': []}],
#     'parameters': [
#         {
#             'in': 'path',
#             'name': 'negotiation_id',
#             'type': 'integer',
#             'required': True,
#             'description': 'The id of the negotiation'
#         }
#     ],
#     'responses': {
#         '200': {
#             'description': 'Negotiation found',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'string'},
#                     'data': {
#                         'type': 'object',
#                         'properties': {
#                             'negotiation_id': {'type': 'integer'},
#                             'customer': {
#                                 'type': 'object',
#                                 'properties': {
#                                     'customer_id': {'type': 'integer'},
#                                     'first_name': {'type': 'string'},
#                                     'last_name': {'type': 'string'}
#                                 }
#                             },
#                             'negotiation_status': {'type': 'string'},
#                             'start_date': {'type': 'string'},
#                             'end_date': {'type': 'string'},
#                             'current_offer': {'type': 'integer'},
#                             'offers': {
#                                 'type': 'array',
#                                 'items': {
#                                     'type': 'object',
#                                     'properties': {
#                                         'offer_id': {'type': 'integer'},
#                                         'offer_type': {'type': 'string'},
#                                         'offer_price': {'type': 'integer'},
#                                         'offer_date': {'type': 'string'},
#                                         'offer_status': {'type': 'string'},
#                                         'message': {'type': 'string'}
#                                     }
#                                 }
#                             },
#                             'vehicle': {
#                                 'type': 'object',
#                                 'properties': {
#                                     'vehicle_id': {'type': 'integer'},
#                                     'year': {'type': 'integer'},
#                                     'make': {'type': 'string'},
#                                     'model': {'type': 'string'},
#                                     'image': {'type': 'string'}
#                                 }
#                             }
#                         }
#                     },
#                     'message': {'type': 'string'},
#                     'code': {'type': 'integer'}
#                 }
#             }
#         },
#         '404': {
#             'description': 'No negotiation found',
#         },
#         '400': {
#             'description': 'Bad request',
#         },
#     }
# })
# def get_negotiation_details(negotiation_id):
#     try:
#         negotiation_details = g.negotiation_service.get_negotiation_details(negotiation_id)
#         if negotiation_details is None:
#             return standardize_response(status='fail', message='No negotiation found', code=404)
#         return standardize_response(data=negotiation_details,
#                                     message='Successfully retrieved negotiation')
#     except Exception as e:
#         raise e

# # place additional offer
# @customer_bp.route('/negotiation/negotiation/<int:negotiation_id>/offer', methods=['POST'])
# @jwt_required()
# @swag_from({
#     'summary': 'Place additional offer',
#     'tags': ['Customer Negotiation'],
#     'consumes': 'application/json',
#     'security': [{'BearerAuth': []}],
#     'parameters': [
#         {
#             'in': 'path',
#             'name': 'negotiation_id',
#             'type': 'integer',
#             'required': True,
#             'description': 'The id of the negotiation'
#         }
#     ],
#     'requestBody': {
#         'content': {
#             'application/json': {
#                 'schema': {
#                     'type': 'object',
#                     'properties': {
#                         'offer_price': {'type': 'integer', 'example': 10000},
#                         'message': {'type': 'string', 'example': 'I\'m not made of money! I have a wife and kids!'}
#                     }
#                 }
#             }
#         }
#     },
#     'responses': {
#         '201': {
#             'description': 'Offer placed',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'string', 'description': 'Request status'},
#                     'data': {'type': 'integer', 'description': 'Offer id'},
#                     'message': {'type': 'string', 'description': 'Status message'},
#                     'code': {'type': 'integer', 'description': 'HTTP status code'}
#                 }
#             }
#         },
#         '400': {
#             'description': 'Bad request',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'string', 'description': 'Request status'},
#                     'message': {'type': 'string', 'description': 'Error message'},
#                     'code': {'type': 'integer', 'description': 'HTTP status code'}
#                 }
#             }
#         }
#     }
# })
# def place_offer(negotiation_id):
#     try:
#         data = request.get_json()
#         offer_price = data['offer_price']
#         message = data['message']
#         if not offer_price:
#             raise ExposedException('Missing required fields', code=400)
#         offer_id = g.negotiation_service.additional_offer(negotiation_id=negotiation_id, offer_price=offer_price,
#                                                     message=message)
#         return standardize_response(data=offer_id, 
#                                     message='Successfully placed offer', 
#                                     code=201)
#     except Exception as e:
#         raise e

# # accept counter offer
# @customer_bp.route('/negotiation/negotiation/<int:negotiation_id>/accept', methods=['POST'])
# @jwt_required()
# @swag_from({
#     'summary': 'Accept counter offer',
#     'tags': ['Customer Negotiation'],
#     'security': [{'BearerAuth': []}],
#     'parameters': [
#         {
#             'in': 'path',
#             'name': 'negotiation_id',
#             'type': 'integer',
#             'required': True,
#             'description': 'The id of the negotiation'
#         }
#     ],
#     'responses': {
#         '200': {
#             'description': 'Offer accepted',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'string', 'description': 'Request status'},
#                     'data': {'type': 'object', 'description': 'Empty object'},
#                     'message': {'type': 'string', 'description': 'Status message'},
#                     'code': {'type': 'integer', 'description': 'HTTP status code'}
#                 }
#             }
#         },
#         '400': {
#             'description': 'Bad request',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'string', 'description': 'Request status'},
#                     'message': {'type': 'string', 'description': 'Error message'},
#                     'code': {'type': 'integer', 'description': 'HTTP status code'}
#                 }
#             }
#         }
#     }
# })
# def accept_offer(negotiation_id):
#     try:
#         g.negotiation_service.accept_counter_offer(negotiation_id)
#         return standardize_response(message='Successfully accepted offer')
#     except Exception as e:
#         raise e

# # reject counter offer
# @customer_bp.route('/negotiation/negotiation/<int:negotiation_id>/reject', methods=['POST'])
# @jwt_required()
# @swag_from({
#     'summary': 'Reject counter offer',
#     'tags': ['Customer Negotiation'],
#     'security': [{'BearerAuth': []}],
#     'parameters': [
#         {
#             'in': 'path',
#             'name': 'negotiation_id',
#             'type': 'integer',
#             'required': True,
#             'description': 'The id of the negotiation'
#         }
#     ],
#     'responses': {
#         '200': {
#             'description': 'Offer rejected',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'string', 'description': 'Request status'},
#                     'data': {'type': 'object', 'description': 'Empty object'},
#                     'message': {'type': 'string', 'description': 'Status message'},
#                     'code': {'type': 'integer', 'description': 'HTTP status code'}
#                 }
#             }
#         },
#         '400': {
#             'description': 'Bad request',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'string', 'description': 'Request status'},
#                     'message': {'type': 'string', 'description': 'Error message'},
#                     'code': {'type': 'integer', 'description': 'HTTP status code'}
#                 }
#             }
#         }
#     }
# })
# def reject_offer(negotiation_id):
#     try:
#         g.negotiation_service.reject_counter_offer(negotiation_id)
#         return standardize_response(message='Successfully rejected offer')
#     except Exception as e:
#         raise e
    
# from flask import jsonify, request, current_app, g
# from flask_jwt_extended import jwt_required
# from flasgger import swag_from
# from . import user_bp
# from app.negotiation.models import Negotiation, Offer
# from app.inventory.models import Vehicle
# from app.exceptions import ExposedException
# from app.auth.auth_decorators import manager_required

# # import utilities
# from app.utilities import Utilities
# standardize_response = Utilities.standardize_response

# # get all negotiations
# @user_bp.route('/negotiation/negotiations', methods=['GET'])
# @jwt_required()
# @manager_required
# def get_all_negotiations():
#     """
#     Get all negotiations
#     ---
#     tags: [User Negotiation]
#     security: [{'BearerAuth': []}]
#     responses:
#         200:
#             description: Negotiations found
#             schema:
#                 type: object
#                 properties:
#                     status: { type: string }
#                     message: { type: string }
#                     data:
#                         type: array
#                         items:
#                             type: object
#                             properties:
#                                 negotiation_id: { type: integer }
#                                 vehicle:
#                                     type: object
#                                     properties:
#                                         vehicle_id: { type: integer }
#                                         year: { type: integer }
#                                         make: { type: string }
#                                         model: { type: string }
#                                         image: { type: string }
#                                 customer_id: { type: integer }
#                                 negotiation_status: { type: integer }
#                                 start_date: { type: string }
#                                 end_date: { type: string }
#                     code: { type: integer }
#         404:
#             description: No negotiations found
#             schema:
#                 type: object
#                 properties:
#                     status: { type: string }
#                     message: { type: string }
#                     data: { type: null }
#                     code: { type: integer }
#         500:
#             description: Internal server error
#             schema:
#                 type: object
#                 properties:
#                     status: { type: string }
#                     message: { type: string }
#                     data: { type: null }
#                     code: { type: integer }
#     """
#     try:
#         negotiations = g.negotiation_service.get_all_negotiations()
#         if negotiations == []:
#             return standardize_response(status='fail', message='No negotiations found', data=None, code=404)
#         return standardize_response(status='success', message='Negotiations found', 
#                                     data=negotiations, code=200)
#     except Exception as e:
#         raise e
    
# # get negotiation details by negotiation id
# @user_bp.route('/negotiation/negotiation/<int:negotiation_id>', methods=['GET'])
# def get_negotiation_details(negotiation_id):
#     """
#     Get negotiation details by negotiation id
#     ---
#     tags: [User Negotiation]
#     parameters:
#         - in: path
#           name: negotiation_id
#           required: true
#           schema:
#             type: integer
#     responses:
#         200:
#             description: Negotiation found
#             schema:
#                 type: object
#                 properties:
#                     status: { type: string }
#                     message: { type: string }
#                     data: 
#                         type: object
#                         properties:
#                             negotiation: 
#                                 type: object
#                                 properties:
#                                     negotiation_id: { type: integer }
#                                     vehicle_id: { type: integer }
#                                     customer_id: { type: integer }
#                                     negotiation_status: { type: integer }
#                                     start_date: { type: string }
#                                     end_date: { type: string }
#                                     offers:
#                                         type: array
#                                         items:
#                                             type: object
#                                             properties:
#                                                 offer_id: { type: integer }
#                                                 offer_type: { type: string }
#                                                 offer_price: { type: number }
#                                                 offer_date: { type: string }
#                                                 offer_status: { type: string }
#                                                 message: { type: string }
#                             vehicle:
#                                 type: object
#                                 properties:
#                                     vehicle_id: { type: integer }
#                                     year: { type: integer }
#                                     make: { type: string }
#                                     model: { type: string }
#                                     image: { type: string }
#                     message: { type: string }
#                     code: { type: integer }
#         404:
#             description: Negotiation not found
#             schema:
#                 type: object
#                 properties:
#                     status: { type: string }
#                     message: { type: string }
#                     data: { type: null }
#                     code: { type: integer }
#         500:
#             description: Internal server error
#             schema:
#                 type: object
#                 properties:
#                     status: { type: string }
#                     message: { type: string }
#                     data: { type: null }
#                     code: { type: integer }
#     """
#     try:
#         negotiation_details = g.negotiation_service.get_negotiation_details(negotiation_id)
#         if not negotiation_details:
#             return standardize_response(status='fail', message='Negotiation not found', data=None, code=404)
#         return standardize_response(status='success', 
#                                     message='Negotiation found', 
#                                     data=negotiation_details,
#                                     code=200)
#     except Exception as e:
#         raise e

# # place counter offer
# @user_bp.route('/negotiation/negotiation/<int:negotiation_id>/counter-offer', methods=['POST'])
# @swag_from({
#     'summary': 'Place counter offer',
#     'tags': ['User Negotiation'],
#     'parameters': [
#         {
#             'in': 'path',
#             'name': 'negotiation_id',
#             'required': True,
#             'schema': {
#                 'type': 'integer'
#             }
#         }
#     ],
#     'requestBody': {
#         'description': 'Counter offer data',
#         'content': {
#             'application/json': {
#                 'schema': {
#                     'type': 'object',
#                     'properties': {
#                         'offer_price': { 'type': 'integer', 'example': 10000 },
#                         'message': { 'type': 'string', 'example': 'It\'s worth more than that... You look like you can afford it.' }
#                     }
#                 }
#             }
#         }
#     },
#     'responses': {
#         '200': {
#             'description': 'Counter offer placed',
#             'content': {
#                 'application/json': {
#                     'schema': {
#                         'type': 'object',
#                         'properties': {
#                             'status': { 'type': 'string' },
#                             'message': { 'type': 'string' },
#                             'data': { 'type': 'integer' },
#                             'code': { 'type': 'integer' }
#                         }
#                     }
#                 }
#             }
#         },
#         '500': {
#             'description': 'Internal server error',
#             'content': {
#                 'application/json': {
#                     'schema': {
#                         'type': 'object',
#                         'properties': {
#                             'status': { 'type': 'string' },
#                             'message': { 'type': 'string' },
#                             'data': { 'type': 'null' },
#                             'code': { 'type': 'integer' }
#                         }
#                     }
#                 }
#             }
#         }
#     }
# })
# def place_counter_offer(negotiation_id):
#     try:
#         data = request.get_json()
#         offer_price = data.get('offer_price')
#         message = data.get('message')
#         offer_id = g.negotiation_service.counter_offer(negotiation_id=negotiation_id, offer_price=offer_price,
#                                                        message=message)
#         return standardize_response(status='success', message='Counter offer placed', data=offer_id, code=200)
#     except Exception as e:
#         raise e
    
# # accept offer
# @user_bp.route('/negotiation/negotiation/<int:negotiation_id>/accept-offer', methods=['POST'])
# def accept_offer(negotiation_id):
#     """
#     Accept offer
#     ---
#     tags: [User Negotiation]
#     parameters:
#         - in: path
#           name: negotiation_id
#           required: true
#           schema:
#             type: integer
#     responses:
#         200:
#             description: Offer accepted
#             schema:
#                 type: object
#                 properties:
#                     status: { type: string }
#                     message: { type: string }
#                     data: { type: null }
#                     code: { type: integer }
#         500:
#             description: Internal server error
#             schema:
#                 type: object
#                 properties:
#                     status: { type: string }
#                     message: { type: string }
#                     data: { type: null }
#                     code: { type: integer }
#     """
#     try:
#         g.negotiation_service.accept_offer(negotiation_id)
#         return standardize_response(status='success', message='Offer accepted', data=None, code=200)
#     except Exception as e:
#         raise e
    
# # reject offer
# @user_bp.route('/negotiation/negotiation/<int:negotiation_id>/reject-offer', methods=['POST'])
# def reject_offer(negotiation_id):
#     """
#     Reject offer
#     ---
#     tags: [User Negotiation]
#     parameters:
#         - in: path
#           name: negotiation_id
#           required: true
#           schema:
#             type: integer
#     responses:
#         200:
#             description: Offer rejected
#             schema:
#                 type: object
#                 properties:
#                     status: { type: string }
#                     message: { type: string }
#                     data: { type: null }
#                     code: { type: integer }
#         500:
#             description: Internal server error
#             schema:
#                 type: object
#                 properties:
#                     status: { type: string }
#                     message: { type: string }
#                     data: { type: null }
#                     code: { type: integer }
#     """
#     try:
#         g.negotiation_service.reject_offer(negotiation_id)
#         return standardize_response(status='success', message='Offer rejected', data=None, code=200)
#     except Exception as e:
#         raise e
    
