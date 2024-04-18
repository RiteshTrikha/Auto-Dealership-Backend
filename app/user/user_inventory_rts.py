from flask import jsonify, request, current_app, g
from . import user_bp
from app.inventory.models import Vehical
from app.exceptions import ExposedException
from flasgger import swag_from

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# create vehicle
@user_bp.route('/inventory/', methods=['POST'])
@swag_from({
    'summary': 'Create vehicle',
    'tags': ['User Vehicle'],
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'vin': {'type': 'string'},
                    'price': {'type': 'integer'},
                    'year': {'type': 'string'},
                    'make': {'type': 'string'},
                    'model': {'type': 'string'},
                    'miles': {'type': 'integer'},
                    'mpg': {'type': 'integer'},
                    'color': {'type': 'string'},
                    'fuel_type': {'type': 'string'},
                    'transmission': {'type': 'string'},
                    'image': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Vehicle created successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'vehicle_id': {'type': 'integer'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad request',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def create_vehicle():
    try:
        data = request.get_json()
        vin = data.get('vin')
        price = data.get('price')
        year = data.get('year')
        make = data.get('make')
        model = data.get('model')
        miles = data.get('miles')
        mpg = data.get('mpg')
        color = data.get('color')
        fuel_type = data.get('fuel_type')
        image = data.get('image')
        transmission = data.get('transmission')
        vehicle_id = g.inventory_service.create_vehicle(vin=vin, price=price, year=year, make=make, 
                                                     model=model, miles=miles, mpg=mpg, color=color, 
                                                     fuel_type=fuel_type, image=image, 
                                                     transmission=transmission)
        return standardize_response(data=vehicle_id, message='Vehicle created successfully', code=201)
    except Exception as e:
        raise e
    
# update vehicle
@user_bp.route('/inventory/vehicle/<int:vehicle_id>', methods=['PUT'])
@swag_from({
    'summary': 'Update vehicle',
    'tags': ['User Vehicle'],
    'parameters': [
        {
            'in': 'path',
            'name': 'vehicle_id',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'vin': {'type': 'string'},
                    'price': {'type': 'integer'},
                    'year': {'type': 'string'},
                    'make': {'type': 'string'},
                    'model': {'type': 'string'},
                    'miles': {'type': 'integer'},
                    'mpg': {'type': 'integer'},
                    'color': {'type': 'string'},
                    'fuel_type': {'type': 'string'},
                    'transmission': {'type': 'string'},
                    'image': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Vehicle updated successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'vehicle_id': {'type': 'integer'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad request',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def update_vehicle(vehicle_id):
    try:
        data = request.get_json()
        vin = data.get('vin')
        price = data.get('price')
        year = data.get('year')
        make = data.get('make')
        model = data.get('model')
        miles = data.get('miles')
        mpg = data.get('mpg')
        color = data.get('color')
        fuel_type = data.get('fuel_type')
        image = data.get('image')
        transmission = data.get('transmission')
        vehicle_id = g.inventory_service.update_vehicle(vehicle_id, vin=vin, price=price, year=year, 
                                                     make=make, model=model, miles=miles, mpg=mpg, 
                                                     color=color, fuel_type=fuel_type, image=image, 
                                                     transmission=transmission)
        return standardize_response(data=vehicle_id, message='Vehicle updated successfully', code=200)
    except Exception as e:
        raise e
    
# set vehicle status
@user_bp.route('/inventory/vehicle/<int:vehicle_id>/status', methods=['PUT'])
@swag_from({
    'summary': 'Set vehicle status',
    'tags': ['User Vehicle'],
    'parameters': [
        {
            'in': 'path',
            'name': 'vehicle_id',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'vehicle_status': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Vehicle status updated successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'vehicle_id': {'type': 'integer'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad request',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def set_vehicle_status(vehicle_id):
    try:
        data = request.get_json()
        vehicle_status = data.get('vehicle_status')
        vehicle_id = g.inventory_service.change_vehicle_status(vehicle_id, vehicle_status)
        return standardize_response(data=vehicle_id, message='Vehicle status updated successfully', code=200)
    except Exception as e:
        raise e