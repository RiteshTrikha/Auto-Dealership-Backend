from flask import jsonify, request, current_app, g
from . import user_bp
from app.inventory.models import Vehicle
from app.exceptions import ExposedException
from flasgger import swag_from
from flask_jwt_extended import jwt_required
from app.auth.auth_decorators import manager_required

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# services routes

# create service
@user_bp.route('/inventory/service', methods=['POST'])
@swag_from({
    'summary': 'Create service',
    'tags': ['User Service'],
    'security': [{'BearerAuth': []}],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'service_type': {'type': 'string'},
                        'price': {'type': 'integer'},
                        'description': {'type': 'string'}
                    }
                }
            }
        }
    },
    'responses': {
        201: {
            'description': 'Service created successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'service_id': {'type': 'integer'}
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
@jwt_required()
@manager_required
def create_service():
    try:
        data = request.get_json()
        service_type = data.get('service_type')
        price = data.get('price')
        description = data.get('description')
        service_id_dict = g.inventory_service.create_service(service_type=service_type, price=price, description=description)
        return standardize_response(data=service_id_dict, message='Service created successfully', code=201)
    except Exception as e:
        raise e
    
# update service
@user_bp.route('/inventory/service/<int:service_id>', methods=['PUT'])
@swag_from({
    'summary': 'Update service',
    'tags': ['User Service'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'service_id',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        }
    ],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'service_type': {'type': 'string'},
                        'price': {'type': 'integer'},
                        'description': {'type': 'string'}
                    }
                }
            }
        }
    },
    'responses': {
        200: {
            'description': 'Service updated successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'service_id': {'type': 'integer'}
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
@jwt_required()
@manager_required
def update_service(service_id):
    try:
        data = request.get_json()
        service_type = data.get('service_type')
        price = data.get('price')
        description = data.get('description')
        service_id_dict = g.inventory_service.update_service(service_id=service_id, 
                                                             service_type=service_type, 
                                                             price=price, description=description)
        return standardize_response(data=service_id_dict, message='Service updated successfully', code=200)
    except Exception as e:
        raise e
    
# set service status
@user_bp.route('/inventory/service/<int:service_id>/status', methods=['PUT'])
@swag_from({
    'summary': 'Set service status',
    'tags': ['User Service'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'service_id',
            'required': True,
            'schema': { 'type': 'integer' }
        }
    ],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'service_status': { 'type': 'integer' }
                    }
                }
            }
        }
    }, 
    'responses': {
        200: {
            'description': 'Service status updated successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': { 'type': 'string' },
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'service_id': { 'type': 'integer' }
                                }
                            },
                            'message': { 'type': 'string' },
                            'code': { 'type': 'integer' }
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
                            'status': { 'type': 'string' },
                            'message': { 'type': 'string' },
                            'code': { 'type': 'integer' }
                        }
                    }
                }
            }
        }
    }
})
@jwt_required()
@manager_required
def set_service_status(service_id):
    try:
        data = request.get_json()
        service_status = data.get('service_status')
        service_id_dict = g.inventory_service.change_service_status(service_id, service_status)
        return standardize_response(data=service_id_dict, message='Service status updated successfully', code=200)
    except Exception as e:
        raise e

    



# vehicle routes

# create vehicle
@user_bp.route('/inventory/vehicle', methods=['POST'])
@swag_from({
    'summary': 'Create vehicle',
    'tags': ['User vehicle'],
    'security': [{'BearerAuth': []}],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
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
        }
    },
    'responses': {
        201: {
            'description': 'vehicle created successfully',
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
@jwt_required()
@manager_required
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
        return standardize_response(data=vehicle_id, message='vehicle created successfully', code=201)
    except Exception as e:
        raise e
    
# update vehicle
@user_bp.route('/inventory/vehicle/<int:vehicle_id>', methods=['PUT'])
@swag_from({
    'summary': 'Update vehicle',
    'tags': ['User vehicle'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'vehicle_id',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        }
    ],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
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
        }
    },
    'responses': {
        200: {
            'description': 'vehicle updated successfully',
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
@jwt_required()
@manager_required
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
        return standardize_response(data=vehicle_id, message='vehicle updated successfully', code=200)
    except Exception as e:
        raise e
    
# set vehicle status
@user_bp.route('/inventory/vehicle/<int:vehicle_id>/status', methods=['PUT'])
@swag_from({
    'summary': 'Set vehicle status',
    'tags': ['User vehicle'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'vehicle_id',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        }
    ],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'vehicle_status': {'type': 'string'}
                    }
                }
            }
        }
    },
    'responses': {
        200: {
            'description': 'vehicle status updated successfully',
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
@jwt_required()
@manager_required
def set_vehicle_status(vehicle_id):
    try:
        data = request.get_json()
        vehicle_status = data.get('vehicle_status')
        vehicle_id = g.inventory_service.change_vehicle_status(vehicle_id, vehicle_status)
        return standardize_response(data=vehicle_id, message='vehicle status updated successfully', code=200)
    except Exception as e:
        raise e