from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from . import inventory_bp
from app.auth.auth_decorators import user_required, manager_required
from .services import InventoryService
inventory_service = InventoryService()

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# get all services
@inventory_bp.route('/services', methods=['GET'], endpoint='get_services')
@swag_from({
    'summary': 'Get all services',
    'tags': ['Services'],
    'responses': {
        200: {
            'description': 'All services',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': { 'type': 'string' },
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'service_id': { 'type': 'integer' },
                                        'service_type': { 'type': 'string' },
                                        'price': { 'type': 'integer' },
                                        'description': { 'type': 'string' },
                                        'status': { 'type': 'string' }
                                    }
                                }
                            },
                            'message': { 'type': 'string' },
                            'code': { 'type': 'integer' }
                        }
                    }
                }
            }
        }
    }
})
def get_services():
    try:
        services = inventory_service.get_services()
        return standardize_response(data=services)
    except Exception as e:
        return e
    
# get a service
@inventory_bp.route('/service/<int:service_id>', methods=['GET'], endpoint='get_service')
@swag_from({
    'summary': 'Get a service',
    'tags': ['Services'],
    'parameters': [
        {
            'in': 'path',
            'name': 'service_id',
            'required': True,
            'description': 'Service ID',
            'schema': {
                'type': 'integer'
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Service',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': { 'type': 'string' },
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'service_id': { 'type': 'integer' },
                                    'service_type': { 'type': 'string' },
                                    'price': { 'type': 'integer' },
                                    'description': { 'type': 'string' },
                                    'status': { 'type': 'string' }
                                }
                            },
                            'message': { 'type': 'string' },
                            'code': { 'type': 'integer' }
                        }
                    }
                }
            }
        }
    }
})
def get_service(service_id):
    try:
        service = inventory_service.get_service(service_id)
        return standardize_response(data=service)
    except Exception as e:
        return e
    
#create a service
@inventory_bp.route('/service/addservice', methods=['POST'], endpoint='add_service')
@jwt_required
@manager_required
@swag_from({
    'summary': 'Add a service',
    'tags': ['Services'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'description': 'Service details',
            'schema': {
                'type': 'object',
                'properties': {
                    'service_type': { 'type': 'string' },
                    'price': { 'type': 'integer' },
                    'description': { 'type': 'string' }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Service added',
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
        }
    }
})
def add_service():
    try:
        data = request.get_json()
        service = inventory_service.create_service(data['service_type'], data['price'], data['description'])
        return standardize_response(data=service)
    except Exception as e:
        return e
    
# update a service
@inventory_bp.route('/service/updateservice', methods=['PUT'], endpoint='update_service')
@jwt_required
@manager_required
@swag_from({
    'summary': 'Update a service',
    'tags': ['Services'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'description': 'Service details',
            'schema': {
                'type': 'object',
                'properties': {
                    'service_id': { 'type': 'integer' },
                    'service_type': { 'type': 'string' },
                    'price': { 'type': 'integer' },
                    'description': { 'type': 'string' }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Service updated',
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
        }
    }
})
def update_service():
    try:
        data = request.get_json()
        service = inventory_service.update_service(data['service_id'], data['service_type'], data['price'], data['description'])
        return standardize_response(data=service)
    except Exception as e:
        return e
    
# change service status
@inventory_bp.route('/service/changestatus', methods=['PUT'], endpoint='change_service_status')
@jwt_required
@manager_required
@swag_from({
    'summary': 'Change service status',
    'tags': ['Services'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'description': 'Service status',
            'schema': {
                'type': 'object',
                'properties': {
                    'service_id': { 'type': 'integer' },
                    'status': { 'type': 'string' }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Service status changed',
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
        }
    }
})
def change_service_status():
    try:
        data = request.get_json()
        service = inventory_service.change_service_status(data['service_id'], data['status'])
        return standardize_response(data=service)
    except Exception as e:
        return e