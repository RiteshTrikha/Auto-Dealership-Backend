from flask import request, jsonify, g, current_app
from . import user_bp 
from app.inventory.models import Addon
from app.exceptions import ExposedException
from flasgger import swag_from
from flask_jwt_extended import jwt_required 
from app.auth.auth_decorators import manager_required

# Use utilities if needed
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

@user_bp.route('/inventory/addons', methods=['GET'])
@swag_from({
    'summary': 'Retrieve all addons', 
    'tags': ['User Addons'],
    'security': [{'BearerAuth': []}],
    'responses': {
        '200': {
            'description': 'List of all addons',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'addon_name': {'type': 'string'},
                                'price': {'type': 'integer'},
                                'description': {'type': 'string'},
                                'status': {'type': 'string'}
                            }
                        }
                    },
                    'example': [
                        {
                            'addon_name': 'Extended Warranty',
                            'price': 299,
                            'description': 'Adds an additional year of warranty',
                            'status': 'ACTIVE'
                        }
                    ]
                }
            }
        },
        '401': {'description': 'Unauthorized'},
        '500': {'description': 'Internal server error'}
    }
})
@jwt_required()
@manager_required
def get_all_addons():
    try:
        addons = g.inventory_service.get_all_addons()
        if addons == []:
            return standardize_response(status='fail', message='No addons found', data=None, code=404)
        return standardize_response(status='success', message='addons found', data=addons, code=200)
    except Exception as e:
        return e

@user_bp.route('/inventory/addon/<int:addon_id>', methods=['GET'])
@swag_from({
    'summary': 'Get a single addon by its ID',
    'tags': ['User Addons'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'name': 'addon_id',
            'in': 'path',
            'required': True,
            'description': 'The ID of the addon to retrieve',
            'schema': {
                'type': 'integer'
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Details of the addon',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'addon_id': {'type': 'integer'},
                            'addon_name': {'type': 'string'},
                            'price': {'type': 'integer'},
                            'description': {'type': 'string'},
                            'status': {'type': 'string'}
                        }
                    },
                    'example': {
                        'addon_id': 1,
                        'addon_name': 'Extended Warranty',
                        'price': 299,
                        'description': 'Adds an additional year of warranty',
                        'status': 'ACTIVE'
                    }
                }
            }
        },
        '404': {'description': 'Addon not found'},
        '500': {'description': 'Internal server error'}
    }
})
@jwt_required()
@manager_required
def get_addon(addon_id):
    try :
        addon = g.inventory_service.get_addon(addon_id)
        if addon == []:
            return standardize_response(status='fail', message='No addon found', data=None, code=404)
        return standardize_response(status='success', message='Addon found',data=addon, code=200)
    except Exception as e:
        return e

# Create an addon
@user_bp.route('/inventory/addons', methods=['POST'])
@swag_from({
    'summary': 'Create an addon',
    'tags': ['User Addons'],
    'security': [{'BearerAuth': []}],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'addon_name': {'type': 'string', 'description': 'Name of the addon'},
                        'price': {'type': 'integer', 'description': 'Price of the addon'},
                        'description': {'type': 'string', 'description': 'Description of the addon'}
                    }
                }
            }
        }
    },
    'responses': {
        201: {
            'description': 'Addon created successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'addon_id': {'type': 'integer'}
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
def create_addon():
    try:
        data = request.get_json()
        addon_name = data.get('addon_name')
        price = data.get('price')
        description = data.get('description')
        addon_id_dict = g.inventory_service.create_addon(addon_name=addon_name, price=price, description=description)
        return standardize_response(data=addon_id_dict, message='Addon created successfully', code=201)
    except Exception as e:
        return e

# Update an addon
@user_bp.route('/inventory/addon/<int:addon_id>', methods=['PUT'])
@swag_from({
    'summary': 'Update an addon',
    'tags': ['User Addons'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'addon_id',
            'required': True,
            'schema': {'type': 'integer'},
            'description': 'The ID of the addon to update'
        }
    ],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'addon_name': {'type': 'string', 'description': 'Updated name of the addon'},
                        'price': {'type': 'integer', 'description': 'Updated price of the addon'},
                        'description': {'type': 'string', 'description': 'Updated description of the addon'},
                        'status': {'type': 'integer', 'description': 'Updated status of the addon'}
                    }
                }
            }
        }
    },
    'responses': {
        200: {
            'description': 'Addon updated successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'addon_id': {'type': 'integer'}
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
def update_addon(addon_id):
    try:
        data = request.get_json()
        addon_name = data.get('addon_name')
        price = data.get('price')
        description = data.get('description')
        addon_id_dict = g.inventory_service.update_addon(addon_id=addon_id, addon_name=addon_name, price=price, description=description)
        return standardize_response(status='success', data=addon_id_dict, message='Addon created successfully', code=201)
    except Exception as e:
        return e


# Change the status of an addon
@user_bp.route('/inventory/addons/<int:addon_id>/status', methods=['PUT'])
@swag_from({
    'summary': 'Change the status of an addon',
    'tags': ['User Addons'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'addon_id',
            'required': True,
            'schema': {'type': 'integer'},
            'description': 'The ID of the addon to update'
        }
    ],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'string', 'description': 'New status of the addon'}
                    }
                }
            }
        }
    },
    'responses': {
        200: {
            'description': 'Addon status updated successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'addon_id': {'type': 'integer'}
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
def change_addon_status(addon_id):
    try:
        data = request.get_json()
        status = data.get('status')
        addon_id_dict = g.inventory_service.change_addon_status(addon_id=addon_id, status=status)
        return standardize_response(status='success', data=addon_id_dict, message='Addon status updated successfully', code=201)
    except Exception as e:
        return e