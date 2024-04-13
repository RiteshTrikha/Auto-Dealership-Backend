from flask import request
from flasgger import swag_from
from . import inventory_bp
from .services import InventoryService
inventory_service = InventoryService()

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# get all services
@inventory_bp.route('/services', methods=['GET'])
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
@inventory_bp.route('/service/<int:service_id>', methods=['GET'])
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
    
