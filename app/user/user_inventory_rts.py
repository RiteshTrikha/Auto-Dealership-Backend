from flask import jsonify, request, current_app, g
from . import user_bp
from app.inventory.models import Vehical
from app.exceptions import ExposedException
from flasgger import swag_from

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# create vehical
@user_bp.route('/inventory/', methods=['POST'])
@swag_from({
    'summary': 'Create vehical',
    'tags': ['User vehical'],
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
            'description': 'vehical created successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'vehical_id': {'type': 'integer'}
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
def create_vehical():
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
        vehical_id = g.inventory_service.create_vehical(vin=vin, price=price, year=year, make=make, 
                                                     model=model, miles=miles, mpg=mpg, color=color, 
                                                     fuel_type=fuel_type, image=image, 
                                                     transmission=transmission)
        return standardize_response(data=vehical_id, message='vehical created successfully', code=201)
    except Exception as e:
        raise e
    
# update vehical
@user_bp.route('/inventory/vehical/<int:vehical_id>', methods=['PUT'])
@swag_from({
    'summary': 'Update vehical',
    'tags': ['User vehical'],
    'parameters': [
        {
            'in': 'path',
            'name': 'vehical_id',
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
            'description': 'vehical updated successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'vehical_id': {'type': 'integer'}
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
def update_vehical(vehical_id):
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
        vehical_id = g.inventory_service.update_vehical(vehical_id, vin=vin, price=price, year=year, 
                                                     make=make, model=model, miles=miles, mpg=mpg, 
                                                     color=color, fuel_type=fuel_type, image=image, 
                                                     transmission=transmission)
        return standardize_response(data=vehical_id, message='vehical updated successfully', code=200)
    except Exception as e:
        raise e
    
# set vehical status
@user_bp.route('/inventory/vehical/<int:vehical_id>/status', methods=['PUT'])
@swag_from({
    'summary': 'Set vehical status',
    'tags': ['User vehical'],
    'parameters': [
        {
            'in': 'path',
            'name': 'vehical_id',
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
                    'vehical_status': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'vehical status updated successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'vehical_id': {'type': 'integer'}
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
def set_vehical_status(vehical_id):
    try:
        data = request.get_json()
        vehical_status = data.get('vehical_status')
        vehical_id = g.inventory_service.change_vehical_status(vehical_id, vehical_status)
        return standardize_response(data=vehical_id, message='vehical status updated successfully', code=200)
    except Exception as e:
        raise e