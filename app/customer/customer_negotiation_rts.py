from flask import jsonify, request, current_app, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import customer_bp
from flasgger import swag_from
from .models import Customer
from app.negotiation.models import Negotiation, Offer
from app.inventory.models import Vehicle
from app.exceptions import ExposedException

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# Place initial offer and create negotiation
@customer_bp.route('/negotiation/negotiation', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Create negotiation',
    'tags': ['Customer Negotiation'],
    'security': [{'BearerAuth': []}],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'vehicle_id': {'type': 'integer', 'example': 1},
                        'offer_price': {'type': 'integer', 'example': 10000},
                        'message': {'type': 'string', 'example': 'I like the car. but I noticed a scratch on the bumper... can I get a discount?'}
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
      customer_id = get_jwt_identity().get('customer_id')
      vehicle_id = data['vehicle_id'] 
      offer_price = data['offer_price']
      message = data['message']
      negotiation_id = g.negotiation_service.create_negotiation(vehicle_id=vehicle_id, customer_id=customer_id, 
                                                                offer_price=offer_price, message=message)
      return standardize_response(data=negotiation_id, 
                                  message='Successfully created negotiation',
                                  code=201)
  except Exception as e:
      raise e

# get list of negotiations by customer
@customer_bp.route('/negotiation/negotiations/', methods=['GET'])
@jwt_required()
@swag_from({
  'summary': 'Get list of negotiations by customer',
  'tags': ['Customer Negotiation'],
  'security': [{'BearerAuth': []}],
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
                  'vehicle': {
                      'type': 'object',
                      'properties': {
                          'vehicle_id': {'type': 'integer'},
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
def get_negotiations():
    try:
        customer_id = get_jwt_identity().get('customer_id')
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
    'security': [{'BearerAuth': []}],
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
                                    'vehicle_id': {'type': 'integer'},
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
    'security': [{'BearerAuth': []}],
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
                        'offer_price': {'type': 'integer', 'example': 10000},
                        'message': {'type': 'string', 'example': 'I\'m not made of money! I have a wife and kids!'}
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
    'security': [{'BearerAuth': []}],
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
    'security': [{'BearerAuth': []}],
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
    
