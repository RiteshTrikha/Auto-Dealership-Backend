from flask import jsonify, request, current_app, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import customer_bp
from flasgger import swag_from
from app.customer.models import Customer
from .services import CustomerServices
from app.exceptions import ExposedException

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

#get customer vehicle by customer_vehilce_id
@customer_bp.route('/vehicle/<int:customer_vehicle_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get Customer Vehicle',
    'tags': ['Customer Vehicle'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'customer_vehicle_id',
            'type': 'integer',
            'required': True,
            'description': 'Customer Vehicle ID'
        }
    ],
    'responses': {
        '200': {
            'description': 'Customer Vehicle',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'object',
                        'properties': {
                            'customer_vehilce_id': {'type': 'integer'},
                            'vin': {'type': 'string'},
                            'year': {'type': 'integer'},
                            'make': {'type': 'string'},
                            'model': {'type': 'string'}
                        }
                    },
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        },
        '404': {
            'description': 'Customer Vehicle not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        }
    }
})
def get_customer_vehicle(customer_vehicle_id):
    try:
        vehicle = g.customer_service.get_vehicle(customer_vehicle_id)
        vehicle = vehicle.to_dict()
        return standardize_response(data=vehicle, message='Customer Vehicle', code=200)
    except Exception as e:
        raise e
    
#get customer vehicles by customer_id
@customer_bp.route('/vehicles/<int:customer_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get Customer Vehicles',
    'tags': ['Customer Vehicle'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'customer_id',
            'type': 'integer',
            'required': True,
            'description': 'Customer ID'
        }
    ],
    'responses': {
        '200': {
            'description': 'Customer Vehicles',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'customer_vehilce_id': {'type': 'integer'},
                                'vin': {'type': 'string'},
                                'year': {'type': 'integer'},
                                'make': {'type': 'string'},
                                'model': {'type': 'string'}
                            }
                        }
                    },
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        },
        '404': {
            'description': 'Customer Vehicles not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        }
    }
})
def get_customer_vehicles(customer_id):
    try:
        vehicles = g.customer_service.get_vehicles(customer_id)
        vehicles = [vehicle.to_dict() for vehicle in vehicles]
        return standardize_response(data=vehicles, message='Customer Vehicles', code=200)
    except Exception as e:
        raise e
    
#update customer vehicle
@customer_bp.route('/vehicle/<int:customer_vehicle_id>', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Update Customer Vehicle',
    'tags': ['Customer Vehicle'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'customer_vehicle_id',
            'type': 'integer',
            'required': True,
            'description': 'Customer Vehicle ID'
        }
    ],
    'requestBody': {
        'description': 'Customer Vehicle',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'year': {'type': 'integer'},
                        'make': {'type': 'string'},
                        'model': {'type': 'string'}
                    }
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Customer Vehicle updated',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'object',
                        'properties': {
                            'customer_vehicle_id': {'type': 'integer'},
                            'vin': {'type': 'string'},
                            'year': {'type': 'integer'},
                            'make': {'type': 'string'},
                            'model': {'type': 'string'}
                        }
                    },
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        },
        '404': {
            'description': 'Customer Vehicle not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        }
    }
})
def update_customer_vehicle(customer_vehicle_id):
    try:
        data = request.get_json()
        year = data.get('year')
        make = data.get('make')
        model = data.get('model')
        vehicle = g.customer_service.update_vehicle(customer_vehicle_id=customer_vehicle_id, year=year, make=make, model=model)
        return standardize_response(data=vehicle.to_dict(), message='Customer Vehicle updated', code=200)
    except Exception as e:
        raise e
    
#create customer vehicle
@customer_bp.route('/vehicle', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Create Customer Vehicle',
    'tags': ['Customer Vehicle'],
    'security': [{'BearerAuth': []}],
    'requestBody': {
        'description': 'Customer Vehicle',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'customer_id': {'type': 'integer'},
                        'vin': {'type': 'string'},
                        'year': {'type': 'integer'},
                        'make': {'type': 'string'},
                        'model': {'type': 'string'}
                    }
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Customer Vehicle created',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'object',
                        'properties': {
                            'customer_vehilce_id': {'type': 'integer'},
                            'vin': {'type': 'string'},
                            'year': {'type': 'integer'},
                            'make': {'type': 'string'},
                            'model': {'type': 'string'}
                        }
                    },
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        }
    }
})
def create_customer_vehicle():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        vin = data.get('vin')
        year = data.get('year')
        make = data.get('make')
        model = data.get('model')
        vehicle = g.customer_service.create_customer_vehicle(customer_id=customer_id, vin=vin, year=year, make=make, model=model)
        return standardize_response(data=vehicle.to_dict(), message='Customer Vehicle created', code=200)
    except Exception as e:
        raise e
    
#delete customer vehicle
@customer_bp.route('/vehicle/<int:customer_vehicle_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'summary': 'Delete Customer Vehicle',
    'tags': ['Customer Vehicle'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'customer_vehicle_id',
            'type': 'integer',
            'required': True,
            'description': 'Customer Vehicle ID'
        }
    ],
    'responses': {
        '200': {
            'description': 'Customer Vehicle deleted',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        },
        '404': {
            'description': 'Customer Vehicle not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        }
    }
})
def delete_customer_vehicle(customer_vehicle_id):
    try:
        g.customer_service.delete_vehicle(customer_vehicle_id)
        return standardize_response(message='Customer Vehicle deleted', code=200)
    except Exception as e:
        raise e