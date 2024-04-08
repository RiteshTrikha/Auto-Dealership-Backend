from flask import jsonify, request, current_app, g
from flask_jwt_extended import jwt_required
from . import customer_bp
from flasgger import swag_from
from .models import Customer
from app.negotiation.models import Negotiation, Offer
from app.inventory.models import Vehical
from app.exceptions import ExposedException

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# list negotiation dict
# {
#     'negotiations': [{
#         'negotiation_id': negotiation.negotiation_id,
#         'vehical': {
#             'vehical_id': negotiation.vehical_id,
#             'year': negotiation.vehical.year,
#             'make': negotiation.vehical.make,
#             'model': negotiation.vehical.model,
#             'image': negotiation.vehical.image
#         },
#         'customer_id': negotiation.customer_id,
#         'current_offer': negotiation.offers[-1].offer_price,
#         'negotiation_status': Negotiation.NegotiationStatus(negotiation.negotiation_status).name,
#         'start_date': negotiation.start_date,
#         'end_date': negotiation.end_date
#     } for negotiation in negotiations]
# }

# negotiation details dict
# {
#     'negotiation_id': negotiation.negotiation_id,
#     'customer': {
#         'customer_id': negotiation.customer_id,
#         'first_name': negotiation.customer.first_name,
#         'last_name': negotiation.customer.last_name,
#     },
#     'negotiation_status': Negotiation.NegotiationStatus(negotiation.negotiation_status).name,
#     'start_date': negotiation.start_date,
#     'end_date': negotiation.end_date,
#     'current_offer': negotiation.offers[-1].offer_price,
#     'offers': [{
#             'offer_id': offer.offer_id,
#             'offer_type': Offer.OfferType(offer.offer_type).name,
#             'offer_price': offer.offer_price,
#             'offer_date': offer.offer_date,
#             'offer_status': Offer.OfferStatus(offer.offer_status).name,
#             'message': offer.message
#         } for offer in offers],
#     'vehicle': {
#         'vehical_id': negotiation.vehical_id,
#         'year': negotiation.vehical.year,
#         'make': negotiation.vehical.make,
#         'model': negotiation.vehical.model,
#         'image': negotiation.vehical.image
#     }
# }

# Place initial offer and create negotiation
@customer_bp.route('/negotiation/negotiation', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Create negotiation',
    'tags': ['Customer Negotiation'],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'customer_id': {'type': 'integer'},
                        'vehical_id': {'type': 'integer'},
                        'offer_price': {'type': 'integer'},
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    },
    'responses': {
        '201': {
            'description': 'Negotiation created',
            'schema': {
                'type': 'object',
                'properties': {
                    'negotiation_id': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Bad request'
        }
    }
})
def create_negotiation():
  try:
      data = request.get_json()
      customer_id = data['customer_id']
      vehical_id = data['vehical_id']
      offer_price = data['offer_price']
      message = data['message']
      negotiation_id = g.negotiation_service.create_negotiation(vehical_id=vehical_id, customer_id=customer_id, 
                                                                offer_price=offer_price, message=message)
      return standardize_response(data=negotiation_id, 
                                  message='Successfully created negotiation',
                                  code=201)
  except Exception as e:
      raise e

# get list of negotiations by customer
@jwt_required()
@customer_bp.route('/negotiation/negotiations/<int:customer_id>', methods=['GET'])
@swag_from({
  'summary': 'Get list of negotiations by customer',
  'tags': ['Customer Negotiation'],
  'parameters': [
    {
      'in': 'path',
      'name': 'customer_id',
      'type': 'integer',
      'required': True,
      'description': 'The id of the customer'
    }
  ],
  'responses': {
    '200': {
      'description': 'Negotiations found',
      'schema': {
        'type': 'object',
        'properties': {
          'status': {'type': 'string'},
          'data': {
            'type': 'array',
            'items': {
              'type': 'object',
              'properties': {
                  'negotiation_id': {'type': 'integer'},
                  'vehical': {
                      'type': 'object',
                      'properties': {
                          'vehical_id': {'type': 'integer'},
                          'year': {'type': 'integer'},
                          'make': {'type': 'string'},
                          'model': {'type': 'string'},
                          'image': {'type': 'string'}
                      }
                  },
                  'customer_id': {'type': 'integer'},
                  'current_offer': {'type': 'integer'},
                  'negotiation_status': {'type': 'string'},
                  'start_date': {'type': 'string'},
                  'end_date': {'type': 'string'}
              }
            }
          },
          'message': {'type': 'string'},
          'code': {'type': 'integer'}
        }
      }
    },
    '404': {
      'description': 'No negotiations found',
    },
    '400': {
      'description': 'Bad request',
    },
  }
})
def get_negotiations(customer_id):
    try:
        negotiations = g.negotiation_service.get_negotiations(customer_id)
        return standardize_response(data=negotiations, message='Successfully retrieved negotiations',
                                    code=200)
    except Exception as e:
        raise e        

# get negotiation details
@customer_bp.route('/negotiation/negotiation/<int:negotiation_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get negotiation details',
    'tags': ['Customer Negotiation'],
    'parameters': [
        {
            'in': 'path',
            'name': 'negotiation_id',
            'type': 'integer',
            'required': True,
            'description': 'The id of the negotiation'
        }
    ],
    'responses': {
        '200': {
            'description': 'Negotiation found',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'negotiation_id': {'type': 'integer'},
                            'customer': {
                                'type': 'object',
                                'properties': {
                                    'customer_id': {'type': 'integer'},
                                    'first_name': {'type': 'string'},
                                    'last_name': {'type': 'string'}
                                }
                            },
                            'negotiation_status': {'type': 'string'},
                            'start_date': {'type': 'string'},
                            'end_date': {'type': 'string'},
                            'current_offer': {'type': 'integer'},
                            'offers': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'offer_id': {'type': 'integer'},
                                        'offer_type': {'type': 'string'},
                                        'offer_price': {'type': 'integer'},
                                        'offer_date': {'type': 'string'},
                                        'offer_status': {'type': 'string'},
                                        'message': {'type': 'string'}
                                    }
                                }
                            },
                            'vehicle': {
                                'type': 'object',
                                'properties': {
                                    'vehical_id': {'type': 'integer'},
                                    'year': {'type': 'integer'},
                                    'make': {'type': 'string'},
                                    'model': {'type': 'string'},
                                    'image': {'type': 'string'}
                                }
                            }
                        }
                    },
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        },
        '404': {
            'description': 'No negotiation found',
        },
        '400': {
            'description': 'Bad request',
        },
    }
})
def get_negotiation_details(negotiation_id):
    try:
        negotiation_details = g.negotiation_service.get_negotiation_details(negotiation_id)
        if negotiation_details is None:
            return standardize_response(status='fail', message='No negotiation found', code=404)
        return standardize_response(data=negotiation_details,
                                    message='Successfully retrieved negotiation')
    except Exception as e:
        raise e

# place additional offer
@customer_bp.route('/negotiation/negotiation/<int:negotiation_id>/offer', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Place additional offer',
    'tags': ['Customer Negotiation'],
    'consumes': 'application/json',
    'parameters': [
        {
            'in': 'path',
            'name': 'negotiation_id',
            'type': 'integer',
            'required': True,
            'description': 'The id of the negotiation'
        }
    ],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'offer_price': {'type': 'integer'},
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    },
    'responses': {
        '201': {
            'description': 'Offer placed',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'description': 'Request status'},
                    'data': {'type': 'integer', 'description': 'Offer id'},
                    'message': {'type': 'string', 'description': 'Status message'},
                    'code': {'type': 'integer', 'description': 'HTTP status code'}
                }
            }
        },
        '400': {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'description': 'Request status'},
                    'message': {'type': 'string', 'description': 'Error message'},
                    'code': {'type': 'integer', 'description': 'HTTP status code'}
                }
            }
        }
    }
})
def place_offer(negotiation_id):
    try:
        data = request.get_json()
        offer_price = data['offer_price']
        message = data['message']
        if not offer_price:
            raise ExposedException('Missing required fields', code=400)
        offer_id = g.negotiation_service.additional_offer(negotiation_id=negotiation_id, offer_price=offer_price,
                                                    message=message)
        return standardize_response(data=offer_id, 
                                    message='Successfully placed offer', 
                                    code=201)
    except Exception as e:
        raise e

# accept counter offer
@customer_bp.route('/negotiation/negotiation/<int:negotiation_id>/accept', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Accept counter offer',
    'tags': ['Customer Negotiation'],
    'parameters': [
        {
            'in': 'path',
            'name': 'negotiation_id',
            'type': 'integer',
            'required': True,
            'description': 'The id of the negotiation'
        }
    ],
    'responses': {
        '200': {
            'description': 'Offer accepted',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'description': 'Request status'},
                    'data': {'type': 'object', 'description': 'Empty object'},
                    'message': {'type': 'string', 'description': 'Status message'},
                    'code': {'type': 'integer', 'description': 'HTTP status code'}
                }
            }
        },
        '400': {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'description': 'Request status'},
                    'message': {'type': 'string', 'description': 'Error message'},
                    'code': {'type': 'integer', 'description': 'HTTP status code'}
                }
            }
        }
    }
})
def accept_offer(negotiation_id):
    try:
        g.negotiation_service.accept_counter_offer(negotiation_id)
        return standardize_response(message='Successfully accepted offer')
    except Exception as e:
        raise e
    
# reject counter offer
@customer_bp.route('/negotiation/negotiation/<int:negotiation_id>/reject', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Reject counter offer',
    'tags': ['Customer Negotiation'],
    'parameters': [
        {
            'in': 'path',
            'name': 'negotiation_id',
            'type': 'integer',
            'required': True,
            'description': 'The id of the negotiation'
        }
    ],
    'responses': {
        '200': {
            'description': 'Offer rejected',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'description': 'Request status'},
                    'data': {'type': 'object', 'description': 'Empty object'},
                    'message': {'type': 'string', 'description': 'Status message'},
                    'code': {'type': 'integer', 'description': 'HTTP status code'}
                }
            }
        },
        '400': {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'description': 'Request status'},
                    'message': {'type': 'string', 'description': 'Error message'},
                    'code': {'type': 'integer', 'description': 'HTTP status code'}
                }
            }
        }
    }
})
def reject_offer(negotiation_id):
    try:
        g.negotiation_service.reject_counter_offer(negotiation_id)
        return standardize_response(message='Successfully rejected offer')
    except Exception as e:
        raise e